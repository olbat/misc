# Copyright (c) by INRIA, Luc Sarzyniec - 2011-2013
# CECILL License V2 - http://www.cecill.info
# For details on use and redistribution please refer to License.txt
# in Kadeploy3 sources: http://kadeploy3.gforge.inria.fr/

require 'pathname'

module NetBoot
  class NetBoot::Error < StandardError; end

  def self.custom_prefix(user, id)
    "#{user}-#{id.to_s}"
  end

  def self.Factory(kind, binary, export_kind, export_server, repository_dir,
    custom_dir, profiles_dir, profiles_kind, chain=nil
  )
    begin
      c = NetBoot.class_eval(kind)
    rescue NameError
      raise 'Invalid kind of PXE configuration'
    end

    c.new(
      binary,
      c::Export.new(export_kind, export_server),
      repository_dir,
      custom_dir,
      profiles_dir,
      profiles_kind,
      chain,
    )
  end


  class PXE
    class Export
      def initialize(kind, server)
        raise NetBoot::Error, "#{self.class.name} do not support "\
          + "'#{kind.to_s}' (supported values: #{kinds().join(', ')})"\
          unless kinds().include?(kind)
        @kind = kind
        @server = server
      end

      def kinds
        raise 'Should be reimplemented'
      end

      def path(_path)
        raise 'Should be reimplemented'
      end
    end

    attr_reader :binary
    attr_reader :export
    attr_reader :chain
    attr_reader :repository_dir
    attr_reader :custom_dir

    def initialize(binary, export, repository_dir, custom_dir, profiles_dir,
      profiles_kind, chain=nil
    )
      @binary = binary
      @export = export
      @repository_dir = repository_dir
      @custom_dir = custom_dir
      if !profiles_dir || profiles_dir.empty?
        @profiles_dir = @repository_dir
      elsif Pathname.new(profiles_dir).absolute?
        @profiles_dir = profiles_dir
      else
        @profiles_dir = File.join(@repository_dir, profiles_dir)
      end
      @profiles_kind = "profilename_#{profiles_kind}".to_sym
      @chain = chain
    end

    def boot(kind, nodes, headers, *args)
      if @chain && (@chain.class != self.class || @chain.binary != @binary)
        @chain.boot(:chain, nodes, headers, @binary)
      end

      profile, meth = __send__("boot_#{kind.to_s}".to_sym, *args)

      unless kind == :custom
        header = headers[kind].to_s
        header += "\n" if header != '' && header[-1] != "\n"
        profile = labelize(header, kind.to_s, profile, args)
      end

      write_profile(nodes, profile, meth)
    end

    protected
    def labelize(_header, _kind, _profile, _args)
      raise 'Should be reimplemented'
    end

    def boot_chain(_pxebin)
      raise 'Should be reimplemented'
    end

    def boot_local(_env, _diskname, _device_id, _partition_id, _default_pars='')
      raise 'Should be reimplemented'
    end

    def boot_network(_kernel, _initrd, _params)
      raise 'Should be reimplemented'
    end

    def boot_custom(profile, user, id, singularities=nil)
      [
        profile,
        lambda do |prof, node|
          #prof.gsub!("PXE_EXPORT",export_path(@custom_dir))
          prof.gsub!("NODE_SINGULARITY", singularities[node[:hostname]].to_s) \
            if singularities
          prof.gsub!("FILES_PREFIX",
            File.join(
              export_path(@custom_dir),
              NetBoot.custom_prefix(user, id),
            ),
          )
          prof
        end,
      ]
    end

    def export_path(path)
      @export.path(path)
    end

    private
    def profilename_hostname(node)
      node[:hostname]
    end

    def profilename_hostname_short(node)
      node[:hostname].split('.')[0]
    end

    def profilename_ip(node)
      node[:ip].strip
    end

    def profilename_ip_hex(node)
      node[:ip].split(".").collect{ |n| sprintf("%02X", n) }.join('')
    end

    def profile_dir(node)
      File.join(@profiles_dir, __send__(@profiles_kind, node))
    end

    def write_profile(nodes, profile, meth=nil)
      prof = profile
      nodes.each do |node|
        file = profile_dir(node)
        File.delete(file) if File.exist?(file)
        begin
          f = File.new(file, File::CREAT | File::RDWR, 0644)
          prof = meth.call(profile.dup, node) if meth
          f.write(prof)
          f.close
        rescue
          return false
        end
      end
      true
    end
  end

  class PXElinux < PXE
    class Export < PXE::Export
      def kinds
        [
          :tftp
        ]
      end

      def path(path)
        if path
          File.join('/', path)
        else
          ''
        end
      end
    end

    def labelize(header, kind, profile, *_args)
      header +
      "DEFAULT #{kind}\n"\
      "LABEL #{kind}\n"\
      + profile.collect{|line| "\t#{line}" }.join("\n")
    end

    def boot_chain(pxebin)
      [[
        "KERNEL #{export_path(pxebin)}",
        "APPEND keeppxe"
      ]]
    end

    def boot_local(_env, _diskname, device_id, partition_id, _default_pars='')
      [[
        "COM32 #{export_path('chain.c32')}",
        "APPEND hd#{device_id} #{partition_id}",
      ]]
    end

    def boot_network(kernel, initrd, params)
      profile = []
      if initrd
        initrd = "initrd=#{export_path(initrd)} "
      else
        initrd = ''
      end

      profile << "KERNEL #{export_path(kernel)}"
      profile << "APPEND #{initrd}#{params}"

      [ profile ]
    end
  end

  class GPXElinux < PXElinux
    class Export < PXE::Export
      def kinds
        [
          :tftp,
          :http,
          :ftp,
        ]
      end

      def path(path)
        case @kind
        when :tftp
          if path
            File.join('/', path)
          else
            ''
          end
        when :http, :ftp
          if path
            File.join("#{@kind.to_s}://", @server, path)
          else
            File.join("#{@kind.to_s}://", @server)
          end
        end
      end
    end

  end

  class IPXE < PXE
    class Export < PXE::Export
      def kinds
        [
          :tftp,
          :http,
          :ftp,
        ]
      end

      def path(path)
        case @kind
        when :tftp
          if path
            File.join('/', path)
          else
            ''
          end
        when :http, :ftp
          if path
            File.join("#{@kind.to_s}://", @server, path)
          else
            File.join("#{@kind.to_s}://", @server)
          end
        end
      end
    end

    def labelize(header, _kind, profile, *_args)
      "#!ipxe\n#{header}#{profile.join("\n")}"
    end

    def boot_chain(pxebin)
      [[
        "chain #{export_path(pxebin)}"
      ]]
    end

    def boot_local(_env, _diskname, device_id, partition_id, _default_pars='')
      [[
        "chain #{export_path('chain.c32')} hd#{device_id} #{partition_id}"
      ]]
    end

    def boot_network(kernel, initrd, params)
      profile = []

      profile << "initrd #{export_path(initrd)}" if initrd
      profile << "chain #{export_path(kernel)} #{params}"

      [ profile ]
    end
  end

  class GrubPXE < PXE
    class Export < PXE::Export
      def kinds
        [
          :tftp,
          :http,
        ]
      end

      def path(path)
        case @kind
        when :tftp
          # Compatibility for old GRUB disks versions
          if path
            File.join('(pxe)', path)
          else
            '(pxe)'
          end
        when :http
          if path
            File.join("(#{@kind.to_s},#{@server})", path)
          else
            "(#{@kind.to_s},#{@server})"
          end
        end
      end
    end

    def labelize(header, kind, profile, *_args)
      header += "\ntimeout=0\n" unless header.include?("timeout")
      header +
      "default=0\n"\
      "menuentry #{kind} {\n"\
      "#{profile.collect{|line| "\t#{line}" }.join("\n")}\n"\
      "}"
    end

    def boot_chain(pxebin)
      [[
        "pxechainloader #{export_path(pxebin)}",
        "boot",
      ]]
    end

    def boot_local(env, diskname, device_id, partition_id, default_params='')
      # The search command should be used to find the device, several options:
      #   --fs-uuid + one microstep to gather the uuid on each machine
      #   --label + write a label on the disk when partitioning
      #   --file + create a unique file (deploy ID# ?) on the deployed fs
      profile = [ "set root=(hd#{device_id},#{partition_id})" ]

      partname = "#{diskname}#{partition_id}"
      kernel_params = (env.kernel_params.empty? \
        ? default_params : env.kernel_params)

      case env.environment_kind
      when 'linux'
        profile << "linux #{env.kernel} #{kernel_params} root=#{partname}"
        profile << "initrd #{env.initrd}" if env.initrd && !env.initrd.empty?
      when 'xen'
        profile << "multiboot #{env.hypervisor} #{env.hypervisor_params}"
        profile << "module #{env.kernel} #{kernel_params} root=#{partname}"
        profile << "module #{env.initrd}" if env.initrd && !env.initrd.empty?
      when 'bsd'
        profile << "insmod ufs1"
        profile << "insmod ufs2"
        profile << "insmod zfs"
        profile << "chainloader +1"
      when 'windows'
        profile << "insmod fat"
        profile << "insmod ntfs"
        profile << "ntldr /bootmgr"
      when 'other'
        profile << "chainloader +1"
      end

      [ profile ]
    end

    def boot_network(kernel, initrd, params, kind='linux')
      profile = []

      profile << "#{kind} #{export_path(kernel)} #{params}"
      profile << "initrd #{export_path(initrd)}" if initrd

      [ profile ]
    end
  end
end
