require 'benchmark'

n = 10_000
v=DATA.read
Benchmark.bm do |x|
  x.report('with'){n.times{v.scan(/<(?:".*"|'.*'|.)+?>/)}}
  x.report('without lazy'){n.times{v.scan(/<.+?>/)}}
  x.report('without greedy'){n.times{v.scan(/<[^>]+>/)}}
end

__END__
<!-- test --><!-- test --><!doctype html>
<html xmlns:fb="http://ogp.me/ns/fb#" class="no-js no-ad s0-f1 s1- t-ranking" lang="fr">
<head>
	<meta charset="utf-8"><title>Classement ecurie 2015 - F1 sur Sports.fr</title><meta name="description" content="Classement ecurie 2015"><meta property="og:title" content="Classement ecurie 2015"><meta property="og:description" content="Classement ecurie 2015"><meta property="og:type" content="website"><meta property="og:url"  content="http://www.sports.fr/f1/classement-ecuries.html"><meta property="og:site_name" content="Sports.fr"><meta property="fb:app_id" content="198961146857248" /><meta name="robots" content="index,follow"><meta name="revisit-after" content="1 days"><meta name="distribution" content="global"><meta http-equiv="content-language" content="fr-FR"><meta name="language" content="fr-FR"><link rel="shortcut icon" href="../../cdn.sports.fr/includes/cobrand/default/img/icon-favicon.ico"><meta name="viewport" content="width=1000px"><link rel="apple-touch-icon" href="../../cdn.sports.fr/includes/cobrand/default/img/icon-apple-touch-57.png"><link rel="apple-touch-icon" sizes="72x72" href="../../cdn.sports.fr/includes/cobrand/default/img/icon-apple-touch-72.png"><link rel="apple-touch-icon" sizes="114x114" href="../../cdn.sports.fr/includes/cobrand/default/img/icon-apple-touch-114.png"><meta http-equiv="cleartype" content="on"><meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"><meta http-equiv="imagetoolbar" content="no"><meta name="google-site-verification" content="f4twh4EFnyOcl2W6d_N8D97YNuFIY0cjaX5LpSl9a3g" /><meta content="600" http-equiv="refresh" />
	
  

	<link rel="stylesheet" href="../../cdn.sports.fr/includes/cobrand/default/css/default.min.css?s176">
	<script>ENV={country: "",domain: "sports.fr",view: "default",section: "f1",subSection: "",subSectionName: "",contentIncludeFilename: "team.htm",type: "ranking",cobrandWebdynUrl: "http://webdyn.sports.fr/",univers: "",cobrand: "sports",contentId: "",contentTitle: "Classement%20ecurie%202015",displayAds: "0"};sas_tmstp=Math.round(Math.random()*10000000000);sas_masterflag=1;function SmartAdServer(sas_pageid,sas_formatid,sas_target){if (sas_masterflag==1){sas_masterflag=0;sas_master='M';}else{sas_master='S';};document.write('<scr'+'ipt src="http://www.smartadserver.com/call/pubj/' + sas_pageid + '/' + sas_formatid + '/' + sas_master + '/' + sas_tmstp + '/' + escape(sas_target) + '?"></scr'+'ipt>');}</script>
	<!--[if lt IE 9]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
	<script src="../../cdn.sports.fr/includes/cobrand/default/js/default.min.js?s169"></script>
	<script>var tc_vars = new Array();tc_vars["content_id"] = ENV.contentId;tc_vars["content_level1"] = ENV.section;tc_vars["content_level2"] = ENV.subSection;tc_vars["content_label"] = ENV.contentTitle;tc_vars["content_class"] = ENV.type;tc_vars["custom1"] = '';if( $.cookie("sports_user_info") ) tc_vars["custom1"] = "connecte";</script>
	<script type="text/javascript" src="http://analytics.ladmedia.fr/sports/analytics_sports.js"></script>
	
	<script type="text/javascript">
		window._taboola = window._taboola || [];
		_taboola.push({category:'auto'});
		!function (e, f, u) { 
			e.async = 1; e.src = u;
			f.parentNode.insertBefore(e, f);
		}(document.createElement('script'),
		document.getElementsByTagName('script')[0], 'http://cdn.taboola.com/libtrc/lagardere-sports/loader.js');
	</script> 
	
	
	
	
		<link rel="stylesheet" href="http://cdn.sports.fr/includes/cobrand/default/css/files/rwd.min.css"/>
	
		

	<meta name="apple-itunes-app" content="app-id=308333134">
</head>


	<body>
	
	
	<script>
		var oan_siteKeywords="", oan_siteContentTopic="", oan_protocol = (window.location.protocol=='https:') ? 'https:' : 'http:', oan_site = 'sports', site = 'spo';
		document.write('<scr'+'ipt src="'+oan_protocol+'//sports.refr.adgtw.orangeads.fr/js/spo_'+_sectionName+'?sKW=' + encodeURI(oan_siteKeywords) + '&sCT=' + encodeURI(oan_siteContentTopic) + '"><\/scr'+'ipt>');
	</script>
	<section id="top">
		<div class="trunk">
			<ul class="first">
				<li id="connect-box">
					<div id="user-box"></div>
					<div id="user-login-box" class="hide"></div>
					<div id="user-logout-box" class="hide"></div>
					<div id="user-registration-box" class="hide"></div>
					<div id="user-forget-password-box" class="hide"></div>
					<div id="user-confirm-password-box" class="hide"></div>
					<div id="user-dummy-form"></div>
					<div id="user-comment-box"></div>
				</li><!--
			 --><li data-link='{"url": "aHR0cDovL3d3dy5ydWdieW5ld3MuZnI=","target": "_blank"}' class='a'>Rugbynews.fr</li><!--
			 --><li data-link='{"url": "aHR0cDovL3d3dy5mb290YmFsbC1tYWcuZnI=","target": "_blank"}' class='a'>FootballMag.fr</li><!--
			 --><li data-link='{"url": "aHR0cDovL3d3dy5jeWNsaXNtZS1tYWcuY29t","target": "_blank"}' class='a'>CyclismeMag.com</li><!--
			 --><li data-link='{"url": "aHR0cDovL3d3dy5pbG92ZXBva2VyLmZy","target": "_blank"}' class='a'>Ilovepoker.fr</li><!--
			 --><li data-link='{"url": "aHR0cDovL3d3dy5mb290YmFsbC5mcg==","target": "_blank"}' class='a'>Football.fr</li>
			</ul>
			
						<div id="social-count" class="fr" style="overflow: hidden;padding-top: 5px;">
							<div id="___follow_0" style="text-indent: 0px; margin: 0px; padding: 0px; background-color: transparent; border-style: none; line-height: normal; font-size: 1px; vertical-align: baseline;margin-left:5px; display: inline-block; width: 88px; height: 20px; background-position: initial initial; background-repeat: initial initial;" class="fr"><iframe frameborder="0" hspace="0" marginheight="0" marginwidth="0" scrolling="no" style="position: static; top: 0px; width: 88px; margin: 0px; border-style: none; left: 0px; visibility: visible; height: 20px;" tabindex="0" vspace="0" width="100%" id="I0_1396271069233" name="I0_1396271069233" src="https://apis.google.com/_/widget/render/follow?usegapi=1&amp;annotation=none&amp;height=20&amp;rel=publisher&amp;hl=fr&amp;origin=http%3A%2F%2Fwww.sports.fr&amp;url=http%3A%2F%2Fplus.google.com%2F115671695822593249805&amp;gsrc=3p&amp;ic=1&amp;jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.fr.Y0bOYvQy8LQ.O%2Fm%3D__features__%2Fam%3DAQ%2Frt%3Dj%2Fd%3D1%2Fz%3Dzcms%2Frs%3DAItRSTM3mrYZYDM0RbsmGc4IcTM4HAsUrg#_methods=onPlusOne%2C_ready%2C_close%2C_open%2C_resizeMe%2C_renderstart%2Concircled%2Cdrefresh%2Cerefresh%2Conload&amp;id=I0_1396271069233&amp;parent=http%3A%2F%2Fwww.sports.fr&amp;pfname=&amp;rpctoken=25026329" data-gapiattached="true"></iframe></div>
						<iframe id="frame-twitter" width="57" height="20" class="frame-twitter fr" allowtransparency="true" frameborder="0" scrolling="no" src="http://platform.twitter.com/widgets/follow_button.html?screen_name=sports_fr&amp;lang=fr&amp;show_count=false&amp;show_screen_name=false"></iframe> 
    					<div class="frame-facebook fr"><iframe src="http://www.facebook.com/plugins/like.php?href=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fplugins%2F&amp;width&amp;layout=button&amp;action=like&amp;show_faces=false&amp;share=false&amp;height=35&amp;appId=183153745084717" scrolling="no" frameborder="0" style="border:none; overflow:hidden; height:35px;width: 60px;margin-right:5px;" allowTransparency="true"></iframe></div>
						</div>
			
		</div><!-- #top .trunk -->
	</section><!-- #top -->
	<div id="overall">
		<header id="header">
			<div class="trunk">
				<div id="branding">
					<a href="../index.html" id="logo"><img src="../../cdn.sports.fr/includes/cobrand/default/img/logo.png" alt="Sports.fr" width="170" height="47" /></a>
					<div id="ad-rec-top1" class="box-ad ads-210x90-1"></div>
					<div id="ad-rec-top2" class="box-ad ads-210x90-2"></div>
				</div><!-- #branding -->
			</div><!-- #header .trunk -->
		</header><!-- #header -->
		
		<nav id="nav">
	<div class="trunk">
		<div id="main-nav">
			<ul class="tabs tabs-s2">
					<li class="tab tab-accueil"><a href="../index.html" class="tab-link"><span><b>Accueil</b></span></a></li><!--
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../video-sport/index.html" class="tab-link"><span><b>Vidéos</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../football/index.html" class="tab-link"><span><b>Football</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../tennis/index.html" class="tab-link"><span><b>Tennis</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../basket/index.html" class="tab-link"><span><b>Basket</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../handball/index.html" class="tab-link"><span><b>Hand</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../sports-us/index.html" class="tab-link"><span><b>Sports US</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../rugby/index.html" class="tab-link"><span><b>Rugby</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../cyclisme/index.html" class="tab-link"><span><b>Cyclisme</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="index.html" class="tab-link"><span><b>F1</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../auto-moto/index.html" class="tab-link"><span><b>Auto-Moto</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../ski/index.html" class="tab-link"><span><b>Ski</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../natation/index.html" class="tab-link"><span><b>Natation</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../omnisports/index.html" class="tab-link"><span><b>Autres</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab tab-livescores"><a href="../livescore.html" class="tab-link"><span><b>Livescore</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="../poker/index.html" class="tab-link"><span><b>Poker</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
					--><!-- 
						--><li class="tab"><a href="classement-ecuries.html" class="tab-link"><span><b>Services</b></span></a></li><!-- 
					--><!-- 
				--><!-- 
			--></ul>
		</div>
											
									
		
		
			
						
		
			<div class="ssnav">
				<div class="sub-nav">
					<strong>
					
						
							<a href="classement-ecuries.html#">F1</a>
						
					</strong>
					<ul>
									<!-- 
							--><!--
								--><li><a href="calendrier.html" alt="Calendrier" taget="_self">Calendrier</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li><a href="resultats.html" alt="Résultats" taget="_self">Résultats</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li><a href="classement-pilotes.html" alt="Classement pilotes" taget="_self">Classement pilotes</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li class="active"><a href="classement-ecuries.html" alt="Classement écuries" taget="_self">Classement écuries</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li><a href="pilotes/effectif.html" alt="Pilotes" taget="_self">Pilotes</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li><a href="ecuries/effectif.html" alt="Ecuries" taget="_self">Ecuries</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li><a href="circuits/liste.html" alt="Circuits" taget="_self">Circuits</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li><a href="palmares-pilotes.html" alt="Palmarès" taget="_self">Palmarès</a></li><!--
							--><!-- 
			-->					<!-- 
							--><!--
								--><li><a href="2014/resultats.html" alt="Saison 2014" taget="_self">Saison 2014</a></li><!--
							--><!-- 
			-->			
					</ul>
				</div>
			</div>
		
												
	</div><!-- #nav .trunk -->
</nav><!-- #nav -->
        
    <div class="nav-window sub-nav-football">
        <a name="football"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../football/ligue-1/index.html" title="Ligue 1">Ligue 1</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/ligue-1/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/ligue-1/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-1/classement.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/ligue-1/buteurs.html" title="Buteurs">Buteurs</a>
	                                                /
	                                                <a class="ib" href="../football/ligue-1/passeurs.html" target="_self" title="Passeurs">Passeurs</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-1/clubs.html" title="Clubs Ligue 1">Clubs Ligue 1</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-1/notes.html" title="Notes">Notes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/amical-ligue-1/resultats.html" title="Matchs Amicaux">Matchs Amicaux</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/trophee-des-champions/resultats.html" title="TdC">TdC</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/ligue-2/index.html" title="Ligue 2">Ligue 2</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/ligue-2/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/ligue-2/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-2/classement.html" title="Classement Ligue 2">Classement Ligue 2</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/ligue-2/buteurs.html" title="Buteurs">Buteurs</a>
	                                                /
	                                                <a class="ib" href="../football/ligue-2/passeurs.html" target="_self" title="Passeurs">Passeurs</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-2/clubs.html" title="Clubs Ligue 2">Clubs Ligue 2</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/coupe-de-france/index.html" title="Coupe de France">Coupe de France</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/coupe-de-la-ligue/index.html" title="Coupe de la Ligue">Coupe de la Ligue</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/national/resultats.html" title="National">National</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/cfa-groupe-a/resultats.html" title="CFA">CFA</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../football/allemagne/index.html" title="Allemagne">Allemagne</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/allemagne/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/allemagne/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/allemagne/classement.html" title="Classement Allemagne">Classement Allemagne</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/coupe-d-allemagne/resultats.html" title="Coupe d'Allemagne">Coupe d'Allemagne</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/angleterre/index.html" title="Angleterre">Angleterre</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/angleterre/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/angleterre/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/angleterre/classement.html" title="Classement Angleterre">Classement Angleterre</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/league-cup/resultats.html" title="League Cup">League Cup</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/coupe-d-angleterre/resultats.html" title="Coupe d'Angleterre">Coupe d'Angleterre</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/community-shield/resultats.html" title="Community Shield">Community Shield</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/espagne/index.html" title="Espagne">Espagne</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/espagne/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/espagne/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/espagne/classement.html" title="Classement Espagne">Classement Espagne</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/coupe-d-espagne/resultats.html" title="Coupe d'Espagne">Coupe d'Espagne</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/italie/index.html" title="Italie">Italie</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/italie/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/italie/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/italie/classement.html" title="Classement Italie">Classement Italie</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/coupe-d-italie/resultats.html" title="Coupe d'Italie">Coupe d'Italie</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/etranger/index.html" title="Etranger">Etranger</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../football/ligue-des-champions/index.html" title="Ligue des Champions">Ligue des Champions</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/ligue-des-champions/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/ligue-des-champions/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-des-champions/buteurs.html" title="Buteurs">Buteurs</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-des-champions/groupe-a.html" title="Groupes">Groupes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/ligue-europa/index.html" title="Ligue Europa">Ligue Europa</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/ligue-europa/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../football/ligue-europa/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/ligue-europa/groupe-a.html" title="Groupes">Groupes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/coupe-du-monde-des-clubs/resultats.html" title="Coupe du Monde des Clubs">Coupe du Monde des Clubs</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/transferts/index.html" title="Transferts">Transferts</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/mercato-en-direct.html" title="Mercato en direct">Mercato en direct</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/ligue-1/mercato-foot.html" title="Ligue 1">Ligue 1</a>
	                                                /
	                                                <a class="ib" href="../football/ligue-2/mercato-foot.html" target="_self" title="Ligue 2 ">Ligue 2 </a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/allemagne/mercato-foot.html" title="Allemagne">Allemagne</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/angleterre/mercato-foot.html" title="Angleterre">Angleterre</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/espagne/mercato-foot.html" title="Espagne">Espagne</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/italie/mercato-foot.html" title="Italie">Italie</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../football/equipe-de-france/index.html" title="Equipe de France">Equipe de France</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/equipe-de-france/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/equipe-de-france/classement-fifa.html" title="Classement FIFA">Classement FIFA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/equipe-de-france/effectif.html" title="Effectif">Effectif</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/euro-2016/index.html" title="Euro 2016">Euro 2016</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-a.html" title="Groupe A">Groupe A</a>
	                                                /
	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-b.html" target="_self" title="Groupe B">Groupe B</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-c.html" title="Groupe C">Groupe C</a>
	                                                /
	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-d.html" target="_self" title="Groupe D">Groupe D</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-e.html" title="Groupe E">Groupe E</a>
	                                                /
	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-f.html" target="_self" title="Groupe F">Groupe F</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-g.html" title="Groupe G">Groupe G</a>
	                                                /
	                                                <a class="ib" href="../football/euro-2016/qualifications/groupe-h.html" target="_self" title="Groupe H">Groupe H</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../football/euro-2016/qualifications/groupe-i.html" title="Groupe I">Groupe I</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/coupe-du-monde-2014/index.html" title="CM 2014">CM 2014</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/coupe-du-monde-feminine-2015/resultats.html" title="CM 2015 (F)">CM 2015 (F)</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/euro-femmes/calendrier.html" title="Euro 2013 (F)">Euro 2013 (F)</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/coupe-des-confederations/resultats.html" title="C.Confédérations">C.Confédérations</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/copa-america/2011/resultats.html" title="Copa America">Copa America</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../football/can/index.html" title="CAN">CAN</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L2Zvb3RiYWxsL2xpZ3VlLWRlcy1jaGFtcGlvbnMvYXJ0aWNsZXMvdGhpYWdvLW1vdHRhLWluc3VsdGUtcGFyLWpvaG4tdGVycnktYS1sYS1taS10ZW1wcy0xMTk2NzMy", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Altercation Thiago Motta-Fabregas à la mi-temps ?
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/football/ligue-des-champions/articles/altercation-thiago-motta-fabregas-a-la-mi-temps/psg-chelsea-tension/14048087-1-fre-FR/PSG-Chelsea-tension_w160.jpg">
                <p>Le passage aux vestiaires à la pause aurait été quelque peu houleux, mercredi soir, à Stamford B...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-tennis">
        <a name="tennis"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../tennis/resultats-atp.html" title="ATP">ATP</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/resultats-atp.html" title="Résultats ATP">Résultats ATP</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/atp/classement/atp-technique-1.html" title="Classement ATP">Classement ATP</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/atp/joueurs.html" title="Joueurs ATP">Joueurs ATP</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/2014/atp/resultats.html" title="Résultats 2014">Résultats 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/atp/tournois-de-la-semaine.html" title="Tournois de la semaine">Tournois de la semaine</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../tennis/resultats-wta.html" title="WTA">WTA</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/resultats-wta.html" title="Résultats WTA">Résultats WTA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/wta/classement/wta-technique-1.html" title="Classement WTA">Classement WTA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                                                        	
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/2014/wta/resultats.html" title="Résultats 2014">Résultats 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/wta/tournois-de-la-semaine.html" title="Tournois de la semaine">Tournois de la semaine</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../tennis/open-d-australie/index.html" title="Open d'Australie">Open d'Australie</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/australie/resultats-messieurs.html" title="Tableau messieurs">Tableau messieurs</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/australie/resultats-dames.html" title="Tableau dames">Tableau dames</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/australie/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../tennis/roland-garros/index.html" title="Roland Garros">Roland Garros</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/roland-garros/resultats-messieurs.html" title="Tableau messieurs">Tableau messieurs</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/roland-garros/resultats-dames.html" title="Tableau dames">Tableau dames</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/roland-garros/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../tennis/wimbledon/index.html" title="Wimbledon">Wimbledon</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/wimbledon/resultats-messieurs.html" title="Tableau messieurs">Tableau messieurs</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/wimbledon/resultats-dames.html" title="Tableau dames">Tableau dames</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/wimbledon/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../tennis/us-open/index.html" title="US Open">US Open</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/us-open/resultats-messieurs.html" title="Tableau messieurs">Tableau messieurs</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/us-open/resultats-dames.html" title="Tableau dames">Tableau dames</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/us-open/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../tennis/coupe-davis/index.html" title="Coupe Davis">Coupe Davis</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/coupe-davis/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/coupe-davis/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../tennis/fed-cup/index.html" title="Fed Cup">Fed Cup</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/fed-cup/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../tennis/fed-cup/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                            
						                        <dl>
                            <dt>
                                <a href="https://www.betclic.fr/c/paris-tennis/" title="Parier sur le tennis">Parier sur le tennis</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                  	
						                                    </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L3Rlbm5pcy9hcnRpY2xlcy91bi1yZXRvdXItbm9uLW1lcmNpLXBvdXItYmFydG9saS0xMTk2NDc0", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Bartoli n'a jamais voulu revenir
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/tennis/articles/bartoli-revient-sur-son-vrai-faux-come-back/marion_bartoli_reu/14045907-1-fre-FR/marion_bartoli_reu_w160.jpg">
                <p>Marion Bartoli s'est exprimée mercredi sur la rumeur qu'elle a elle-même entretenue d'un possibl...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-basket">
        <a name="basket"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../basket/pro-a/resultats.html" title="Pro A">Pro A</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../basket/pro-a/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../basket/pro-a/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../basket/pro-a/classement.html" title="Classement Pro A">Classement Pro A</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../basket/pro-a/clubs.html" title="Clubs Pro A">Clubs Pro A</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../basket/leaders-cup/resultats.html" title="Leaders Cup">Leaders Cup</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../basket/pro-b/resultats.html" title="Pro B">Pro B</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../basket/pro-b/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../basket/pro-b/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../basket/pro-b/classement.html" title="Classement Pro B">Classement Pro B</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../basket/coupe-de-france/resultats.html" title="Coupe de France">Coupe de France</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../basket/lfb/resultats.html" title="LFB">LFB</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../basket/lfb/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../basket/lfb/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../basket/lfb/classement.html" title="Classement LFB">Classement LFB</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../basket/euroligue-hommes/resultats.html" title="Euroligue (H)">Euroligue (H)</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../basket/euroligue-femmes/resultats.html" title="Euroligue (F)">Euroligue (F)</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../basket/coupe-du-monde-hommes/resultats.html" title="Mondial (H)">Mondial (H)</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../basket/championnat-du-monde-femmes/resultats.html" title="Mondial (F)">Mondial (F)</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../basket/championnat-du-monde-femmes/groupe-b.html" title="Groupe B (France)">Groupe B (France)</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../basket/euro-hommes/resultats.html" title="Euro 2013 (H)">Euro 2013 (H)</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../basket/euro-femmes/resultats.html" title="Euro 2013 (F)">Euro 2013 (F)</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../nba/index.html" title="NBA">NBA</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/calendrier.html" title="Saison régulière">Saison régulière</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/classement-conferences.html" title="Classement NBA">Classement NBA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/equipes.html" title="Équipes NBA">Équipes NBA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/2014/playoffs/miami-san-antonio.html" title="Finales 2014">Finales 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/statistiques-francais.html" title="Français">Français</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/historique.html" title="Historique">Historique</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                            
						                        <dl>
                            <dt>
                                <a href="https://www.betclic.fr/c/paris-basket/" title="Parier sur le basket">Parier sur le basket</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                  	
						                                    </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L25iYS9hcnRpY2xlcy9jdXJyeS1qYW1lcy1oYXJkZW4td2VzdGJyb29rLXF1aS1zZXJhLW12cC0xMTk0ODE0", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Curry, James, Westbrook: qui sera MVP ?
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/nba/articles/curry-james-harden-westbrook-qui-sera-mvp/mvp-collage/14031519-1-fre-FR/MVP-Collage_w160.jpg">
                <p>A un mois du terme de la saison régulière en NBA, les candidats au titre de MVP se bousculent. S...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-hand">
        <a name="hand"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../handball/division-1/resultats.html" title="Division 1">Division 1</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/division-1/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/division-1/classement.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/division-1/calendrier.html" title="Calendrier">Calendrier</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/division-1/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../handball/division-1-f/resultats.html" title="Division 1 (F)">Division 1 (F)</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/division-1-f/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/division-1-f/classement.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/division-1-f/calendrier.html" title="Calendrier">Calendrier</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../handball/ligue-des-champions/resultats.html" title="LDC">LDC</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/ligue-des-champions/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/ligue-des-champions/calendrier.html" title="Calendrier">Calendrier</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../handball/championnat-du-monde/resultats.html" title="Mondial">Mondial</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/championnat-du-monde/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/championnat-du-monde-hommes/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../handball/championnat-du-monde-femmes/resultats.html" title="Mondial (F)">Mondial (F)</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/championnat-du-monde-femmes/poule-a.html" title="Poule A (France)">Poule A (France)</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/championnat-du-monde-femmes/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../handball/championnat-d-europe/resultats.html" title="Euro">Euro</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/championnat-d-europe/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../handball/championnat-d-europe-femmes/resultats.html" title="Euro (F)">Euro (F)</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../handball/championnat-d-europe-femmes/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            
            
        
        
    </div>

                
    <div class="nav-window sub-nav-sportsus">
        <a name="sportsus"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../nba/index.html" title="NBA">NBA</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../nba/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../nba/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/classement-conferences.html" title="Classement NBA">Classement NBA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/equipes.html" title="Équipes NBA">Équipes NBA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/statistiques-francais.html" title="Français">Français</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/historique.html" title="Historique">Historique</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/2014/playoffs/miami-san-antonio.html" title="Finales 2014">Finales 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/playoffs-est.html" title="Playoffs Est">Playoffs Est</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nba/playoffs-ouest.html" title="Playoffs Ouest">Playoffs Ouest</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../sports-us/nhl/index.html" title="NHL">NHL</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nhl/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../sports-us/nfl/index.html" title="NFL">NFL</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nfl/resultats.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nfl/classement.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../nfl/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            
            
        
        
    </div>

                
    <div class="nav-window sub-nav-rugby">
        <a name="rugby"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../rugby/top-14/index.html" title="Top 14">Top 14</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../rugby/top-14/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../rugby/top-14/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/top-14/classement.html" title="Classement Top 14">Classement Top 14</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/top-14/marqueurs-d-essais.html" title="Marqueurs d'essais">Marqueurs d'essais</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/top-14/realisateurs.html" title="Réalisateurs">Réalisateurs</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/top-14/clubs.html" title="Clubs Top 14">Clubs Top 14</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/match-amical/resultats.html" title="Matches amicaux">Matches amicaux</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../rugby/pro-d2/resultats.html" title="Pro D2">Pro D2</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../rugby/pro-d2/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../rugby/pro-d2/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/pro-d2/classement.html" title="Classement Pro D2">Classement Pro D2</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../rugby/coupe-d-europe/resultats.html" title="Coupe d'Europe">Coupe d'Europe</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../rugby/coupe-d-europe/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../rugby/coupe-d-europe/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                    
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../rugby/challenge-europeen/resultats.html" title="Challenge Européen">Challenge Européen</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../rugby/challenge-europeen/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../rugby/challenge-europeen/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                    
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../rugby/xv-de-france/index.html" title="XV de France">XV de France</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/calendrier/2015/france.html" title="Calendrier">Calendrier</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/equipes/effectif/france.html" title="Effectif">Effectif</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/equipes/france.html" title="Fiche">Fiche</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../rugby/6-nations/index.html" title="6 Nations">6 Nations</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../rugby/6-nations/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../rugby/6-nations/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/6-nations/classement.html" title="Classement 6 Nations">Classement 6 Nations</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/6-nations/equipes.html" title="Équipes">Équipes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/6-nations/stades.html" title="Stades">Stades</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/6-nations/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/6-nations/grands-chelem.html" title="Grands Chelems">Grands Chelems</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/6-nations/records.html" title="Records">Records</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../rugby/international/index.html" title="International">International</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/international/resultats/test-match.html" title="Test Match">Test Match</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/international/classement_irb.html" title="Classement IRB">Classement IRB</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/coupe-du-monde-2011/index.html" title="Coupe du monde">Coupe du monde</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/championnats-du-monde-u20/resultats.html" title="Mondial U20">Mondial U20</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../rugby/four-nations/resultats.html" title="Four-Nations">Four-Nations</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../rugby/four-nations/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../rugby/four-nations/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../rugby/four-nations/classement.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="https://www.betclic.fr/calendrier/rugby-à-xv-s5i1" title="Parier sur le rugby">Parier sur le rugby</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L3J1Z2J5L3h2LWRlLWZyYW5jZS9hcnRpY2xlcy9wc2Etb3BlcmUtOC1jaGFuZ2VtZW50cy1hdS1zZWluLWR1LXh2LWRlLWZyYW5jZS0xMTk2Mzkx", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Du changement, vraiment ?
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/rugby/xv-de-france/articles/xv-de-france-du-changement-vraiment/nicolas-mas/14045038-1-fre-FR/Nicolas-Mas_w160.jpg">
                <p>Le sélectionneur du XV de France Philippe Saint-André a communiqué ce jeudi matin à Marcoussis l...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-cyclisme">
        <a name="cyclisme"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../cyclisme/world-tour.html" title="World Tour">World Tour</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/world-tour.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/equipes/equipes-world-tour.html" title="Équipes">Équipes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../cyclisme/tour-de-france/index.html" title="Tour de France">Tour de France</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/resultats2014/tour-de-france/tour-de-france-classement-general.html" title="Classements">Classements</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/tour-de-france/etapes.html" title="Étapes">Étapes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/tour-de-france/carte.html" title="Carte 2014">Carte 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/tour-de-france/coureurs.html" title="Participants 2014">Participants 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/palmares/palmares-tour-de-france.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../cyclisme/tour-d-italie/index.html" title="Tour d'Italie">Tour d'Italie</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/resultats2014/tour-d-italie/tour-d-italie-classement-general.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/tour-d-italie-2014/carte.html" title="Parcours">Parcours</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/palmares/palmares-tour-d-italie.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../cyclisme/tour-d-espagne/index.html" title="Tour d'Espagne">Tour d'Espagne</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/resultats2014/tour-d-espagne/tour-d-espagne-classement-general.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/tour-d-espagne/parcours.html" title="Parcours">Parcours</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../cyclisme/palmares/palmares-tour-d-espagne.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L2N5Y2xpc21lL2FydGljbGVzL3JpY2hpZS1wb3J0ZS1ldC1sYS1za3ktcmVnbmVudC1zdXItcGFyaXMtbmljZS0xMTk2NTMy", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
La Sky en a sous la pédale
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/cyclisme/articles/paris-nice-demonstration-de-force-du-team-sky/richie_porte_portrait_paris_nice_icon/14046371-1-fre-FR/richie_porte_portrait_paris_nice_icon_w160.jpg">
                <p>Après une saison 2014 décevante, le Team Sky veut briller en 2015. Les coureurs de Dave Brailsfo...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-f1">
        <a name="f1"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="index.html" title="Saison 2015">Saison 2015</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="calendrier.html" title="Calendrier F1">Calendrier F1</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="resultats.html" title="Résultats F1">Résultats F1</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="classement-pilotes.html" title="Classement pilotes">Classement pilotes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="classement-ecuries.html" title="Classement écuries">Classement écuries</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="pilotes/effectif.html" title="Pilotes F1">Pilotes F1</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="ecuries/effectif.html" title="Écuries">Écuries</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="circuits/liste.html" title="Circuits">Circuits</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="2014/resultats.html" title="Saison 2014">Saison 2014</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="2013/resultats.html" title="Saison 2013">Saison 2013</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="2012/resultats.html" title="Saison 2012">Saison 2012</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="palmares-pilotes.html" title="Palmarès">Palmarès</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                                    
                    	 <li class="wide">
	<dl class="last">
		<span><a href="2015/directs/gp-d-australie/course.html" title="">Prochain Grand Prix</a></span>
		<dd>
			<h2>GP d'Australie<span></span></h2>
			<time>du 13 au 15 mars</time>
			<div class="tc">
				<a href="2015/directs/gp-d-australie/course.html" title="">
														<img data-src="http://cdn.sports.fr//images/sportsdatas/circuit/logo/7/albert-park/Albert-Park_scale290.png" alt="GP d'Australie">
								</a>
			</div>
		</dd>
	</dl>
</li>
                    
                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L2YxL2FydGljbGVzL2dwLWF1c3RyYWxpZS1tZXJjZWRlcy1sb2luLWRldmFudC0xMTk2Nzg0", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Mercedes, loin devant
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/f1/articles/gp-australie-mercedes-loin-devant/rosberg/14048597-1-fre-FR/Rosberg_w160.jpg">
                <p>Les deux premières séances d’essais libres de la saison, disputées ce vendredi en Australie, ont...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-automoto">
        <a name="automoto"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../auto-moto/rallyes-wrc/index.html" title="Rallyes WRC">Rallyes WRC</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../auto-moto/rallyes/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../auto-moto/rallyes/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/rallyes/classementpilotes.html" title="Classement pilotes">Classement pilotes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/rallyes/classementconstructeurs.html" title="Classement const.">Classement const.</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/rallyes/pilotes/liste.html" title="Pilotes">Pilotes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/rallyes/voitures/liste.html" title="Écuries">Écuries</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/rallyes/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/rallyes/2013/resultats.html" title="Résultats 2013">Résultats 2013</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../auto-moto/moto/index.html" title="MotoGP">MotoGP</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../auto-moto/moto/resultats.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../auto-moto/moto/calendrier.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/moto/classement-motogp.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/moto/pilotes/motogp.html" title="Pilotes">Pilotes</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/moto/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../auto-moto/moto/resultats-moto2.html" title="Moto2">Moto2</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../auto-moto/moto/resultats-moto2.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../auto-moto/moto/calendrier-moto2.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/moto/classement-moto2.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../auto-moto/moto/resultats-moto3.html" title="Moto3">Moto3</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            	                                                <a class="ib" href="../auto-moto/moto/resultats-moto3.html" title="Résultats">Résultats</a>
	                                                /
	                                                <a class="ib" href="../auto-moto/moto/calendrier-moto3.html" target="_self" title="Calendrier">Calendrier</a>
	                                            	    
	                                            	                                        	                                                                        
																		

                                                                                                        </dd>
                                                                                                                                                                    
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/moto/classement-moto3.html" title="Classement">Classement</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../auto-moto/dakar/index.html" title="Dakar">Dakar</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/etapes.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/resultats/autos/classement-general.html" title="Général Autos">Général Autos</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/resultats/motos/classement-general.html" title="Général Motos">Général Motos</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/resultats/quads/classement-general.html" title="Général Quads">Général Quads</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/resultats/camions/classement-general.html" title="Général Camions">Général Camions</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/carte.html" title="Carte">Carte</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/resultats/2013/autos/classement-general.html" title="Dakar 2013">Dakar 2013</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../auto-moto/dakar/autos/palmares.html" title="Palmarès">Palmarès</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../auto-moto/24-heures-du-mans/index.html" title="24h du Mans">24h du Mans</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L2F1dG8tbW90by9yYWxseWVzLXdyYy9hcnRpY2xlcy9vZ2llci1hLWRlamEtZmFpdC1sZS10cm91LSEtMTE5NDU1Mw==", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Ogier a déjà fait le trou !
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/auto-moto/rallyes-wrc/scans/mexique-ogier-realise-le-triple/ogier/14029187-1-fre-FR/Ogier_w160.jpg">
                <p>Sébastien Ogier a survolé le rallye du Mexique ce week-end au volant de sa Polo, s’imposant du c...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-ski">
        <a name="ski"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../ski/calendrier-messieurs.html" title="Ski alpin M">Ski alpin M</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../ski/calendrier-dames.html" title="Ski alpin D">Ski alpin D</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../biathlon/calendrier-messieurs.html" title="Biathlon M">Biathlon M</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../biathlon/calendrier-dames.html" title="Biathlon D">Biathlon D</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../combine-nordique/calendrier.html" title="Combiné">Combiné</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../ski/2013/calendrier/championnat-du-monde-ski-nordique.html" title="Mondiaux nordique">Mondiaux nordique</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L3NraS9iaWF0aGxvbi9hcnRpY2xlcy9mb3VyY2FkZS1wb3VyLW11ZmZhdC12YXN0aW5lLWV0LWFydGhhdWQtMTE5NjY0Mw==", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Fourcade: "A cœur de bien faire pour Alexis, Camille et Florence"
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/ski/biathlon/articles/mondiaux-fourcade-avait-a-coeur-de-bien-faire-pour-alexis-camille-et-florence/martin-fourcade/14047324-1-fre-FR/Martin-Fourcade_w160.jpg">
                <p>Sacré une nouvelle fois champion du monde de l’individuel aux Mondiaux de Kontiolahti, en Finlan...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-natation">
        <a name="natation"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../natation/championnats-d-europe/calendrier.html" title="Europe 2014">Europe 2014</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/championnats-d-europe/calendrier.html" title="Calendrier">Calendrier</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/championnats-d-europe/recap.html" title="Résultats">Résultats</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/championnats-d-europe/medailles.html" title="Tableau des médailles">Tableau des médailles</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="http://www.sports.fr/records/records-du-monde-hommes.html" title="Records Messieurs">Records Messieurs</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-du-monde-hommes.html" title="Monde">Monde</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-olympiques-hommes.html" title="Olympique">Olympique</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-d-europe-hommes.html" title="Europe">Europe</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-de-france-hommes.html" title="France">France</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../natation/records/records-du-monde-femmes.html" title="Records Dames">Records Dames</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-du-monde-femmes.html" title="Monde">Monde</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-olympiques-femmes.html" title="Olympique">Olympique</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-d-europe-hommes.html" title="Europe">Europe</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../natation/records/records-d-europe-femmes.html" title="France">France</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L25hdGF0aW9uL2FydGljbGVzL25hdGF0aW9uLWNhbWlsbGUtbXVmZmF0LXNlcy1wbHVzLWJlbGxlcy12aWN0b2lyZXMtMTE5NTQ3OA==", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Muffat, pour l’éternité
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/natation/articles/palmares-2012-camille-muffat/camille-muffat/4530802-1-fre-FR/Camille-Muffat_w160.jpg">
                <p>A tout jamais, elle restera gravée dans nos mémoires. Décédée lundi en Argentine, lors d’un cras...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-autres">
        <a name="autres"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="../volley/index.html" title="Volley">Volley</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../volley/ligue-a/resultats.html" title="Ligue A">Ligue A</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../volley/ligue-des-champions/resultats.html" title="LDC">LDC</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../volley/championnat-du-monde-hommes/calendrier.html" title="Mondial (H)">Mondial (H)</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../golf/index.html" title="Golf">Golf</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../golf/european/calendrier.html" title="Circuit Européen">Circuit Européen</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../golf/pga/calendrier.html" title="PGA Tour">PGA Tour</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../golf/pga/classement-mondial.html" title="Classement Mondial">Classement Mondial</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../boxe/index.html" title="Boxe">Boxe</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../boxe/detenteurs/ibf.html" title="IBF">IBF</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../boxe/detenteurs/wba.html" title="WBA">WBA</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../boxe/detenteurs/wbc.html" title="WBC">WBC</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../boxe/detenteurs/wbo.html" title="WBO">WBO</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../boxe/detenteurs/europe.html" title="Europe">Europe</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../boxe/detenteurs/france.html" title="France">France</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../escrime/index.html" title="Escrime">Escrime</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../athletisme/index.html" title="Athlétisme">Athlétisme</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../athletisme/championnats-d-europe/calendrier.html" title="Europe 2014">Europe 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../athletisme/2013/championnats-du-monde/recap.html" title="Mondiaux 2013">Mondiaux 2013</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../athletisme/2013/championnats-d-europe-en-salle/calendrier.html" title="Euro salle 2013">Euro salle 2013</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../athletisme/records/records-du-monde-hommes.html" title="Records">Records</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../judo/index.html" title="Judo">Judo</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../judo/2014/championnats-du-monde/calendrier.html" title="Mondiaux 2014">Mondiaux 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../prolongations/index.html" title="Prolongations">Prolongations</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                                                
                            </li>
                            <li>
                        						
						                        <dl>
                            <dt>
                                <a href="../voile/index.html" title="Voile">Voile</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../voile/route-du-rhum/index.html" title="Route du Rhum">Route du Rhum</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../voile/vendee-globe/index.html" title="Vendée Globe">Vendée Globe</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../voile/coupe-de-l-america/index.html" title="Coupe de l'America">Coupe de l'America</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../hockey/ligue-magnus/resultats.html" title="Hockey">Hockey</a>
                            </dt>

                            
                                                            
                                <dd>
                                                                                                            
                                    
                                    									
					                    	                                        	                                            <a href="../hockey/championnat-du-monde/2014/resultats.html" title="Mondial 2014">Mondial 2014</a>
	                                        	                                                                        
																		

                                                                                                        </dd>
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../jo-2014/index.html" title="Sotchi 2014">Sotchi 2014</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            
            
        
        
    </div>

                
    <div class="nav-window sub-nav-poker">
        <a name="poker"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="http://www.sports.fr/poker/emptty" title="Empty">Empty</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            <div class="nav-supp">
    <div>
        <ol>
            
            <li data-link='{"url": "L3Bva2VyL2FydGljbGVzL2V1cm9wZWFuLXBva2VyLXRvdXItZGVhdXZpbGxlLWNyZXB1c2N1bGUtc2Fucy1ldG9pbGUtMTE4MTQ5MQ==", "target": ""}' class="a">
                <span>À la une</span>
                <h2>
Deauville, crépuscule sans étoile
</h2>
                <img width="160" alt="" src="../../cdn.sports.fr/images/media/poker/articles/european-poker-tour-deauville-crepuscule-sans-etoile/finale-deauville/13909709-1-fre-FR/Finale-Deauville_w160.jpg">
                <p>Alors que l’European Poker Tour pourrait ne plus passer par Deauville, où l’affluence a chuté, l...</p>
            </li>

                    </ol>
    </div>
</div>
            
        
        
    </div>

                
    <div class="nav-window sub-nav-services">
        <a name="services"></a>

        <div>
            <ul>
                <li>
                                            						
						                        <dl>
                            <dt>
                                <a href="http://shopping.sports.fr/" title="Shopping">Shopping</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../services/mobile" title="Mobile">Mobile</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                                    						
						                        <dl>
                            <dt>
                                <a href="../../forum.sports.fr/index.html" title="Forum">Forum</a>
                            </dt>

                            
                            
                                                    </dl>
                        
                                                            </li>

                            </ul>
        </div>
        
        
            
            
            
        
        
    </div>

        

	



		<div id="banner-full">
			<div id="ad-megaban2" class="box-ad"></div>
		</div><!-- #banner-full -->
		
		<div id="ad-habillage-flash" class="box-ad noAds"></div>
		<div id="content">
		
			
			
			<div class="trunk">
<div id="col1" class="col c1 c-first">
	<article id="main-content" style="position: relative;">
		<!--ZONES-->
	
	

		
		

<div class="nwTable">
	<img alt="" class="nwLogo" src="images/70/logo-F1.gif">

	<h1>Classement Ecuries<span> Formule 1 - Saison 2015</span></h1>

	<table cellspacing="0" cellpadding="1" border="0" width="100%" class="nwGrandPrix">
		<colgroup>
			<col width="1%">
			<col width="49%">
			<col width="5%">
			<col width="5%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
							<col width="2%">
					</colgroup>

		<thead>
			<tr>
				<td colspan="4" class="br"></td>
																			<td class="tc bt altv">
						<a href="2015/directs/gp-d-australie/course.html">
												<img src='images/GrandPrix/noms/aus.png'  width='15' height='75' alt='GP d'Australie'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-malaisie/course.html">
												<img src='images/GrandPrix/noms/mas.png'  width='15' height='75' alt='GP de Malaisie'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-chine/course.html">
												<img src='images/GrandPrix/noms/chn.png'  width='15' height='75' alt='GP de Chine'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-bahrein/course.html">
												<img src='images/GrandPrix/noms/brn.png'  width='15' height='75' alt='GP de Bahreïn'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-espagne/course.html">
												<img src='images/GrandPrix/noms/spa.png'  width='15' height='75' alt='GP d'Espagne'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-monaco/course.html">
												<img src='images/GrandPrix/noms/mon.png'  width='15' height='75' alt='GP de Monaco'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-canada/course.html">
												<img src='images/GrandPrix/noms/can.png'  width='15' height='75' alt='GP du Canada'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-autriche/course.html">
												<img src='images/GrandPrix/noms/aut.png'  width='15' height='75' alt='GP d'Autriche'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-grande-bretagne/course.html">
												
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-allemagne/course.html">
												<img src='images/GrandPrix/noms/ger.png'  width='15' height='75' alt='GP d'Allemagne'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-hongrie/course.html">
												<img src='images/GrandPrix/noms/hun.png'  width='15' height='75' alt='GP de Hongrie'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-belgique/course.html">
												<img src='images/GrandPrix/noms/bel.png'  width='15' height='75' alt='GP de Belgique'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-italie/course.html">
												<img src='images/GrandPrix/noms/ita.png'  width='15' height='75' alt='GP d'Italie'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-singapour/course.html">
												<img src='images/GrandPrix/noms/sin.png'  width='15' height='75' alt='GP de Singapour'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-japon/course.html">
												<img src='images/GrandPrix/noms/jpn.png'  width='15' height='75' alt='GP du Japon'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-russie/course.html">
												<img src='images/GrandPrix/noms/rus.png'  width='15' height='75' alt='GP de Russie'/>
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-des-etats-unis/course.html">
												<img src='images/GrandPrix/noms/usa.png'  width='15' height='75' alt='GP des Etats-Unis'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-mexique/course.html">
												
						</a>
					</td>
																			<td class="tc bt altv">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-bresil/course.html">
												<img src='images/GrandPrix/noms/bra.png'  width='15' height='75' alt='GP du Brésil'/>
						</a>
					</td>
																			<td class="tc bt ">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-abu-dhabi/course.html">
												<img src='images/GrandPrix/noms/uae.png'  width='15' height='75' alt='GP d'Abu Dhabi'/>
						</a>
					</td>
							</tr>
			<tr class="bl br">
				<th colspan="3">Grand Prix</th>
				<th class="tc">Tot.</th>

																								<th class="tc">
						<a href="2015/directs/gp-d-australie/course.html">
													<img  class="vm" alt="Australie" src="../../cdn.sports.fr/images/sportsdatas/country/logo/0/aus/AUS_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-malaisie/course.html">
													<img  class="vm" alt=" Malaisie" src="../../cdn.sports.fr/images/sportsdatas/country/logo/8/mas/MAS_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-chine/course.html">
													<img  class="vm" alt=" Chine" src="../../cdn.sports.fr/images/sportsdatas/country/logo/0/chn/CHN_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-bahrein/course.html">
													<img  class="vm" alt=" Bahreïn" src="../../cdn.sports.fr/images/sportsdatas/country/logo/4/brn/BRN_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-espagne/course.html">
													<img  class="vm" alt="Espagne" src="../../cdn.sports.fr/images/sportsdatas/country/logo/4/spa/SPA_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-monaco/course.html">
													<img  class="vm" alt=" Monaco" src="../../cdn.sports.fr/images/sportsdatas/country/logo/0/mon/MON_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-canada/course.html">
													<img  class="vm" alt=" Canada" src="../../cdn.sports.fr/images/sportsdatas/country/logo/6/can/CAN_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-autriche/course.html">
													<img  class="vm" alt="Autriche" src="../../cdn.sports.fr/images/sportsdatas/country/logo/1/aut/AUT_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-grande-bretagne/course.html">
													<img  class="vm" alt=" Grande Bretagne" src="../../cdn.sports.fr/images/sportsdatas/country/logo/7/gbr/GBR_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-allemagne/course.html">
													<img  class="vm" alt="Allemagne" src="../../cdn.sports.fr/images/sportsdatas/country/logo/8/ger/GER_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-hongrie/course.html">
													<img  class="vm" alt=" Hongrie" src="../../cdn.sports.fr/images/sportsdatas/country/logo/9/hun/HUN_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-belgique/course.html">
													<img  class="vm" alt=" Belgique" src="../../cdn.sports.fr/images/sportsdatas/country/logo/7/bel/BEL_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-italie/course.html">
													<img  class="vm" alt="Italie" src="../../cdn.sports.fr/images/sportsdatas/country/logo/5/ita/ITA_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-singapour/course.html">
													<img  class="vm" alt=" Singapour" src="../../cdn.sports.fr/images/sportsdatas/country/logo/1/sin/SIN_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-japon/course.html">
													<img  class="vm" alt=" Japon" src="../../cdn.sports.fr/images/sportsdatas/country/logo/3/jpn/JPN_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-de-russie/course.html">
													<img  class="vm" alt=" Russie" src="../../cdn.sports.fr/images/sportsdatas/country/logo/5/rus/RUS_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-des-etats-unis/course.html">
													<img  class="vm" alt="s Etats-Unis" src="../../cdn.sports.fr/images/sportsdatas/country/logo/3/usa/USA_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-mexique/course.html">
													<img  class="vm" alt=" Mexique" src="../../cdn.sports.fr/images/sportsdatas/country/logo/3/mex/MEX_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-du-bresil/course.html">
													<img  class="vm" alt=" Brésil" src="../../cdn.sports.fr/images/sportsdatas/country/logo/5/bra/BRA_scale1510.png">
												</a>
					</th>
																								<th class="tc">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/2015/directs/gp-d-abu-dhabi/course.html">
													<img  class="vm" alt="Abu Dhabi" src="../../cdn.sports.fr/images/sportsdatas/country/logo/9/uae/UAE_scale1510.png">
												</a>
					</th>
							</tr>
		</thead>

		<tbody>
																	<tr class="alt">
						<td class="tr bl">
							<b>1</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/lotus.html">Lotus</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>2</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/force-india.html">Force India</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>3</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/ferrari.html">Ferrari</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>4</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/williams.html">Williams</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>5</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/manor.html">Manor</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b></b></td>
													
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>6</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/mclaren.html">McLaren</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>7</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/toro-rosso.html">Toro Rosso</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b></b></td>
													
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>8</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/sauber.html">Sauber</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>9</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/red-bull.html">Red Bull</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>10</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/mercedes.html">Mercedes</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b>0</b></td>
													
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																				
															<td class="tc ">0</td>
																		</tr>
														<tr class="alt">
						<td class="tr bl">
							<b>11</b>
						</td>
						<td nowrap="">
							<strong><a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/caterham.html">Caterham</a></strong>
						</td>
						<td>
						
						</td>
						<td class="tc classAuto"><b></b></td>
													
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																				
																		</tr>
									</tbody>
	</table>
</div>

		<!--ZONES-->
	
		<div class="node" style="padding: 20px 0 0; text-align: center;">
			<SCRIPT LANGUAGE="JavaScript1.1" SRC="http://ww392.smartadserver.com/call/adj/116590/1785629/Newsweb_SPS.betclic/0x0/[timestamp]/no?[countgo]"></SCRIPT>
			<NOSCRIPT>
				<a href="http://ww392.smartadserver.com/call/jumpi/116590/1785629/Newsweb_SPS.betclic/0x0/[timestamp]/no?" target="_blank">
					<img src="http://ww392.smartadserver.com/call/adi/116590/1785629/Newsweb_SPS.betclic/0x0/[timestamp]/no?" border="0">
				</a>
			</NOSCRIPT>
		</div>
	

	<!--
<div class="OUTBRAIN" data-src="DROP_PERMALINK_HERE" data-widget-id="CB_1" data-ob-template="sportsfr" ></div>
	<script type="text/javascript" src="http://widgets.outbrain.com/outbrain.js"></script> 
	
	<script type="text/javascript">
		$(".ob_container_recs a").live("click", function(){
		_gaq.push(['_trackEvent', 'Oubtrain', 'Clic',,, false]);  
		 });
	</script>
-->

	<div id="taboola-below-article-thumbnails-data"></div>
<script type="text/javascript">
	window._taboola = window._taboola || [];
	_taboola.push({ 
		mode: 'thumbnails-a', 
		container: 'taboola-below-article-thumbnails-data', 
		placement: 'Below Article Thumbnails Data', 
		target_type: 'mix' 
	});
</script>


	
	<!-- Annonces google -->
	<script type="text/javascript">
		var google_ad_channel = '1606716272',
			google_num_ads = 2,
			google_max_num_ads = 2;
			google_Id = 'ad-google-adsense-650';
			google_class = 'box-google-space';
	</script>
	<script src="../../cdn.sports.fr/includes/cobrand/default/js/libs/ads-google-adsense.js?1" type="text/javascript"></script>
	<script language="JavaScript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
	<!-- /Annonces google -->
	


	</article><!-- main-content -->
</div><!-- col1 -->
<aside id="col2" class="col c2">
	<div id="ad-rec-bet1" class="node"></div>	
	
		                        <!--HTML -->
            
    
    

                        <!--Scanner -->
            
	
	


<section class="box box-scan">
	<div class="box-content">
		<span id="popupSwitch" class="ico i-pop"></span>
	    <ul class="tabs tabs-s2">
	        <li class="tab tab-scan tab-active"><a href="classement-ecuries.html" class="tab-link"><span><b>Scan</b></span></a></li><!--
	        --><li class="tab tab-fb"><a href="classement-ecuries.html" class="tab-link"><span><b>Facebook</b></span></a></li>
	    </ul>
	    <div class="tabs-content">
	        <div class="box-tabs">
	            <div class="pagine">
			        <div class="pagine-content">
			        	        <!--
                                            --><ul class="scan">
            
            <li data-vr-contentbox="">
                <a href="scans/gp-australie-libres-2-rosberg-encore-devant-1196767/index.html">
                    

                    GP Australie-Libres 2: Rosberg encore devant 
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="scans/gp-australie-libres-1-les-mercedes-devant-1196754/index.html">
                    

                    GP Australie-Libres 1: Les Mercedes devant 
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/de-tout-petits-progres-pour-bianchi-1195573/index.html">
                    

                    &quot;De tout petits progrès&quot; pour Bianchi
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/alonso-espere-debuter-en-malaisie-1195384/index.html">
                    

                    Alonso espère débuter en Malaisie
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/merhi-roulera-avec-manor-1195181/index.html">
                    

                    Merhi roulera avec Manor
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/manor-confirme-son-inscription-pour-2015-1192638/index.html">
                    

                    Manor confirme son inscription pour 2015
                </a>
            </li>

            
                                
            <li class="hot" data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/mclaren-alonso-prive-du-gp-d-australie-1192047/index.html">
                    

                    McLaren: Alonso privé du GP d’Australie
                </a>
            </li>

                            </ul><!--
            
                                                --><ul class="scan">
            
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/le-fils-de-schumi-en-f4-1191823/index.html">
                    

                    Le fils de Schumi en F4
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-bottas-finit-en-beaute-1191254/index.html">
                    

                    Essais Barcelone: Bottas finit en beauté
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-mercedes-garde-les-devants-1190774/index.html">
                    

                    Essais Barcelone: Mercedes garde les devants
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/Ca-sent-bon-pour-manor-1190404/index.html">
                    

                    Ça sent bon pour Manor
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-rosberg-accelere-1190370/index.html">
                    

                    Essais Barcelone: Rosberg accélère
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/grosjean-c-est-alonso-qui-a-pris-toute-l-energie-du-choc-1190328/index.html">
                    

                    Grosjean: &quot;C'est Alonso qui a pris toute l'énergie du choc&quot;
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/mclaren-alonso-je-vais-parfaitement-bien-1190253/index.html">
                    

                    Alonso: &quot;Je vais parfaitement bien&quot;
                </a>
            </li>

                            </ul><!--
            
                                                --><ul class="scan">
            
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-massa-le-plus-rapide-probleme-pour-button-1189932/index.html">
                    

                    Essais Barcelone: Massa le plus rapide, problème pour Button
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/alonso-incertain-pour-l-australie-1189782/index.html">
                    

                    Alonso incertain pour l'Australie
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/la-fia-va-enqueter-sur-l-accident-d-alonso-1189412/index.html">
                    

                    La FIA va enquêter sur l’accident d’Alonso
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/manor-stevens-pour-premier-pilote-1189310/index.html">
                    

                    Manor: Stevens pour premier pilote
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/les-schumacher-se-separent-de-leur-chalet-norvegien-1189296/index.html">
                    

                    Les Schumacher se séparent de leur chalet norvégien
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/alonso-est-sorti-de-l-hopital-1189262/index.html">
                    

                    Alonso est sorti de l’hôpital
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/mclaren-aucune-preuve-de-defaillance-mecanique-1188578/index.html">
                    

                    McLaren: &quot;Aucune preuve de défaillance mécanique&quot;
                </a>
            </li>

                            </ul><!--
            
                                                --><ul class="scan">
            
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-grosjean-roi-du-week-end-1188010/index.html">
                    

                    Essais Barcelone: Grosjean roi du week-end
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/et-si-alonso-s-etait-electrocute-1187974/index.html">
                    

                    Et si Alonso s'était électrocuté ?
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/vettel-alonso-a-tourne-a-droite-dans-le-mur-1187887/index.html">
                    

                    Vettel: &quot;Alonso a tourné à droite dans le mur&quot;
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-mclaren-trime-encore-1187487/index.html">
                    

                    Essais Barcelone: McLaren trime encore
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-ricciardo-devant-alonso-a-tourne-1187029/index.html">
                    

                    Essais Barcelone: Ricciardo devant, Alonso a tourné
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/grosjean-fait-du-velo-1186976/index.html">
                    

                    Grosjean fait du vélo...
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/essais-barcelone-hamilton-malade-mclaren-aussi-1186773/index.html">
                    

                    Essais Barcelone: Hamilton malade, McLaren aussi...
                </a>
            </li>

                            </ul><!--
            
                                                --><ul class="scan">
            
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/marussia-repart-sous-manor-f1-1186487/index.html">
                    

                    Marussia repart sous Manor F1
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/williams-wolff-au-volant-jeudi-1186004/index.html">
                    

                    Williams: Wolff au volant jeudi
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/ferrari-doublee-par-lego-1185493/index.html">
                    

                    Ferrari doublée par... Lego
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/m.-verstappen-je-suis-tres-experimente-1184828/index.html">
                    

                    M. Verstappen: &quot;Je suis très expérimenté&quot;
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/mclaren-vise-la-victoire-a-court-terme-1181988/index.html">
                    

                    McLaren vise la victoire &quot;à court terme&quot;
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/lewis-hamilton-avec-kanye-west-1181601/index.html">
                    

                    Lewis Hamilton avec Kanye West
                </a>
            </li>

            
                                
            <li data-vr-contentbox="">
                <a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/mclaren-la-frustration-d-alonso-1181482/index.html">
                    

                    McLaren: La frustration d'Alonso
                </a>
            </li>

                            </ul><!--
            
                            -->
    
					</div>
	                <div class="more">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/scans/index.html">Plus de scans</a>
	                </div>
	                <a href="../rss/rss.html" class="ico i-rss"></a>
	            </div>
	        </div>
			<div class="box-tabs">
				<fb:recommendations site="sports.Fr" width="280" height="280" header="false" font="" border_color="#FFFFFF"></fb:recommendations>
			</div>
	    </div>
	</div>
</section><!-- Scan + others -->
                    <!--HTML -->
            
    
    <div id="ad-rectangle1" class="box box-nod box-ad"></div>

                        <!--LiveScore -->
            
<div id="nw-wg-livescore">
		<div class="nw-inner"> 
				
                	<h2><span>Live</span> scores</h2>
                
                
	
		<iframe src="http://ww392.smartadserver.com/call/adif/116590/1785513/Newsweb_SPS.betclic/286x85/" width="286" height="85" marginwidth="0" marginheight="0" hspace="0" vspace="0" frameborder="0" scrolling="no"></iframe>
	

                <dl class="nw-lv1">
                                                                                                                                                                                				                 
					                                
                                                                                        
                                                                                                                                                                                        <dt class="nw-moins"><strong>Tennis</strong></dt>
                                <dd class="nw-tennis">
                                        <dl class="nw-lv2">
                                                                								                                  

                                                                                                                        <dt class="nw-moins">Tournoi d'Indian Wells </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																															<li class="">
    <a href="../tennis/directs/tournoi-d-indian-wells/livescore.html">
        <span class="nw-horaire">19:00</span>
        <span class="nw-eq">
            <em>Dolgopolov </em>
            <em>Dancevic </em>
        </span>
        <span class="nw-score">
            <em></em>
            <em></em>
            <em></em>
            <em></em>
            <em></em>
        </span>
        <span class="nw-state"></span>
    </a>

            
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



    
    
</li>																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																															<li class="">
    <a href="../tennis/directs/tournoi-d-indian-wells/livescore.html">
        <span class="nw-horaire">22:00</span>
        <span class="nw-eq">
            <em>Fish </em>
            <em>Harrison </em>
        </span>
        <span class="nw-score">
            <em>4 6</em>
            <em>6 4</em>
            <em>6 7</em>
            <em></em>
            <em></em>
        </span>
        <span class="nw-state"></span>
    </a>

    
    
</li>																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																															<li class="">
    <a href="../tennis/directs/tournoi-d-indian-wells/livescore.html">
        <span class="nw-horaire">03:00</span>
        <span class="nw-eq">
            <em>Williams </em>
            <em>Niculescu </em>
        </span>
        <span class="nw-score">
            <em></em>
            <em></em>
            <em></em>
            <em></em>
            <em></em>
        </span>
        <span class="nw-state"></span>
    </a>

            
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



    
    
</li>																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																															<li class="">
    <a href="../tennis/directs/tournoi-d-indian-wells/livescore.html">
        <span class="nw-horaire">19:00</span>
        <span class="nw-eq">
            <em>Riske </em>
            <em>Radwanska </em>
        </span>
        <span class="nw-score">
            <em></em>
            <em></em>
            <em></em>
            <em></em>
            <em></em>
        </span>
        <span class="nw-state"></span>
    </a>

            
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



    
    
</li>																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                
                                                                                        
                                                                                                                                
                                                                                                        	
									<li class=" nw-directs">
			
				<a href="../tennis/directs/tournoi-d-indian-wells/livescore.html">
					
					
					
					<span class="nw-eq"><em>Multiplex Tournoi d'Indian Wells </em></span><span class="nw-state"></span>
				</a>
				
				
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>
		                                                                                                 												                                        
																								</ul>
											</dd>
											</dl><!--lv2-->
																					                                                                                                        <dt class="nw-moins"><strong>Formule 1</strong></dt>
                                <dd class="nw-formule1">
                                        <dl class="nw-lv2">
                                                                								                                  

                                                                                                                        <dt class="nw-moins">GP d'Australie </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																															<li class="">
	<div class="nw-live-title">	
		<a href="2015/directs/gp-d-australie/essais-libres-1.html"><em>Essais libres 1 à 02:30</em></a>
	</div>
	
	<span class="nw-state"></span>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



	<!--	<a href="/f1/2015/directs/gp-d-australie/essais-libres-1.html" class="nw-comment">Détails</a>-->
</li>
																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																															<li class="">
	<div class="nw-live-title">	
		<a href="2015/directs/gp-d-australie/essais-libres-2.html"><em>Essais libres 2 à 06:30</em></a>
	</div>
	
	<span class="nw-state"></span>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



	<!--	<a href="/f1/2015/directs/gp-d-australie/essais-libres-2.html" class="nw-comment">Détails</a>-->
</li>
																			 
                                                                                                                                                                                                                                									 
					                                
                                                                                        
                                                                                                                                
                                                                                                        <!--<div class="more"><a href="/rugby/directs/2015/top-14/10740/clermont-bordeaux-begles.html">Tous les directs</a></div>-->                                                                                                												                                        
																								</ul>
											</dd>
											</dl><!--lv2-->
																					                                                                                                        <dt class="nw-moins"><strong>Rugby</strong></dt>
                                <dd class="nw-rugby">
                                        <dl class="nw-lv2">
                                                                								                                  

                                                                                                                        <dt class="nw-moins">Top 14 </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																																<li class="">
				<a href="../rugby/directs/2015/top-14/10740/clermont-bordeaux-begles.html">
		
			<span class="nw-horaire">20:45</span> 
			<span class="nw-eq">
				<em>Clermont</em>
				<em>Bordeaux-Bègles</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



				<a href="../rugby/directs/2015/top-14/10740/clermont-bordeaux-begles.html" class="nw-comment">Live Texte</a>
		</li>


																			 
                                                                                                                                                                                                                                									 
					                                
                                                                                        
                                                                                                                                
                                                                                                                                                                                                         												                                        
																								</ul>
											</dd>
											</dl><!--lv2-->
																					                                                                                                        <dt class="nw-moins"><strong>Basket</strong></dt>
                                <dd class="nw-basket">
                                        <dl class="nw-lv2">
                                                                								                                  

                                                                                                                        <dt class="nw-moins">Pro A </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																																<li class="">
				<a href="../basket/directs/pro-a/livescore.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Le Havre</em>
				<em>Orléans</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                  

                                                                                                                                                							    
                                                                                                                                                                                                                                 
                                                </ul>
                                        </dd>
                                                                                                                        <dt class="nw-moins">Euroligue Hommes </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                
                                                                                        
                                                                                                                                
                                                                                                                                                                                                         												                                        
																								</ul>
											</dd>
											</dl><!--lv2-->
																					                                                                                                        <dt class="nw-moins"><strong>Football</strong></dt>
                                <dd class="nw-football">
                                        <dl class="nw-lv2">
                                                                								                                  

                                                                                                                        <dt class="nw-moins">Ligue 1 </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-1/monaco-bastia.html">
		
			<span class="nw-horaire">20:30</span> 
			<span class="nw-eq">
				<em>Monaco</em>
				<em>Bastia</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



				<a href="../football/directs/ligue-1/monaco-bastia.html" class="nw-comment">Live Texte</a>
		</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-1/nice-guingamp.html">
		
			<span class="nw-horaire">20:30</span> 
			<span class="nw-eq">
				<em>Nice</em>
				<em>Guingamp</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



				<a href="../football/directs/ligue-1/nice-guingamp.html" class="nw-comment">Live Texte</a>
		</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                  

                                                                                                                                                							    
                                                                	
									<li class=" nw-directs">
			
				<a href="../football/directs/ligue-1/livescore.html">
					
					
					
					<span class="nw-eq"><em>Multiplex Ligue 1 </em></span><span class="nw-state"></span>
				</a>
				
				
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>
		                                                                                                                                                                 
                                                </ul>
                                        </dd>
                                                                                                                        <dt class="nw-moins">Ligue 2 </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Clermont</em>
				<em>Dijon</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Creteil</em>
				<em>Angers</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Ajaccio GFCO</em>
				<em>Nancy</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Laval</em>
				<em>Nimes</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Le Havre</em>
				<em>Orleans</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Chateauroux</em>
				<em>Arles-Avignon</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Niort</em>
				<em>Ajaccio</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../football/directs/ligue-2/multiplex.html">
		
			<span class="nw-horaire">20:00</span> 
			<span class="nw-eq">
				<em>Tours</em>
				<em>Brest</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                  

                                                                                                                                                							    
                                                                	
									<li class=" nw-directs">
			
				<a href="../football/directs/ligue-2/livescore.html">
					
					
					
					<span class="nw-eq"><em>Multiplex Ligue 2 </em></span><span class="nw-state"></span>
				</a>
				
				
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>
		                                                                                                                                                                 
                                                </ul>
                                        </dd>
                                                                                                                        <dt class="nw-moins">Allemagne </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																																<li class="">
				<a href="../football/directs/allemagne/livescore.html">
		
			<span class="nw-horaire">20:30</span> 
			<span class="nw-eq">
				<em>Leverkusen</em>
				<em>Stuttgart</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                  

                                                                                                                                                							    
                                                                                                                                                                                                                                 
                                                </ul>
                                        </dd>
                                                                                                                        <dt class="nw-moins">Espagne </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																																<li class="">
				<a href="../football/directs/espagne/livescore.html">
		
			<span class="nw-horaire">20:45</span> 
			<span class="nw-eq">
				<em>FC Valence</em>
				<em>La Corogne</em>
			</span>
			<span class="nw-score">
								<em></em>
				<em></em>
							</span>
			<span class="nw-state"></span>
		</a>
			
	<a rel="nofollow" class="nw-pari" target="_blank" href="http://ww392.smartadserver.com/call/cliccommand/6550844/116590/[timestamp]/[reference]?"><img border="0" src="http://ww392.smartadserver.com/call/adimppixel/6550844/116590/[timestamp]?">Parier</a>



			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                  

                                                                                                                                                							    
                                                                                                                                                                                                                                 
                                                </ul>
                                        </dd>
                                                                                                                        <dt class="nw-moins">National </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																			
																													 
                                                                                                                                                                                                                                									 
									 
					                                
                                                                                        
                                                                                                                                
                                                                                                                                                                                                         												                                        
																								</ul>
											</dd>
											</dl><!--lv2-->
																					                                                                                                        <dt class="nw-moins"><strong>Nba</strong></dt>
                                <dd class="nw-nba">
                                        <dl class="nw-lv2">
                                                                								                                  

                                                                                                                        <dt class="nw-moins">NBA </dt>
                                                                                <dd style="display: block;">
                                                <ul>
                                																																	
                                																																<li class="">
				<a href="../nba/directs/livescore.html">
		
			<span class="nw-horaire">00:00</span> 
			<span class="nw-eq">
				<em>Indiana</em>
				<em>Milwaukee</em>
			</span>
			<span class="nw-score">
								<em>109</em>
				<em>103</em>
							</span>
			<span class="nw-state"></span>
		</a>
			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../nba/directs/livescore.html">
		
			<span class="nw-horaire">00:00</span> 
			<span class="nw-eq">
				<em>Washington</em>
				<em>Memphis</em>
			</span>
			<span class="nw-score">
								<em>107</em>
				<em>87</em>
							</span>
			<span class="nw-state"></span>
		</a>
			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../nba/directs/livescore.html">
		
			<span class="nw-horaire">01:00</span> 
			<span class="nw-eq">
				<em>San Antonio</em>
				<em>Cleveland</em>
			</span>
			<span class="nw-score">
								<em>125</em>
				<em>128</em>
							</span>
			<span class="nw-state"></span>
		</a>
			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../nba/directs/livescore.html">
		
			<span class="nw-horaire">02:00</span> 
			<span class="nw-eq">
				<em>Utah</em>
				<em>Houston</em>
			</span>
			<span class="nw-score">
								<em>109</em>
				<em>91</em>
							</span>
			<span class="nw-state"></span>
		</a>
			</li>


																			 
                                                                                                                                                                                                                                									 
					                                                                								                                																																	
                                																																<li class="">
				<a href="../nba/directs/livescore.html">
		
			<span class="nw-horaire">03:30</span> 
			<span class="nw-eq">
				<em>LA Lakers</em>
				<em>New York</em>
			</span>
			<span class="nw-score">
								<em>94</em>
				<em>101</em>
							</span>
			<span class="nw-state"></span>
		</a>
			</li>


																			 
                                                                                                                                                                                                                                									 
					                                
                                                                                                                                                                                                                        
                                                                                                        	
						                                                                                                 												                                        
																								</ul>
											</dd>
											</dl><!--lv2-->
																					                                                                                                                                </dl><!--lv1-->
                
				                <div class="more"><a href="../livescore/13-03-2015.html">Tous les directs</a></div>
				                
        </div><!-- .nw-inner -->
</div><!-- .nw-wg-livescore-->
                    <!--HTML -->
            
    
    <div id="ad-rectangle2" class="box box-nod box-ad"></div> 

                        <!--Databox -->
            
	<section class="box box-datas databox">
	<header>
		<h2 class="aws-title"><span>Résultats</span> Formule1</h2>
	</header>
	<div class="box-content">
		<ul class="tabs tabs-s1">
			<li class="tab tab-active"><a href="classement-ecuries.html" class="tab-link"><span><b>Class. Pilotes</b></span></a></li><!--
			--><li class="tab"><a href="classement-ecuries.html" class="tab-link"><span><b>Class. Ecuries</b></span></a></li><!--
			--><li class="tab"><a href="classement-ecuries.html" class="tab-link"><span><b>Résultats</b></span></a></li>
		</ul>
		<div class="tabs-content">
	        <div class="box-tabs" style="display: block;">
				
				<div class="tabs-content">					
				    <div class="nwTable nwSep box-tabs" style="display: block;">
	<table class="nwClassement" cellspacing="0">
		<colgroup>
					<col width="5%">
					<col width="45%">
					<col width="25%">
					<col width="15%">
					</colgroup>
		<tbody>
	
												
					<tr class="even">
						<td class="pos">1</td>
						<td class="team">
						 
														<img src='../images/drapeaux/japon.gif'  class='vm'/>
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/pilotes/kamui-kobayashi.html">Kamui Kobayashi</a></td>
						<td class="team">Caterham</td>
						<td class="pts"><b>0</b></td>
						</tr>
					
																
					<tr class="odd">
						<td class="pos">2</td>
						<td class="team">
						 
														<img src='../images/drapeaux/allemagne.gif'  class='vm'/>
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/pilotes/sebastian-vettel.html">Sebastian Vettel</a></td>
						<td class="team">Ferrari</td>
						<td class="pts"><b>0</b></td>
						</tr>
					
																
					<tr class="even">
						<td class="pos">3</td>
						<td class="team">
						 
														<img src='../images/drapeaux/bresil.gif'  class='vm'/>
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/pilotes/felipe-massa.html">Felipe Massa</a></td>
						<td class="team">Williams</td>
						<td class="pts"><b>0</b></td>
						</tr>
					
																
					<tr class="odd">
						<td class="pos">4</td>
						<td class="team">
						 
														<img src='../images/drapeaux/russie.gif'  class='vm'/>
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/pilotes/daniil-kvyat.html">Daniil Kvyat</a></td>
						<td class="team">Red Bull</td>
						<td class="pts"><b>0</b></td>
						</tr>
					
																
					<tr class="even">
						<td class="pos">5</td>
						<td class="team">
						 
														<img src='../images/drapeaux/mexique.gif'  class='vm'/>
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/pilotes/sergio-perez.html">Sergio Perez</a></td>
						<td class="team">Force India</td>
						<td class="pts"><b>0</b></td>
						</tr>
					
																		</tbody>
	</table>
</div>
				<p class="more">
					<a href="classement-pilotes.html">Classement complet</a>
				</p>
				</div>
			</div>
			<div class="box-tabs">
				
				<div class="tabs-content">	
				 <div class="nwTable nwSep box-tabs" style="display: block;">
	<table class="nwClassement" cellspacing="0">
		<colgroup>
					<col width="12%">
					<col width="12%">
					<col width="64%">
					<col width="12%">
					</colgroup>
		<tbody>
	
																																																	
					<tr class="even">
						<td class="pos">7</td>
						<td class="logo">
						</td>
						<td class="team">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/toro-rosso.html">Toro Rosso</a>
						</td>
						<td class="pts"></td>
						</tr>
					
											
					<tr class="odd">
						<td class="pos">8</td>
						<td class="logo">
						</td>
						<td class="team">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/sauber.html">Sauber</a>
						</td>
						<td class="pts">0</td>
						</tr>
					
											
					<tr class="even">
						<td class="pos">9</td>
						<td class="logo">
						</td>
						<td class="team">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/red-bull.html">Red Bull</a>
						</td>
						<td class="pts">0</td>
						</tr>
					
											
					<tr class="odd">
						<td class="pos">10</td>
						<td class="logo">
						</td>
						<td class="team">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/mercedes.html">Mercedes</a>
						</td>
						<td class="pts">0</td>
						</tr>
					
											
					<tr class="even">
						<td class="pos">11</td>
						<td class="logo">
						</td>
						<td class="team">
						<a href="http://lab01.xilopix.net:8084/www.sports.fr/f1/ecuries/caterham.html">Caterham</a>
						</td>
						<td class="pts"></td>
						</tr>
					
									</tbody>
	</table>
</div>					
				<p class="more">
					<a href="classement-ecuries.html">Classement complet</a>
				</p>
				</div>
			</div>
			<div class="box-tabs">
				
				<div class="tabs-content">	
				 <div class="nwTable nwSep box-tabs" style="display: block;">
	<table class="nwClassement" cellspacing="0">
	<colgroup>
	<col width="12%">
	<col width="44%">
	<col width="12%">
	</colgroup>
	<tbody>	
		<tbody>
			<tr class="even">
				<th colspan="3">
					<p align="center"></p>
				</th>
			</tr>
								</tbody>
	</table>
</div>										
				<p class="more">
					<a href="resultats.html">Résultats complets</a>
				</p>
				</div>
			</div>
		</div>
	</div>
</section>
 
                    <!--HTML -->
            
    
    <div class="box"><div class="leguide"><iframe src="http://cshoppingbox.partner.leguide.com/sports/001_accueil.htm" width="300" height="260" frameborder="0" scrolling="no"></iframe></div></div>

                        <!--Reactions -->
            <section class="box box-parlons-sport">
	<header>
		<h2 class="aws-title"><span>Parlons</span> sports</h2>
	</header>
	
	<ul class="tabs tabs-s1">
		<li class="tab tab-active"><a class="tab-link" href="classement-ecuries.html"><span><b>Réactions</b></span></a></li><li class="tab"><a class="tab-link" href="classement-ecuries.html"><span><b>Forum</b></span></a></li>
	</ul>
	

	<div class="tabs-content">
        <div class="box-tabs" style="display: block;">
			<ul class="liste">
							<li class="list-item">
					<div>
						<a href="../cyclisme/articles/fauchee-par-un-spectateur-en-plein-sprint-!-1196831/index.html">bipede</a>
						<br>sur <strong><a href="../cyclisme/articles/fauchee-par-un-spectateur-en-plein-sprint-!-1196831/index.html">Fauchée par un spectateur en plein sprint ! </a></strong>
					</div>
					<p>J'espère qu'ils ont chopé cet abruti .</p>
				</li>
							<li class="list-item">
					<div>
						<a href="../football/ligue-1/scans/discipline-bastia-furiani-suspendu-jusqu-a-nouvel-ordre-1196718/index.html">thebiglebowski</a>
						<br>sur <strong><a href="../football/ligue-1/scans/discipline-bastia-furiani-suspendu-jusqu-a-nouvel-ordre-1196718/index.html">Discipline-Bastia: Furiani suspendu jusqu'à nouvel ordre</a></strong>
					</div>
					<p>Ouais, si on oublie Estrozy...</p>
				</li>
							<li class="list-item">
					<div>
						<a href="../football/ligue-1/scans/le-rendement-d-ibrahimovic-en-question-1196813/index.html">michel1970</a>
						<br>sur <strong><a href="../football/ligue-1/scans/le-rendement-d-ibrahimovic-en-question-1196813/index.html">Ibra, vraiment indispensable au PSG ? </a></strong>
					</div>
					<p>Je n'ai jamais été fan d'Ibra. Bien-sur les 2 années passées quand il claquait buts sur buts j'étais content. Cette année il fait une très mauvaise saison. Je pense que lorsqu'il n'est pas la, les joueurs du PSG se libèrent. Est il indispensable au groupe ? je n'en suis pas sur du tout.</p>
				</li>
							<li class="list-item">
					<div>
						<a href="../football/ligue-des-champions/articles/altercation-fabregas-thiago-motta-a-la-mi-temps-1196732/index.html?features3ligue-des-champions">pixigol</a>
						<br>sur <strong><a href="../football/ligue-des-champions/articles/altercation-fabregas-thiago-motta-a-la-mi-temps-1196732/index.html?features3ligue-des-champions">Altercation Thiago Motta-Fabregas à la mi-temps ?</a></strong>
					</div>
					<p>Merci pour cette leçon d'objectivité</p>
				</li>
						</ul>
			<!-- <div class="more"><a href="">Plus de commentaires</a></div> -->
		</div>
		<div class="box-tabs" style="display: none;">
			<ul class="liste">
							<li class="list-item">
									<a href="../../forum.sports.fr/index.php?showuser=6144"><img width="46" height="46" src="../../forum.sports.fr/uploads/53b1dd56433d32195a33e.gif" alt="" /></a>
								<div>
					<strong>
						<a href="../../forum.sports.fr/index.php?showtopic=13686&amp;view=getlastpost">Nba : Saison 2014/2015</a>
					</strong>
					<p>
						<a href="../../forum.sports.fr/index.php?showtopic=13686&amp;view=getlastpost">Utah est en train de démonter Houston   Utah est sur une bonne série, 4 victoires in a...<span>(45894 lectures)</span></a>
					</p>
				</div>
				</li>
							<li class="list-item">
															<a href="../../forum.sports.fr/index.php?showuser=525"><img width="46" height="46" src="../../forum.sports.fr/uploads/noavatar" /></a>
													<div>
					<strong>
						<a href="../../forum.sports.fr/index.php?showtopic=12941&amp;view=getlastpost">Actu Des Bleus</a>
					</strong>
					<p>
						<a href="../../forum.sports.fr/index.php?showtopic=12941&amp;view=getlastpost">Je pense qu&#39;il sera sélectionné pour le prochain rassemblement>Le truc qui me déran...<span>(73240 lectures)</span></a>
					</p>
				</div>
				</li>
							<li class="list-item">
															<a href="../../forum.sports.fr/index.php?showuser=4945"><img width="46" height="46" src="../../forum.sports.fr/uploads/9f86e58040cdc43810464.jpg" /></a>
													<div>
					<strong>
						<a href="../../forum.sports.fr/index.php?showtopic=13669&amp;view=getlastpost">Ligue Des Champions 2014-2015</a>
					</strong>
					<p>
						<a href="../../forum.sports.fr/index.php?showtopic=13669&amp;view=getlastpost">Je maintiens ce que je dis>A Porto, il beneficiait deja d&#39;un effectif largement sup...<span>(14707 lectures)</span></a>
					</p>
				</div>
				</li>
							<li class="list-item">
															<a href="../../forum.sports.fr/index.php?showuser=4945"><img width="46" height="46" src="../../forum.sports.fr/uploads/9f86e58040cdc43810464.jpg" /></a>
													<div>
					<strong>
						<a href="../../forum.sports.fr/index.php?showtopic=13656&amp;view=getlastpost">Pronos L1 : Saison 2014 - 2015 - Uniquement Les Pronos</a>
					</strong>
					<p>
						<a href="../../forum.sports.fr/index.php?showtopic=13656&amp;view=getlastpost">Monaco - Bastia : 1-0Metz - St Etienne : 0-1Lens - Toulouse : 1-0Lorient - Caen : 1-0Mo...<span>(28762 lectures)</span></a>
					</p>
				</div>
				</li>
						</ul>
			<!-- <div class="more"><a href="">Plus de commentaires</a></div> -->			
		</div>
	</div>
</section><!-- Last Reactions -->                    <!--HTML -->
            
    
    <!-- Annonces google Cover -->
<script type="text/javascript">
	var google_ad_channel = '4110234209',
		google_num_ads = 3,
		google_max_num_ads = 3;
	google_Id = 'ad-google-adsense-300';
	google_class = 'box-google-cover';
</script>
<script src="../../cdn.sports.fr/includes/cobrand/default/js/libs/ads-google-adsense.js" type="text/javascript"></script>
<script language="JavaScript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
<!-- /Annonces google Cover -->



                
	
	<div class="box box-nod box-betclic" style="padding:10px;border: 1px solid #ccc;">
		<p style="margin-bottom: 5px; font-size: 14px;"><a href="../paris-sportifs/betclic/index.html"><strong>Parier sans risque avec Betclic :<br>100€ offerts !</strong></a></p>
		<p style="text-align: justify;">Rejoignez Betclic, le site leader des <a href="https://www.betclic.fr/c/paris-sportifs" target="_blank">paris sportifs</a> en France. 
Un bonus de 100€ est offert à tout nouveau joueur : profitez-en pour <a href="https://www.betclic.fr/c/parier" target="_blank">parier</a> sur le sport (football, tennis, rugby, basket), sur la compétition et le match de votre choix !</p>
	</div>
</aside><!-- side-content -->

							<div class="clear"></div>
							<!-- Bloc promotions services -->
							<div class="box-group box-group-1">
								<section id="promo-services" class="box box-1">
									<header>
										<ul class="breadcrumb">
											<li>Services</li>
										</ul>
									</header>
									<ul>
										<li class="service" data-link='{"url": "aHR0cDovL3Nob3BwaW5nLnNwb3J0cy5mci8=", "target":"_blank"}'>
											<img width="185" border="0" alt="" title="" src="../../cdn.sports.fr/includes/cobrand/default/img/services/shopping.jpg" />
											<strong><a href="http://shopping.sports.fr/" target="_blank">Shopping</a></strong>
											<p>Soldes, réductions exceptionnelles: retrouvez les plus belles offres shopping du moment.</p>
										</li><!--
										--><li class="service" data-link='{"url": "aHR0cDovL3d3dy5zbWFydGFkc2VydmVyLmNvbS9jYWxsL2NsaWNjb21tYW5kLzg1ODI2MDUv", "target":"_blank" }'>
											<img width="185" border="0" alt="" title="" src="../../cdn.sports.fr/includes/cobrand/default/img/services/assurland/footer.jpg" />
											<strong><a href="http://www.smartadserver.com/call/cliccommand/8582605/" target="_blank">Assurance auto</a></strong>
											<p>Comparez 78 offres d'assurance pour auto</p>
										</li><!--
										--><li class="service" data-link='{"url": "aHR0cDovL3d3dy5zcG9ydHMuZnIvc2VydmljZXMvbW9iaWxlLw==", "target":"_blank"}'>
											<img width="185" border="0" alt="" title="" src="../../cdn.sports.fr/includes/cobrand/default/img/services/mobiles.jpg?s" />
											<strong><a href="../services/mobile" target="_blank">Mobile</a></strong>
											<p>Sports.fr sur votre mobile Disponible sur App Store et Google Play.</p>
										</li><!--
										--><li class="service" data-link='{"url": "aHR0cDovL3dlYmR5bi5zcG9ydHMuZnIvL0luc2NyaXB0aW9u", "target":"_blank"}'>
											<img width="185" border="0" alt="" title="" src="../../cdn.sports.fr/includes/cobrand/default/img/services/newsletter.jpg" />
											<strong><a href="../../webdyn.sports.fr/Inscription" target="_blank">Newsletter Sports</a></strong>
											<p>Inscrivez-vous et ne ratez plus rien de l'actu sportive !</p>
										</li>
									</ul>
								</section>
							</div>
							<!-- / Bloc promotions services -->
							
						</div><!-- #content .trunk -->
					</div><!-- #content -->
					
					<footer id="footer">
						<div class="trunk">							
						    <section id="site-info">
						        <h2><a href="http://www.lagardere.com" target="_blank">Les Sites Newsweb</a></h2>
						        <p>
						        	les <a target="_blank" href="http://www.boursier.com/elections/municipales/resultats-2014">résultats des élections municipales 2014</a>,
						        	La <a target="_blank" href="http://www.boursier.com">Bourse</a>, 
						        	le <a target="_blank" href="http://www.boursier.com/indices/cours/cac-40-FR0003500008,FR.html">CAC 40</a> et 
						        	le <a target="_blank" href="http://www.boursier.com/devises">cours des devises</a> avec Boursier.com, 
						        	la <a href="http://www.football.fr/ligue-1" target="_blank">Ligue 1</a>, 
						        	le <a href="http://www.football.fr/psg/" target="_blank">PSG</a> et 
						        	l' <a href="http://www.football.fr/marseille" target="_blank">OM</a> avec football.fr, 
						        	le <a href="http://www.rugbynews.fr" target="_blank">Rugby</a> avec Rugbynews.fr, 
						        	le <a href="http://www.ilovepoker.fr" target="_blank">Poker</a> avec Ilovepoker.fr, 
						        	le <a href="http://www.football-mag.fr" target="_blank">Foot</a> avec Football-mag.fr, 
						        	le <a href="http://www.cyclisme-mag.com" target="_blank">Cyclisme</a> avec Cyclisme-mag.com 
						        </p>
						        <ul class="links">
									<li><a href="../services/contacts/index.html" class="">Contacts</a></li>
									<li><a href="mailto:support@sports.fr">Signaler un contenu illicite</a></li>
									<li><a href="../services/cgu/index.html" class="">CGU</a></li>
									<li><a href="../services/cpu/index.html" class="">CPU</a></li>
									<li><a href="../services/mentions-legales/index.html" class="">Mentions légales</a></li>
									<li><a href="../services/partenaires/index.html" class="">Partenaires</a></li>
									<li><a href="../services/recrutement/index.html" class="">Recrutement</a></li>
								</ul>
						        <p class="copy">&copy; Copyright 2011 Sports.fr. Tous droits réservés. Le Site Sports.fr est édité par Newsweb - Leader d'audience sur la cible masculine - Sites du réseau Sports.fr</p>
						    </section><!-- #site-info -->
						</div><!-- #footer .trunk -->
					</footer><!-- #footer -->
			
		</div><!-- #overall -->
		<script src="../../cdn.sports.fr/includes/cobrand/default/js/la/init-modules.js?s166"></script>
		
			 
<script type="text/javascript">
    if (typeof $LAU !== 'undefined') {
    	$LAU.domReady($LAU.domReadyStack);
    }
    if ($LAU.inQueryUrl('la_console') && $LAU.inQueryUrl('testAds')) {
    	$.extend($.la.promo.formats, $.la.promo.tests[$LAU.inQueryUrl('testAds')]);
    }
</script><script type="text/javascript">
	function siteUnder(cookieName, url, siteName, sport){
		(function(win){
			var cookieValue = $.cookie(cookieName) ? parseInt($.cookie(cookieName), 10) : 0,
				capping = 1,
				expires = 1;
			
			var openWin = function(){
					width = 1020,
					height = 800;
		
				win.open(url, siteName, 'width=' + width + ', height=' + height + ', left=100, top=200, scrollbars=yes, toolbar=no, location=yes, directories=yes, status=yes, menubar=yes, resizable=yes');
				win.focus();
				cookieValue++;
				$.cookie(cookieName, cookieValue, { expires: expires, domain: '.sports.fr', path: '/' });
			};
			
			if (cookieValue < capping) {
				$('a[href*="/'+ sport +'/"]').click(openWin);
				return false;
			}
		})(window);
		//test
	}
</script>











<script type="text/javascript" src="http://cdn-sports.ladmedia.fr/includes/cobrand/default/js/plugins/tc_POCLagardreActive.js?1"></script><div id="ad-habillage"></div><div id="ad-inread"></div><div id="ads-loader" style="overflow: hidden; height: 0;"><div id="ad-megaban2-load"><script language="JavaScript" type="text/javascript">
            ord = (typeof(ord)!="undefined") ? ord : Math.random()*10000000000000000;
            if(ENV.country === 'BE') document.write('<scr'+'ipt language="JavaScript" src="http://ad.doubleclick.net/adj/P4995.SPORTS/OTHER-FR_LEADERBOARD_TOP_MULTI;sz=728x90,468x60,1x1;dcopt=ist;tile=1;lang=fr;pos=top;pgl1=other;kw=[KEYWORD];ord='+ord+'?" type="text/javascript"></scr'+'ipt>');
             else if(ENV.country === 'CH') document.write('<scr'+'ipt language="JavaScript" src="http://www6.smartadserver.com/call/pubj/50984/(home)/20810/S/?" type="text/javascript"></scr'+'ipt>');
             else if(ENV.country === 'CA') document.write("<scr"+"ipt type='text/javascript' src='http://www.googletagservices.com/tag/js/gpt.js'>googletag.defineSlot('/7326/Lagardereactive.network/SportsFR.adNetwork',[728, 90], 'rogers_Lagardereactive.network_leader').addService(googletag.pubads());googletag.pubads().enableSyncRendering();googletag.enableServices();googletag.display('rogers_Lagardereactive.network_leader');</scr"+"ipt>");
             else if(ENV.country === 'FR') $.la.promo.writeAd('megaban2');
             else $.la.promo.writeAd('megaban2');
        </script></div><div id="ad-rec-top1-load"><script type="text/javascript">$.la.promo.writeAd('rec-top1');</script></div><div id="ad-ban-load"><script type="text/javascript">$.la.promo.writeAd('ban');</script></div><div id="ad-rec-top2-load"><script type="text/javascript">$.la.promo.writeAd('rec-top2');</script></div><div id="ad-inread-load"><script type="text/javascript">$.la.promo.writeAd('inread');</script></div><div id="ad-habillage-load"><script type="text/javascript">$.la.promo.writeAd('habillage');</script></div></div></div><script>$.la.promo.deferedAdsProcess();</script><script type="text/javascript">
    var _vrq = _vrq || [];
    _vrq.push(['id', 246]);
    _vrq.push(['automate', false]);
    _vrq.push(['track', function(){}]);
    (function(d, a){
    var s = d.createElement(a),
    x = d.getElementsByTagName(a)[0]; s.async = true; s.src = 'http://a.visualrevenue.com/vrs.js'; x.parentNode.insertBefore(s, x); })(document, 'script');
</script><!-- Google Tag Manager --><noscript><iframe src="http://www.googletagmanager.com/ns.html?id=GTM-MJGZ39"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript><script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push(
{'gtm.start': new Date().getTime(),event:'gtm.js'}
);var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-MJGZ39');</script><!-- End Google Tag Manager --><script type="text/javascript" src="http://1x12.net/sites/lsf-banners/banner.js"></script><script type="text/javascript">(function(d){var uuid=null;if(typeof Storage!=="undefined"){function guid(){function e(){return Math.floor((1+Math.random())*65536).toString(16).substring(1)}return e()+e()+"-"+e()+"-"+e()+"-"+e()+"-"+e()+e()+e()}uuid=localStorage.getItem("uuid");if(uuid==null){uuid=guid();localStorage.setItem("uuid",uuid)}} var dl=d.location;var t=new Date;d.write("<script src='http://cdn.dekalee.net/serve/122.js?p=&quot;+encodeURIComponent(dl.pathname)+&quot;&amp;s=&quot;+encodeURIComponent(dl.search)+&quot;&amp;t=&quot;+t.getTime()+&quot;&amp;uuid=&quot;+uuid+&quot;&amp;width=&quot;+window.innerWidth+&quot;'>\x3C/script>");}(top.document));</script>
		
		
			<script type="text/javascript">
				window._taboola = window._taboola || [];
				_taboola.push({flush: true});
			</script>
		
	</body>
</html> 
