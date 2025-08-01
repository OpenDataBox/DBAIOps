/* Copyright (c) 2001, 2015, Oracle and/or its affiliates. All rights reserved.*/
/
/ ident "%Z%%M% %I%     %E%"
/
/ NAME
/   crsus.msg
/ DESCRIPTION
/   Message file for CRS/CLSD global alert
/ NOTES
/
# CHARACTER_SET_NAME=American_America.US7ASCII
/
/ MODIFIED
/   apfwkr      10/20/15 - Backport nmallego_bug-20408163 from main
/   vdandu      10/16/14 - Backport vdandu_bug17780903_1 from
/                          st_has_11.2.0.4.0gipsu
/   pckamath    04/09/14 - Backport pckamath_bug-17531342 from main
/   vdandu      05/06/14 - Bug 17780903
/   jwarnes     10/15/13 - Backport jwarnes_bug-14525998 from main
/	                   Backport Bug Number: 17601084
/   pckamath    10/14/13 - Backport of bug16206997
/   pckamath    06/07/13 - Backport of bug16846090
/   minzhu      05/21/13 - Backport minzhu_bug-16443575 from st_has_12.1.0.1
/   jwarnes     04/10/13 - Bug 16630831: Add message CRS-0036
/   jwarnes     02/26/12 - Bug 16399678: Backport jwarnes_bug-13936066 
/                          from main
/   shiyer      01/17/13 - Backport shiyer_bug-13584057 from main
/   shiyer      01/01/13 - Backport shiyer_bug-13503776 from main
/   bamorale    11/15/12 - Backport anjiwaji_bug-11843934 from main
/   csivanan    10/24/12 - Backport csivanan_bugfix_10638125 from
/   spavan      08/17/12 - Backport spavan_bug-8764954 from
/   arpshukl    07/17/12 - Backport arpshukl_bug-13499646 from main
/   wegu        07/13/12 - XbranchMerge wegu_bdbfull from main
/   gdbhat      04/09/12 - Backport gdbhat_bug-13574793 from main
/   samjo       03/12/12 - Backport samjo_bug-11730613 from main
/   nkorehis    03/09/12 - Backport nkorehis_bug-9648247 from main
/   nbraak      10/21/11 - Backport nbraak_bug-12867511 from main
/   jleys       07/18/11 - Review comments
/   jleys       07/17/11 - Do not print help for votedisk backup
/   samjo       07/05/11 - Add for upgrade message to query av
/   agusev      06/16/11 - Backport agusev_bug-12648190 from main
/   sbezawad    06/02/11 - Backport sbezawad_ocrbackups_asm from main
/   sbezawad    05/23/11 - Backport sbezawad_force_upgrade from main
/   spavan      05/05/11 - xbranchmerge fix spavan_proj19732-wallet
/   vsamudra    05/03/11 - Backport vsamudra_chmalerts from main
/   anutripa    05/01/11 - Backport anutripa_purgeoclumon from main
/   nmallego    01/23/15 - Bug20408163 - Message for CSSD base priority
/   pckamath    01/14/14 - Bug17531342 -Remove manual from CRS-1625 message
/   akhaladk    04/28/11 - Add more credential messages
/   rbvarshn    04/26/11 - Backport rbvarshn_b9872858 from main
/   spavan      04/26/11 - XbranchMerge spavan_bug-9872147 from main
/   jchandar    04/25/11 - Backport jchandar_prionicelinux from main
/   vsamudra    04/18/11 - CHM alert messages for clusterware log(Bug 12370546)
/   anutripa    04/11/11 - Change oclumon dumpnodeview usage
/   lmortime    04/07/11 - Adding crsctl credential messages
/   jchandar    03/31/11 - add priority and nice value in process
/   jgobbur     03/30/11 - to fix bug#11937312
/   cwang       03/24/11 - Backport cwang_bug-9974925 from main
/   anutripa    03/21/11 - Backport anutripa_bug-11820743 from main
/   ssaggar     03/16/11 - XbranchMerge ssaggar_9750124_new from main
/   csivanan    03/15/11 - bug/10638125
/   samjo       03/14/11 - Adding CHA specific messages 3501-3999
/   hkanchar    03/10/11 - Backport hkanchar_bug-9465089 from main
/   papatel     03/09/11 - Bug 11848398
/   arpshukl    03/06/11 - Correct bdb location change message for CRF
/   vmanivel    03/03/11 - WhatIf for add/modify/fail
/   wegu        03/02/11 - Bug-10413273. Add metric explanation and units for
/                          oclumon dumpnodeview -h 
/   vsamudra    03/02/11 - Backport vsamudra_bug-9940700 from main
/   anutripa    03/01/11 - Fix message 9015 for oclumon
/   csivanan    02/17/11 - bug/10239164
/   dtrejoh     02/16/11 - Bug 9754300. Add msg for clusterized commands.
/   cwang       02/14/11 - fix 5019
/   priagraw    02/10/11 - Backport priagraw_bug-11069507 from main
/   rbvarshn    02/09/11 - update start testdns msg
/   vmanivel    02/07/11 - WhatIf for Servers
/   jgrout      01/28/11 - Backport bug 6849323 fix from main
/   jgrout      01/28/11 - Backport bug 10039715 fix from main
/   vsamudra    01/26/11 - Add error message for dumpnodeview -allnodes -n
/                          combined usage
/   priagraw    01/19/11 - Backport priagraw_bug-10011022 from main
/   diguma      01/19/11 - Backport diguma_bug-10309627 from main
/   jgrout      01/18/11 - Fix bugs 6849323, 8313948 and 10039715
/   priagraw    01/14/11 - add alert 1662, 1663
/   nbraak      01/12/11 - adding cardinality hotmod failure message
/   sltam       01/11/11 - Backport sltam_bug-9800595 from main
/   ssaggar     01/10/11 - Bug: 9750124
/   spavan      01/06/11 - fix bug10081734
/   sbezawad    12/21/10 - Add alert if OCR backup in ASM DG is not accessible
/   vmanivel    12/21/10 - WhatIf for ServerPools
/   samjo       12/17/10 - XbranchMerge samjo_bug-10079965 from main
/   spavan      12/16/10 - messages for osuser wallets
/   sltam       12/08/10 - Add 5020
/   gdbhat      12/01/10 - Policy mgmt msgs
/   samjo       11/29/10 - Add 1119 mesg to reject AV change
/   nbraak      11/23/10 - Backport nbraak_bug-09916033 from main
/   priagraw    11/22/10 - add backup option to 4392
/   diguma      11/19/10 - adding alert msg to the agent
/   hkanchar    11/18/10 - Update 5017 error message
/   nbraak      11/11/10 - bug 09916033, 10037262
/   vmanivel    10/19/10 - What-If for Resources
/   nbraak      09/28/10 - adding crs pe message and expanding crs pe space
/                          allocation
/   ankkhand    09/02/10 - modify 'CAUSE' portion of err 5018
/   cwang       08/30/10 - bug 9974925 fix syntax 5019
/   ankkhand    08/26/10 - fix bug# 9688552
/   samjo       08/18/10 - Changes for oclumon analyze
/   sbezawad    07/28/10 - Bug 9648247: Add alert if some of the contents of
/                          OCR/OLR are corrupt.
/   cwang       07/27/10 - bug 9945271 missing 5019
/   cwang       07/07/10 - XbranchMerge cwang_bug-9799693 from main
/   sukumar     07/06/10 - Change BDB to repos and add more CHM messages.
/   cwang       06/23/10 - add 5019
/   anutripa    06/14/10 - CHM/IPD: Add CRFM component to debug help for
/                          oclumon
/   anutripa    06/16/10 - Remove -m option from oclumon commands
/   anutripa    06/03/10 - Add bdb change loc help
/   pkharter    05/05/10 - add query ipmiconfig (9682450)
/   jleys       04/28/10 - Fix typo
/   jleys       04/27/10 - Review comments
/   jleys       04/27/10 - Remove msg 1660 becasue it duplicates 1625
/   jleys       04/27/10 - Adding new alert log msg for normal shutdown
/   jleys       04/26/10 - Add alert log entry for voting file add during
/                          discovery
/   jleys       04/23/10 - Add alert log entries
/   gnagiah     04/23/10 - 9469133 Added message 1714
/   jgrout      04/22/10 - Fix bug 9581411
/   jgrout      04/21/10 - Fix online help message 4832
/   anutripa    04/15/10 - ADD IPD daemons related messages
/   sbezawad    04/15/10 - Bug 9466855: Add alert if specific key is missing
/                          from OCR/OLR
/   jgrout      04/14/10 - Add message CRS-4697
/   pkharter    04/14/10 - code-review comments (9498965)
/   pkharter    04/09/10 - add msgs for crsctl unset ipmiconfig (bug 9498965)
/   spavan      04/07/10 - fix bug9561854
/   spavan      03/29/10 - fix bug9494516
/   anutripa    03/22/10 - Add messages for CHM/IPD
/   hchau       03/15/10 - Bug 9462061. Msg 10100: args -> arguments. Msg
/                          10103: error(s) -> errors.
/   spavan      03/10/10 - fix bug9350240
/   pkharter    03/08/10 - improve message 4218 "IPMI not found" (bug 8916164)
/   jgrout      02/25/10 - Fix bugs 9381673 and 9404752
/   jgrout      02/21/10 - Fix bugs 8370534, 9233639, 9278870 and 9318794
/   diguma      02/11/10 - msgs for crsd clean up
/   sbezawad    02/11/10 - Bug 9098918: Add alert when OCR service exits
/   hchau       02/10/10 - Bug 6956719. Add messages for init.ohasd script.
/   spavan      02/09/10 - fix bug9299151
/   psankara    02/08/10 - change 4683 to make it generic
/   jgrout      02/01/10 - Fix bug 9336782
/   diguma      01/27/10 - add string priority on msg 4678
/   stpolu      01/25/10 - Bug 8509615
/   cwang       01/19/10 - add 5017
/   wegu        01/15/10 - Modify 4119
/   sbezawad    01/08/10 - Bug 8512453: Add alert for auto repair of OCR
/                          configuration on local node
/   rdasari     12/23/09 - add mesg 2802
/   spavan      12/14/09 - add cvu generic message to add to alert log
/   vmanivel    12/10/09 - Bug 9084067
/   hchau       12/07/09 - Add messages for crswrapexece.pl
/   jgrout      01/13/10 - Add "crsctl check evm"
/   sbezawad    01/11/10 - Project 31227: Add alert message for OLR
/                          configuration upgrade
/   jgrout      01/12/10 - Add resource and type error messages
/   diguma      01/07/10 - 8651449: fix crsctl delete usage
/   hchau       01/06/10 - Bug 9246093. Split alert msg 4905 into 2 msgs: 4905,
/                          4924.
/   ysharoni    12/28/09 - bug 9042422 - clsgpnp_crs_callHosts to return host
/                          errs/excpts
/   rdasari     12/23/09 - add mesg 2802
/   vmanivel    12/10/09 - Bug 9084067
/   sravindh    12/07/09 - Bug 8297804
/   vmanivel    12/02/09 - Bug 8915362
/   stpolu      12/02/09 - Bug 8760631
/   spavan      11/26/09 - fix usage message
/   psankara    11/26/09 - Add alert log msg for config change rejection
/   diguma      11/21/09 - 8670191: change msg 4043
/   psankara    11/20/09 - Bug 8909979
/   ysharoni    11/09/09 - add dynamic gpnp/mdns log/trace supp
/   psankara    11/01/09 - bug 9048685
/   hchau       10/23/09 - Add 2413, 2414. Step sync fails due to high RTT.
/   jgrout      10/21/09 - Fix bug 8921040
/   vmanivel    10/20/09 - Bug 8739328
/   vmanivel    10/16/09 - Bug 6841172
/   psankara    10/14/09 - bug 8904082
/   spavan      10/07/09 - fix bug8981030
/   vmanivel    09/29/09 - Bug 8852422
/   psankara    09/10/09 - bug 8640347
/   sbezawad    08/26/09 - Bug 8833808: Add msg for OLR restore
/   stpolu      08/24/09 - Adding error msg for CRS startup
/   psankara    08/14/09 - bugs 8667037, 8467036 
/   psankara    08/11/09 - bugs 8500770, 8414085
/   priagraw    07/29/09 - messages for vd>15 check.
/   stpolu      07/27/09 - Bug 8686859. Prompt culprits at shutdown failure
/   vmanivel    07/22/09 - Bug 8645873
/   minzhu      07/15/09 - backup mesg
/   shullur     07/13/09 - For fixing bug 8594111 and 8614873
/   diguma      06/06/09 - add 4267 
/   cwang       06/06/09 - add 5016
/   hchau       06/03/09 - Bug 7647028. Migrate ctss to dynamic log level
/                          change
/   mkallana    06/03/09 - add a message for IO failure
/   vmanivel    06/01/09 - Bug 8551680: Updating crs_* messages.
/   sbezawad    05/28/09 - Bug 8532404: Add warning message during upgrade that
/                          upgrade operation may take several minutes
/   skakarla    05/28/09 - adding state change alert
/   hchau       05/27/09 - Add msg 2412: detected time different is too much in
/                          observer mode.
/   sbezawad    05/24/09 - Bug 8461293: Add new message when upgrade return
/                          unimplemented operation
/   jgrout      05/21/09 - Remove enable, disable and config cluster
/   jgrout      05/20/09 - Fix enable, disable and config cluster
/                          to work with all the cluster daemons
/   shullur     05/19/09 - Bug 8527069: For fixing spelling mistakes
/   sbezawad    05/14/09 - Add alert when import file does not exists
/   jleys       05/13/09 - Add periods
/   anutripa    05/12/09 - Add message for missing msg id
/   sbezawad    05/12/09 - Add alert when Cache Local exit during reconfig
/   jgrout      05/11/09 - Implement exclusive-mode crsctl start
/   mimili      05/11/09 - Add EVMD port taken alert message (1403)
/   sujkumar    05/06/09 - add out of bounds error message
/   bmanry      05/06/09 - incorporate errors_us feedback on LG messages
/   jleys       05/03/09 - Add msgs for SAGE fencing failures
/   minzhu      05/01/09 - modify msg 4403
/   hchau       04/29/09 - Bug 8265795,8465897,8215975. Edit msg 2404 and add
/                          msg 2411
/   samjo       04/29/09 - Add alert for member kill by ocr. Ran spell check.
/   jleys       04/24/09 - Add more verbiage to 4402 msg action
/   bmanry      04/21/09 - add Last Gasp alert log messages (range 8000-8199)
/   hchau       04/17/09 - Add mesg to document OCTSSD switching to Active mode
/   jgrout      04/15/09 - Add clusterization NLS messages
/   vmanivel    04/15/09 - Bug 8240637, updating error message
/   hchau       04/14/09 - Capitalize 'service' in Cluster Time Synchronization
/                          Service
/   psankara    04/14/09 - Bug 8393286 
/   minzhu      04/14/09 - fix bug 8413683
/   hchau       04/10/09 - Change message 2408 to mention about ctss
/   gdbhat      04/10/09 - Bug 8293296
/   vmanivel    04/09/09 - Bug 7231169: Adding alerts for CRS and Agent
/                          Framework
/   jgrout      04/02/09 - Fix bug 7497372
/   minzhu      04/07/09 - add backup usage
/   minzhu      04/01/09 - enrich 4608 for '16'
/   sbezawad    03/30/09 - Add alert for OCR failures in clscfg
/   minzhu      03/30/09 - fix 5867996
/   jgrout      03/26/09 - Fix bug 8298209
/   jgrout      03/25/09 - Fix bug 8288978
/   sbasu       03/25/09 - add crsctl set|get jazn messages
/   minzhu      03/24/09 - new mesg 1642
/   gdbhat      03/20/09 - Bug 7322005
/   minzhu      03/19/09 - update by message review
/   minzhu      03/12/09 - tune unset/set messages
/   minzhu      03/12/09 - add log for unset
/   mkallana    03/15/09 - fix the message for crsctl
/   mkallana    03/13/09 - message for crstl add diskgroup
/   minzhu      03/10/09 - change for 4608 too
/   sbezawad    03/09/09 - Add more messages for clusterware upgrade
/   minzhu      03/06/09 - modify 4602
/   psankara    03/05/09 - Bug 7691630.
/   vmanivel    03/05/09 - Bug 8288691. Adding OHASD alert.
/   jleys       03/04/09 - Remove node number from 1636
/   mkallana    03/02/09 - final review comments
/   mkallana    03/01/09 - review comments
/   jgrout      02/26/09 - Clean up add, delete, query for Cluster/SIHA
/   cwang       02/25/09 - Agent alert messages 5011 5012 5013 and 5014
/   minzhu      02/25/09 - add new mesg for set css trace
/   jachang     02/24/09 - Add failure case for css unset operations
/   jgrout      02/22/09 - Fix bug 8217252
/   hchau       02/19/09 - Add 'crsctl check ctss'
/   mkallana    02/18/09 - add NLS messages for SLOS errors
/   sbezawad    02/13/09 - Add clusterware upgrade specific messages
/   hkanchar    02/13/09 - Fix for bug#8207130 and update with feedback
/   jleys       02/12/09 - Review comments
/   jgrout      02/10/09 - Fix bug 7828526
/   jleys       02/10/09 - Add more CSSD error msgs
/   jleys       02/01/09 - Add alert log msg for exclusive mode failure
/   diguma      02/10/09 - 7675042: changing msg to include addition/deletion
/   sbezawad    02/02/09 - Add crsctl set crs activeversion
/   samjo       02/10/09 - Add alert for ASM access error in OCR
/   minzhu      01/27/09 - add DRUIDs
/   agusev      01/22/09 - shutdown related changes
/   lmortime    01/15/09 - Storing logging levels to daemon profiles
/   minzhu      01/15/09 - update wording for delete voting disk
/   agusev      01/08/09 - added more crsd errors
/   jgrout      01/07/09 - Fix bug 7279710, changing "appears healthy"
/                          to "is online"
/   jgrout      01/07/09 - When possible, remove trailing linefeeds
/                          from crsctl messages
/   jgrout      01/07/09 - Separate crsctl check css from crsctl check cssd
/   diguma      01/05/09 - discoverystring between single-quotes
/   jleys       12/27/08 - Add msg for node removal not as eviction
/   mkallana    01/06/09 - review comments
/   mkallana    01/02/09 - add cause/action details for 1627
/   mkallana    12/31/08 - add alert logs for Config Change
/   mkallana    12/28/08 - fix shutdown alertlog
/   jleys       12/27/08 - Add msg for node removal not as eviction
/   minzhu      12/22/08 - interesting crash in messages
/   minzhu      12/12/08 - finalizing pin/unpin mesgs
/   mkallana    12/23/08 - modify shutdown alertlog
/   minzhu      12/22/08 - interesting crash in messages
/   mkallana    12/22/08 - add alertlog for manual shutdown
/   minzhu      12/12/08 - finalizing pin/unpin mesgs
/   agusev      12/12/08 - Added a new error message
/   agusev      12/16/08 - added more crsd errors
/   ysharoni    12/09/08 - add CLSGPNP_SIG_WALLETDIF err
/   minzhu      12/08/08 - mesg refine
/   minzhu      12/08/08 - refine pin wording
/   minzhu      11/14/08 - add more pin/unpin mesg
/   gdbhat      12/04/08 - Tabular stat help msg
/   psankara    12/02/08 - 7525958, 7524102, 7521013, 7562941
/   lmortime    11/10/08 - Bug 6619628 - Requiring that the user specify an
/                          attr value, if only a blank one
/   ppallapo    10/31/08 - Fix GPnP messages
/   diguma      10/22/08 - delete node
/   diguma      10/15/08 - Adding msg for change discovery string
/   cwang       10/10/08 - add msg 5010
/   jgrout      10/07/08 - Convert get, set and unset to new parser
/   lmortime    09/25/08 - Bug 6897806 - fixing crsctl relocate resource -s
/                          nodename
/   lmortime    09/24/08 - Bug 7245297 - Replacing clssnsprivatebynum with new
/                          function clsu_get_private_ip_addr
/   agusev      09/30/08 - fixed a typo
/   sukumar     09/24/08 - Add syntax error on server side for clsdm.
/   agusev      09/22/08 - Added a better dependency error
/   lmortime    09/19/08 - Bug 7279735 - CHANGE CRSCTL "CLUSTERWARE" COMMAND
/                          STEMS, HELP TO "CLUSTER
/   jgrout      09/19/08 - Remove newlines from converted messages
/   ysharoni    09/19/08 - Remove gpnp soap rcv msg
/   gdbhat      09/05/08 - Bug 6826391
/   jgrout      09/01/08 - Convert add, check, delete, start, stop,
/                          query, debug and lsmodules to new parser
/   spavan      08/25/08 - fix query wallet message - bug7289109
/   akhaladk    09/05/08 - add msg about bad perms
/   skakarla    08/20/08 - For fixing bug 7339885
/   samjo       08/14/08 - Changing from passive to observer
/   agusev      08/19/08 - separated crsd managed entity namespaces
/   akhaladk    08/19/08 - Add new msg for dependency perms check
/   lmortime    08/18/08 - Bug 6528796 - Allowing multipule types for delete
/                          type
/   agusev      08/12/08 - added queueing-related messages
/   gdbhat      08/12/08 - Bug 7320963
/   agusev      08/12/08 - Fixed severity in a few crsd messages
/   psankara    08/07/08 - New message for crsctl ipmi login change
/   akhaladk    08/07/08 - Fix start has/crs help
/   jachang     08/05/08 - Add ASM voting diskgroup messages
/   ppallapo    07/30/08  - Add GPnP specific messages.
/   jachang     07/28/08  - New message for unsetting linked parameter
/   agusev      07/24/08  - Added deprecated messages for crs_ commands
/   gdbhat      07/23/08  - Bug 7114066
/   gdbhat      07/21/08  - Bug 6933023
/   lmortime    07/21/08  - Bug 7142054 fix: server groups to server pools
/   jgrout      07/07/08  - Fix bug 7204412 (clean up getperm help)
/   gdbhat      07/03/08  - Bug 6957064
/   ppallapo    06/27/08  - Add GPnP specific messages
/   gdbhat      05/15/08  - Moved messages and comments from clsdus.msg to 
/                           crsus.msg
/   ysharoni    05/01/08  - Add mDNS messages
/   samjo       03/26/08  - Fix CTSS alerts
/   vrai        12/16/07  - Cluster Time Synchronization service alerts
/   jgrout      12/03/07  - Correct format in msgs 2005, 2006
/   jleys       08/24/07  - Correct msg 1606
/   samjo       07/09/07  - Add Cluster Time Synchronization service alerts
/   rwessman    05/17/07  - Added RD and GNS pass-through messages.
/   mkallana    03/13/07  - XbranchMerge mkallana_alertlog_dec04 from
/                           st_has_11.1
/   ysharoni    12/15/06  - addition of gpnp messages.
/   mkallana    12/19/06  - add alert messages for css
/   minzhu      08/28/06  - better wording for split-brain case
/   minzhu      08/10/06  - add new alert msg for split-brain case 
/   kelee       07/24/06  - Fix OLR message 
/   ilam        03/24/05  - Fix CRS alert for 10gR2 
/   samjo       03/17/05  - Update clscfg alerts 
/   rajayar     02/16/05  - caues and action for CRS and EVM 
/   samjo       02/04/05  - Adding cause and action for OCR alerts 
/   kelee       12/22/04  - change OCR alert 
/   ilam        11/08/04  - Update with more 10gR2 CRS messages
/   ilam        09/24/04  - Add msg for CLSDM 
/   ilam        06/23/04  - Add alert messages for CRS stacks
/   ilam        05/14/04  - ilam_clsd_10gr2_logging_change
/   ilam        05/08/04  - Created
/
/ ***************************************************************************
/ Message number ranges:
/ ***************************************************************************
/   0000-0100: CLSD specific internal messages (From clsdus.msg)
/   0101-1000: CRS specific messages (From clsdus.msg)
/   1001-1100: OCR specific messages (From clsdus.msg)
/   1101-1200: Oracle Clusterware upgrade specific messages (From clsdus.msg)
/   1201-1300: CRSD specific messages (From clsdus.msg)
/   1301-1400: OHASD specific messages
/   1401-1600: EVMD specific messages (From clsdus.msg)
/   1601-1800: CSSD specific messages (From clsdus.msg)
/   1801-1900: CLSCFG specific messages (From clsdus.msg)
/   1901-2000: CRSCTL specific messages (From clsdus.msg)
/   2001-2050: CLSDM specific messages (From clsdus.msg)
/   2101-2300: OLR specific messages (From clsdus.msg)
/   2301-2400: GPNP specific messages (From clsdus.msg)
/   2401-2499: Cluster Time Synchronization service specific messages 
/   2500-2900: CRS Policy Engine error messages
/   4000-4999: CRSCTL specific messages
/   5000-5500: HAA specific messages
/   5501-5600: Reporter specific messages
/   5601-5700: MDNS specific messages
/   5701-5800: Placement Policy specific messages
/   5801-5999: AGFW specific messages
/   6001-6999: CRSD specific messages
/   7000-7999: GPNP messages (see also 2301-2400)
/   8000-8199: Last Gasp messages
/   9000-9999: CHM/IPD specific message
/   10000-10001: Other component specific messages
/   10100-10130: crswrapexece.pl specific messages
/
/
/ ***************************************************************************
/ Message Severity:
/ ***************************************************************************
/ 0 - Undefined
/ 1 - Error
/ 2 - Warning
/ 3 - Info
/ ***************************************************************************
/
/ CLSD specific messages
/
0000, 0, "Testing message for CLSD regression %s"
// *Document: NO
001,  1, "Message ID %s-%04d not found."
// *Cause:  The messsage for the given message id is not found in any language.
// *Action: Make sure the product is setup correctly on the system.
/
002, 1, "%s:Internal list corruption. trace file: \"%s\""
// *Cause: An internal error was detected during trace file flush processing.
// *Action: Contact Oracle Support Services.
/
003,  1, "An error was encountered while attempting to open file \"%s\". Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to open the specified
//         file.
// *Action: Examine the additional diagnostics, if available, and attempt
//          to correct any file system environmental problems if indicated.
//          Otherwise, contact Oracle Support Services.
/
004,  1, "Logging terminated for the process. Log file: \"%s\""
// *Cause: One or more file system errors were encountered which caused
//         logging to be terminated for this process. 
// *Action: Examine preceding alert log messages for details on the error or
//          errors that occurred. Restart the process to reenable logging.
/
005,  1, "log file \"%s\" deleted after close failure"
// *Cause: This message is informational. An attempt to close the specified
//         log file failed. The contents of the log file after a close
//         error are undefined. The log file has been successfully deleted.
//         Log data are lost.
// *Action: None. 
/
006,  3, "file rotation processing continues for file: \"%s\""
// *Cause: This message is informational and indicates only that a preceding
//         error was not sufficiently severe to terminate file rotation which
//         might otherwise be the case.
// *Action: None.
/
007,  1, "failed to open new log file \"%s\"
// *Cause: The file system encountered an error while attempting to open the
//         specified file during log file rotation. Log data are lost.
// *Action: Review the preceding Alert log message CRS-0011 and attempt to
//          resolve any file system environmental problems indicated.
//          Otherwise, contact Oracle Support Services.
/
008,  1, "opened new file \"%s\" after close failure"
// *Cause: This message is informational. Log data are lost.
// *Action: None.
/
009,  1, "log file \"%s\" reopened"
// *Cause: An error was encountered during rotation processing so that log
//         file rotation could not proceed. The original log file, which
//         had been closed, was successfully reopened.
// *Action: Review Alert log messages that precede this message that
//          identify the file system error or errors encountered. If the
//          additional diagnostic data in a preceding alert log message
//          indicate a file system environmental problem, attempt to correct
//          it. Otherwise contact Oracle Support Services.
/
010,  0, "NONE AVAILABLE"
// *Document: NO
// *Action: None. The text of this message is inserted into other messages and
//         is defined here so that it can be translated into other languages.
/
011,  1, "An error occurred while attempting to close file \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered when attempting to close the specified
//         file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
012,  1, "An error occurred while attempting to rename file \"%s\" to \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered when attempting to rename the source
//         file to the destination file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
013,  1, "An error occurred while attempting to check for the existence of file \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to determine if the
//         specified file existed.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
014,  1, "An error occurred while attempting to delete file \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to delete the specified
//         file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
015,  1, "An error occurred while attempting to flush file \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while an attempting to flush the
//         specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
016,  1, "An error was encountered while attempting to free the file name object for file \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to free the file name
//         object for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
017,  1, "An error occurred while attempting to create a file name object for file \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create a file name
//         object for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
018,  1, "An error occurred while attempting to reopen file \"%s\" during log file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to reopen the 
//         specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct 
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
019,  1, "file rotation terminated. log file: \"%s\""
// *Cause: One or more file system errors were encountered which caused log
//         file rotation to be terminated for the process. Although log file
//         rotation has been terminated, logging continues.
// *Action:  Review Alert log messages that precede this alert log message
//           that identify the file system error or errors encountered. If the
//           additional diagnostic data in a preceding alert log message
//           indicate a file system environmental problem, attempt
//           to correct it. Otherwise contact Oracle Support Services.
//
//           To re-enable file rotation the process must be restarted.
/
020,  1, "An error occurred while attempting to create a file name object for file \"%s\" during file open processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create a file name
//         object for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
021,  1, "An error occurred while attempting to check for the existence of file \"%s\" during file open processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to determine if the
//         specified file existed.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
022,  1, "An error occurred while attempting to change access permissions and privileges for file \"%s\" during file open processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to change access
//         permissions and privileges for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
023,  1, "An error occurred while attempting to create default permissions for file \"%s\" during file open processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create default file
//         permissions for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
024,  1, "An error occurred while attempting to create a file name object for file \"%s\" during file open processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create a file name
//         object for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services. 
/
025,  1, "An error occurred while attempting to create a file object for file \"%s\" during file open processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create a file object
//         for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
026,  1, "failed to create one or more file name objects to rename \"%s\" to \"%s\" during file rotation processing"
// *Cause: An error was encountered while attempting to create one of more
//         file name objects for the specified files.
// *Action: Contact Oracle Support Services.
/
027,  1, "An error occurred while attempting to determine the size of file \"%s\" during file open processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to determine the size of
//         the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
028,  1, "An error occurred while attempting to write the banner for file \"%s\". Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to write the banner record
//         to the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
029,  1, "An error occurred while attempting to flush file \"%s\" after the banner record was written. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to flush the
//         specified file after writing the banner record.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
030,  1, "An invalid file type was encountered while attempting to perform file synchronization. Additional diagnostics: %s ftype: %d"
// *Cause An invalid file type specification was encountered by file 
//        synchronization services.
// *Action: Contact Oracle Support Services.
/
031,  1, "An error occurred while attempting to flush file \"%s\" during file synchronization processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to flush the
//         specified file during file synchronization processing.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
032,  1, "An error occurred while attempting to create a file object for file \"%s\" during generate-file-name processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create a file object
//         for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
033,  1, "An error occurred while attempting to create a file object for file \"%s\" during generate-file-name processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create a file object
//         for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
034,  1, "An error occurred while attempting to open file \"%s\" during generate-file-name processing. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to open the 
//         specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
035,  1, "An invalid pointer to an internal control structure was encountered while attempting to open a log file. Additional diagnostics: %s"
// *Cause: An invalid pointer was encountered when attempting to open a
//         file. Logging is disabled for the process.
// *Action: Contact Oracle Support Services.
/
036,  1, "An error was encountered while attempting to open log file \"%s\". Directory information \"%s\"."
// *Cause: An error was encountered while attempting to open the specified 
//	   file. Logging is disabled for the process.
// *Action: Review the preceding alert log messages and attempt to
//          resolve any file system environmental problems indicated.
//          Otherwise, contact Oracle Support Services.
/
037,  1, "An error occurred while attempting to write to file \"%s\". Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to write to the 
//         specified file. Logging is disabled for the process.
// *Action: Review preceding Alert log messages and attempt to
//          resolve any file system environmental problems indicated.
//          Otherwise, contact Oracle Support Services
/
038,  1, "An invalid pointer to an internal control structure was encountered while attempting to open a trace file. Additional diagnostics: %s"
// *Cause: An invalid pointer was encountered when attempting to open a
//        trace file. Tracing is disabled for the process.
// *Action: Contact Oracle Support Services.
/
039,  1, "An error occurred while attempting to open trace file \"%s\"."
// *Cause: An error was encountered while attempting to open the specified 
//         file. Tracing is disabled for the process.
// *Action: Review preceding Alert log messages and attempt to
//          resolve any file system environmental problems indicated.
//          Otherwise, contact Oracle Support Services
/
040,  1, "Trace logging terminated for the process. trace file: \"%s\""
// *Cause: One or more file system errors were encountered which caused
//         tracing to be terminated for this process.
// *Action: Examine preceding Alert log messages for details on the error or
//          errors that occurred. Restart the process to reenable logging.
/
041,  1, "Trace file rotation terminated for the process. Trace file: \"%s\""
// *Cause: One or more file system errors were encountered which caused trace
//         file rotation to be terminated for the process. Although trace file
//         rotation has been terminated, tracing continues.
// *Action:  Review Alert log messages that precede this alert log message
//           that identify the file system error or errors encountered. If the
//           additional diagnostic data in a preceding alert log message
//           indicate a file system environmental problem, attempt
//           to correct it. Otherwise contact Oracle Support Services.
//
//           To reenable trace file rotation the process must be restarted.
/
/ Messages for CRS
/
101,    0, "Name"
102,    0, "Type"
103,    0, "R/RA"
104,    0, "F/FT"
105,    0, "Target"
106,    0, "State"
107,    0, "Host"
108,    0, "Attribute"
109,    0, "Value"
110,    0, "Rebalance"
111,    0, "unavailable"
115,    0, "RESTART COUNT"
116,    0, "RESTART ATTEMPTS"
117,    0, "FAILOVER COUNT"
118,    0, "FAILOVER THRESHOLD"
119,    0, "Owner"
120,    0, "Group"
121,    0, "Permission"
122,    0, "Primary PrivGrp"
150,    1, "Error in comma-separated options string parsed: '%s'."
151,    1, "Trailing comma found.\nNote, the comma-separated options string should not contain spaces."
152,    1, "Error in comma delimited entry '%s'."
153,    1, "ATTRIBUTE=VALUE expected."
160,    1, "The attribute '%s' is not supported in this resource type." 
161,    1, "The resource profile template's attribute '%s' has an error." 
162,    1, "The file '%s' exists. Creation is cancelled."
163,    1, "Cannot open the file '%s'."
164,    1, "The file '%s' is locked by another process."
165,    1, "Cannot get a read lock on the file '%s'."
166,    1, "Cannot read the file '%s'."
167,    1, "Cannot remove the action script '%s'."
168,    1, "Cannot create the backup file."
169,    1, "Cannot remove the resource '%s'."
170,    1, "The resource '%s' doesn't exist."
171,    1, "The action script '%s' cannot be created."
172,    1, "The parameter '%s' cannot be interpreted by CRSD."
173,    1, "Invalid command line option."
174,    1, "Resource name cannot exceed 256 characters."
175,    1, "Resource type '%s' either doesn't exist or cannot be accessed."
178,    1, "The pathname is incorrect."
180,    1, "Resource '%s' validation failed."
181,    1, "Cannot access the resource profile '%s'."
182,    1, "RTI error: '%s'"
184,    1, "Cannot communicate with the CRS daemon."
// *Cause:  The CRS daemon on the local node is either not running or there was
//          an internal communication error with the CRS daemon.
// *Action: Check if the CRS daemon process is running on the local node.
185,    1, "Resource template '%s' not found."
186,    1, "There is a switch conflict in the type definition files used by crs_profile\nwhen creating your '%s' type resource. Please make sure each attribute\nswitch is defined only once.\n"
187,    1, "Switch '%s' is used by the following attributes: '%s'."
199,    2, "CRS general warning. No reason is provided."
200,    1, "CRS general failure. No reason is provided."
201,    1, "Catch all failure. No reason is provided."
202,    1, "No resources are registered."
203,    1, "Reason is to be supplied."
204,    1, "One or more attributes not found for resource '%s'"
210,    1, "Could not find resource '%s'."
// *Cause:  An attempt was made to operate on a resource that is not 
//          registered.
// *Action: Ensure that the resource name is specified correctly using the command 'crsctl status resource'.
211,    1, "Resource '%s' has already been registered."
// *Cause:  An attempt was made to register a resource that is already
//          registered.
// *Action: Ensure that the resource name is specified correctly and retry the command.
212,    1, "Resource '%s' is not registered."
213,    1, "Could not register resource '%s'."
// *Cause:  There was an internal error while registering the resource.
// *Action: Check the CRS daemon log file.
214,    1, "Could not unregister resource '%s'."
// *Cause:  There was an internal error while unregistering the resource.
// *Action: Check the CRS daemon log file.
215,    1, "Could not start resource '%s'."
// *Cause:  There was an internal error while starting the resource.
// *Action: Check the CRS daemon log file.
216,    1, "Could not stop resource '%s'."
// *Cause:  There was an internal error while stopping the resource.
// *Action: Check the CRS daemon log file.
217,    1, "Could not relocate resource '%s'."
// *Cause:  There was an internal error while relocating the resource.
// *Action: Check the CRS daemon log file.
218,    1, "Could not restart the resource '%s' on the original node."
// *Cause:  There was an internal error while restarting the resource.
// *Action: Check the CRS daemon log file.
219,    1, "Could not update resource '%s'."
// *Cause:  There was an internal error while updating the resource.
// *Action: Check the CRS daemon log file.
220,    1, "Resource '%s' has invalid resource profile."	
// *Cause: Invalid attributes in the resource profile.
// *Action: Run the command 'crsctl status type' to identify the invalid attributes. Modify these attributes 
//          using the command 'crsctl modify type'.
221,    1, "Resource '%s''s action script cannot be found."
// *Cause: The action script has been deleted from the file system.
// *Action: Run 'crsctl status resource -p' to determine the action script location, and check for its existence.
222,    1, "Resource '%s' has dependency error."
223,    1, "Resource '%s' has placement error."
// *Cause: There was no host available to on which failover/start the resource
//         based on the Placement Policy for the resource.
// *Action: Check the target host for the resource and restart the resource
//          using the 'crsctl start resource' command.    

/
/ added for 10i
224,	  2, "Warning: failed to redirect I/O"
225,    1, "Resource name not specified"
226,    2, "Warning: memory allocation"
227,    1, "Invalid resource name"
228,	  1, "Invalid host"
229,    1, "Invalid combination of flags"
/ end 10i additions
/
230,    1, "Member '%s' is not in the cluster."
// *Cause: The hostname was not found in the cluster.
// *Action: Check the hostnames in the cluster.
231,    1, "Operation is invalid for this type of resource."
232,    1, "Cluster member is down.  Cannot perform operation."
// *Cause:  The node on which CRS is attempting to start the resource is down.
// *Action: Start the node and retry the operation.
233,    1, "Resource or relatives are currently involved with another operation.\n"
// *Cause: Another CRS daemon was operating on the same resource.
// *Action: Wait for a minute and try the command or operation again.
234,    1,  "Attribute not defined in profile"
/
/ added for 10i
/
239,	1,  " Invalid command"
240,	1,  " Piped channel output error"
241,	1,  " Invalid directory path."
242,	1,  " ACL information is not available"
243,	1,  " default setting unavailable"
244,	1,  " registration allow/deny information is not available"
245,	1,  " User doesn't have enough privilege to perform the operation"
246,	1,  " User id is invalid"
247,	1,  " User name or group name is invalid"

248,	1,  " ACL operation failed"
249,	1,  " Authentication failure. "
250,	1,  " Configuration unsuccessful. Try again or restart CRSD."
251,	1,  " CRS configuration file missing."
252,	1,  " CRS configuration file syntax error."
/
253,	1,  " CRS configuration error, the CRS default directory is not set in Oracle Cluster Registry. "
// *Cause:   The Oracle Cluster Registry key which contains the user default CRS key is not 
//           initialised.
// *Action:  Check the CRS configuration. If necessary reinstall CRS.
/
254,	1,  " authorization failure"
// *Cause:  The user permissions were insufficient to operate on the
//          resource.
// *Action: Check the permissions associated with the resource using 
//          'crsctl getperm resource' and set the appropriate user permissions
//          using 'crsctl setperm resource'.
255,	1,  " CRSD is not running in privileged mode. Insufficient permissions to run this command. "
// *Cause:  The CRS daemon was not running as the privileged user.
// *Action: Check if the CRS daemon is running as root (Unix) or Administrator 
//          (Windows).
256,    1,  "Username conflicts with the owner of the resource."
// *Cause:  An attempt was made to give separate user level permissions for the
//          owner of the resource.
// *Action: Check the owner of the resource and the user being given 
//          permissions.
257,    1,  "Groupname conflicts with the primary group of the resource."
// *Cause:  An attempt was made to give separate group level permissions for 
//          the primary group of the resource.
// *Action: Check the primary group of the resource and the group being given 
//          permissions.
258,    1,  "Invalid ACL string format."
// *Cause:  An invalid permission string (ACL) was supplied.
// *Action: Check the syntax of the permission string (ACL).

259,    1,  "Owner of the resource does not belong to the group."
// *Cause:  The owner of the resource does not belong to the expected group.
// *Action: If this resource is owned by the root user, check if the root user
//          belongs to the dba group.
260,    3, "Attempting to start `%s` on member `%s`"
261,    3, "Attempting to stop `%s` on member `%s`"
262,    1, "Start of `%s` on member `%s` failed."
263,    1, "Stop of `%s` on member `%s` failed."
264,    3, "Start of `%s` on member `%s` succeeded."
265,    3, "Stop of `%s` on member `%s` succeeded."
266,    1, "`%s` on member `%s` has experienced an unrecoverable failure."
267,    1, "Human intervention required to resume its availability."
268,    3, "Relocating resource `%s`."
269,    3, "Trying to start `%s.`"
270,    3, "Trying to stop `%s.`"
271,    1, "CRSD shutdown is already in progress.\n"
// *Cause:  crsctl stop command is issued before waiting for a prior stop 
//          command to finish.
// *Action: Wait for the currently running shutdown command to complete 
//          before issuing subsequent command.
272,    3,  "This command remains for backward compatibility only"
// *Cause: A deprecated command was issued.
// *Action: For all new use cases, please use the replacement.
273,    3,  "This command is deprecated and has been replaced by '%s'"
// *Cause: A deprecated command was issued.
// *Action: For all new use cases, please use the replacement.
274,    3,  "This command is deprecated and its functionality incorporated into '%s'"
// *Cause: A deprecated command was issued.
// *Action: For all new use cases, please use the replacement.

/
/
301,    1, "'%s': Hostname can be between 2 and %d alphanumeric or '.' or '-' characters."
302,    1, "'%s': Hostname must consist of alphanumeric or '.' or '-' characters."
303,    1, "'%s': Hostname must begin with a letter."
304,    1, "'%s': Short Hostname can be between 2 and %d alphanumeric or '-' characters."
305,     1, "Cluster Information not available."
306,     1, "\tLook for '%s' among %d cluster members."
307,     2, "Warning: '%s' is not available."
308,     2, "Warning: It may be among [%d] unavailable members."
309,     1, " Specify Subnet in [nnn.nnn.nnn.0] format."
310,     1, "Duplicate definition is not allowed : '%s' at line %d"
311,     1, "HOSTING_MEMBERS values are ignored for balanced placement"
312,     1, "value:  ACTION_SCRIPT is at line %d"
313,     1, "'%s' at line no %d, Action Script must have read and execute permissions."
314,     1, "'%s' at line no %d, Action Script must be a file."
315,     1, "value: '%s' of the keyword: OWN_OPERATIONS is not absolute path at line no %d"
316,     1, "'%s' at line no %d, Action Script must be have read and execute permissions."
317,     1, "'%s' at line no %d, Action Script is not accessible."
318,     1, "'%s' '%s' at line no %d, Access Error"
319,     1, " 'Active Placement' is currently unsupported."
320,     1, " A required resource '%s' is not registered."
321,     1, "profile '%s' extension is not '%s'."
322,     1, "Keyvalue : '%s' for keyword : '%s' is not valid."
323,     1, "['%s'] is not a keyword at line %d."
324,     1, "'%s' is not a keyword."
325,     1, "Unable to process the command, CRS upgrade is going on."
/
/
/
401,     1, "Directory '%s' not found."
402,     1, "Could not make safe directory('%s')"
// *Cause: Unable to create safe directory.
// *Action: Check if you have proper permissions and sufficient space on the disk to create the directory.
403,     1, "Could not change working directory to safe directory('%s')"
// *Cause: Unable to change directory to safe directory.
// *Action: Please check if safe directory exists and if you have proper permissions. 
404,     1, "Could not fork for daemon ('%s')"
405,     1, "Could not get local hostname ('%s')"
406,     1, "Could not create lock directory ('%s')"
// *Cause: Unable to create lock directory.
// *Action: Check if you have proper permissions and sufficient space on the disk to create the directory.
407,     1, "Another CRSD may be running, could not obtain lock file '%s'."
// *Cause: Unable to obtain lock file as another CRSD may be running.
// *Action: Stop the existing CRSD before attempting to start CRSD again.
408,     1, "Could not send application restart request to CRSD"
409,     1, "Could not send application shutdown request to CRSD"
410,     1, "ORACLE_HOME not set"
411,     1, "Could not init the cluster context"
412,     1, "Could not join the cluster group"

413,     1, "Could not initialize the Cluster Synchronization Services context"
// *Cause:   Unable to communicate with the cluster services.
// *Action:  Verify that the Cluster Synchronization Services Daemon is properly configured and is running.
/

414,     1, "Could not establish Event Manager connection"
// *Cause: Unable to communicate with Event Manager daemon.
// *Action: Run the 'crsctl check evmd' command to determine whether Event Manager daemon is properly configured and is running.

415,     1, "Could not establish dependency graph."
416,     1, "Could not create UI connection"
417,     1, "Fixed port %d in use"
418,     1, "Error trying to portmap port %d"
419,     1, "All reserved ports in use"

// Oracle Cluster Registry Related Messages 450-470
451,	0,  " CRS configuration error, unable to initialize Oracle Cluster Registry. "
// *Cause:   The Oracle Cluster Registry that contains information about the CRS configuration
//           is unavailable.
// *Action:  Check the OCR configuration using the ocrcheck utility and resolve any issues it reports. 
//           If the problem persists, contact Oracle Support Services.
/
452,	0,  " CRS configuration error, unable to find CRSD Connection Information in Oracle Cluster Registry. "
// *Cause:   The Oracle Cluster Registry key which contains the user default CRSD connection is not
//           initialized.
// *Action:  Check the OCR configuration using the ocrcheck utility and resolve any issues it reports.
//           If the problem persists, contact Oracle Support Services.
/
453,	0,  " CRS configuration error, unable to find Instance Information in Oracle Cluster Registry. "
// *Cause:   The Oracle Cluster Registry key which contains the Instance's information is not
//           initialized.
// *Action:  Check the OCR configuration using the ocrcheck utility and resolve any issues it reports.
//           If the problem persists, contact Oracle Support Services.
/

// Cluster Synchronization Services Related Messages 471-500
471,     0, "Node number is not found"
// *Cause:   Cluster Synchronization Services is unable to retrieve the node name.
// *Action:  Verify your cluster installation, including any vendor
//           cluster ware. If necessary reinstall the cluster.
/

472,     0, "Node name is not found"
// *Cause:   Cluster Services is unable to retrieve the node name.
// *Action:  Verify your cluster installation, including any vendor
//           cluster ware. If necessary reinstall the cluster.
/

// Event Manager Related messages
501, 0, "Invalid file descriptor in IO_Dispatcher, cannot recover ('%s')"
503, 0, "Connected to Montior '%s', subscribed to %d resources."
/
/ Event ManagerMgr messages
/
504, 0, "Couldn't connect to Event Manager.  Reconnecting in %d seconds."
505, 0, "Lost connection to Event Manager.  Reconnecting in %d seconds."
506, 0, "Couldn't connect to Event Manager for posting."
507, 0, "Error posting Event Manager Event (error=%d)."
508, 0, "Error subscribing to Event Manager events."


/
0600, 0, "[%s] Error [%s]. Details in %s."
// *Document: NO
/


/ CRS Internal Error
/
0601, 0, "Internal error"


/ OHAS Initialization Error
/
0700, 1, "Oracle High Availability Service aborted due to failure to allocate memory. Details at %s in %s."
// *Cause: Memory allocation failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0701, 1, "Oracle High Availability Service aborted due to failure to obtain identity of the running process. Details at %s in %s."
// *Cause: Failed to retrieve user id.
// *Action: Check <crs_home> owner and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0702, 1, "Oracle High Availability Service aborted due to failure to run as privileged user. Details at %s in %s."
// *Cause: Oracle High Availability Service was not running as privileged user.
// *Action: On Unix, restart Cluster Ready Service as privileged user using 'crsctl stop crs -f' followed by 'crsctl start crs'. On Windows, check the privileges of the Oracle High Availability Service and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs' If the problem persists, contact Oracle Support Services.
0703, 1, "Oracle High Availability Service aborted due to failure to initialize the communication context. Details at %s in %s."
// *Cause: The network layer initialization failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0704, 1, "Oracle High Availability Service aborted due to Oracle Local Registry error [%s]. Details at %s in %s."
// *Cause: Oracle Local Registry aborted with an error. Look at the associated error message to determine the underlying issue.
// *Action: Solve the underlying issue and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0708, 1, "Oracle High Availability Service aborted due to failure to retrieve ORA_CRS_HOME environment variable. Details at %s in %s."
// *Cause: An environment variable required by Oracle High Availability Service failed to be set at initialization.
// *Action: Run 'rootcrs.pl -unlock' followed by 'rootcrs.pl -patch' and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0709, 1, "Oracle High Availability Service aborted due to failure to initialize ORA_CRS_HOME path. Details at %s in %s."
// *Cause: Oracle High Availability Service ORA_CRS_HOME path could not be initialized.
// *Action: Check for execute permissions on the Grid Infrastructure home or <crs_home> and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0712, 1, "Oracle High Availability Service aborted due to failure to initialize the network layer with error [%d]. Details at %s in %s."
// *Cause: The network layer initialization failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0713, 2, "An error occurred initializing the Reboot Advisory Monitor: error code [%d]. Details at %s in %s."
// *Cause: An error occurred initializing the Reboot Advisory Monitor component of Oracle High Availability Service.  This error is not fatal; Oracle High Availability Service processing continues.
// *Action: Examine the Clusterware alert log for messages providing details of the error.  If the error is correctable, do so and then restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'.  If no messages are found or you do not understand how to correct the problem, contact Oracle Support Services.
0715, 1, "Oracle High Availability Service has timed out waiting for init.ohasd to be started."
// *Cause: The Oracle High Availability Service requires that initd start init.ohasd to successfully initialize.
// *Action: 1. Check the run level to ensure that you are in the correct runlevel using cluvfy ("cluvfy stage -pre crsinst -n <nodelist>"); 2. If the run level is correct, diagnose the reason for init.d not starting init.ohasd.



/ CRS Initialization Error
/
0800, 1, "Cluster Ready Service aborted due to failure to allocate memory. Details at %s in %s."
// *Cause: Memory allocation failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0801, 1, "Cluster Ready Service aborted due to failure to obtain identity of the running process. Details at %s in %s."
// *Cause: Failed to retrieve user id.
// *Action: Check <crs_home> owner and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0802, 1, "Cluster Ready Service aborted due to failure to run as privileged user. Details at %s in %s."
// *Cause: Cluster Ready Service was not running as privileged user.
// *Action: On Unix, restart Cluster Ready Service as privileged user using 'crsctl stop crs -f' followed by 'crsctl start crs'. On Windows, check the privileges of the Oracle High Availability Service and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs' If the problem persists, contact Oracle Support Services.
0803, 1, "Cluster Ready Service aborted due to failure to initialize the communication context. Details at %s in %s."
// *Cause: The network layer initialization failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0804, 1, "Cluster Ready Service aborted due to Oracle Cluster Registry error [%s]. Details at %s in %s."
// *Cause: Oracle Cluster Registry aborted with an error. Look at the associated error message to determine the underlying issue.
// *Action: Solve the underlying issue and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0805, 1, "Cluster Ready Service aborted due to failure to communicate with Cluster Synchronization Service with error [%d]. Details at %s in %s."
// *Cause: The Cluster Synchronization Service is unreachable.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0806, 1, "Cluster Ready Service aborted due to failure to retrieve the local node name. Details at %s in %s."
// *Cause: The Cluster Synchronization Service node name is not accessible.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0807, 1, "Cluster Ready Service aborted due to failure to check version compatibility. Details at %s in %s."
// *Cause: Oracle Cluster Registry content is not compatible with this version of Cluster Ready Service.
// *Action: Start the correct version of Cluster Ready Service. If the problem persists, contact Oracle Support Services.
0808, 1, "Cluster Ready Service aborted due to failure to retrieve ORA_CRS_HOME environment variable. Details at %s in %s."
// *Cause: An environment variable required by Cluster Ready Service failed to be set at initialization.
// *Action: Run 'rootcrs.pl -unlock' followed by 'rootcrs.pl -patch' and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0809, 1, "Cluster Ready Service aborted due to failure to initialize ORA_CRS_HOME path. Details at %s in %s."
// *Cause: Cluster Ready Service ORA_CRS_HOME path could not be initialized.
// *Action: Check for execute permissions on the Grid Infrastructure home or <crs_home> and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0810, 1, "Cluster Ready Service aborted due to failure to communicate with Event Management Service with error [%d]. Details at %s in %s."
// *Cause: The Event Management Service is unreachable.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0811, 1, "Cluster Ready Service aborted due to failure to build dependency graph. Details at %s in %s."
// *Cause: There exists inconsistencies in the resources dependencies.
// *Action: Check the resources dependencies and restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0812, 1, "Cluster Ready Service aborted due to failure to initialize the network layer with error [%d]. Details at %s in %s."
// *Cause: The network layer initialization failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0813, 1, "Cluster Ready Service aborted due to failure to initialize the network layer with error [%s]. Details at %s in %s."
// *Cause: The network layer initialization failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.
0814, 1, "Cluster Ready Service aborted due to failure to start thread with error [%d]. Details at %s in %s."
// *Cause: Thread creation failed.
// *Action: Restart Cluster Ready Service using 'crsctl stop crs -f' followed by 'crsctl start crs'. If the problem persists, contact Oracle Support Services.


//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
/
/   1001-1200: OCR specific messages. From clsdus.msg.
/
/   NOTE TO DEVELOPER:
/              When an OCR message is added or deleted, a corresponding
/              OLR message must be added or deleted if applicable.
/              Please do not fill holes in the message numbers because
/              the unused message numbers might be used by OLR messages.
/   NOTE TO TRANSLATOR:
/              These OCR messages should be translated almost identical
/              to the corresponding OLR messages (2101 - 2300).
/
//////////////////////////////////////////////////////////////////////////

1001, 0, "The OCR was formatted using version %d."
// *Cause: Successfully formatted the OCR location(s). 
// *Action: None.
1002, 3, "The OCR was restored from file %s."
// *Cause: The OCR was successfully restored from a backup file as requested
//         by the user.
// *Action: None.
1003, 0, "The OCR format was downgraded to version %d."
// *Cause: The OCR was successfully downgraded to an earlier block format
//         as requested by the user.
// *Action: None.
1004, 0, "The OCR was imported from %s."
// *Cause: Successfully imported the OCR contents from a file as requested
//         by the user.
// *Action: None
1005, 0, "The Oracle Clusterware upgrade was completed. Version has changed from [%d, %s] to [%d, %s]. Details in %s."
// *Cause: The Oracle Clusterware was successfully upgraded to a version.
// *Action: None.
1006, 0, "The OCR location %s is inaccessible. Details in %s."
// *Cause: An error occurred while accessing the OCR.
// *Action: Use the ocrcheck command to validate the accessibility of the
//          device and its block integrity. Check that the OCR location in
//          question has the correct permissions. Determine whether this
//          behavior is limited to one node or whether it occurs across all of
//          the nodes in the cluster.
//          Use the ocrconfig command with the -replace option to replace
//          the OCR location.
1007, 0, "The OCR/OCR mirror location was replaced by %s."
// *Cause: The OCR location was successfully replaced as requested by the user.
// *Action: None.
1008, 0, "Node %s is not responding to OCR requests. Details in %s."
// *Cause: Error in communicating to the OCR server on a peer node. This OCR
//         did not receive a notification regarding its peer's death within
//         the specified time.
// *Action: Contact Oracle Customer Support.
1009, 0, "The OCR configuration is invalid. Details in %s."
// *Cause: The OCR configuration on this node does not match the OCR 
//         configuration on the other nodes in the cluster.
// *Action: Determine the OCR configuration on the other nodes in the cluster 
//          on which Oracle Clusterware is running by using the ocrcheck
//          command. Run the ocrconfig command with the -repair option to
//          correct the OCR configuration on this node.
1010, 0, "The OCR mirror location %s was removed."
// *Cause: The OCR location was successfully removed as requested by the user.
// *Action: None.
1011, 0, "OCR cannot determine that the OCR content contains the latest updates. Details in %s."
// *Cause: The OCR could not be started. The OCR location configured on this
//         node does not have the necessary votes and might not have the
//         latest updates. 
// *Action: Ensure that the other nodes in the cluster have the same OCR
//          location configured. If the configuration on the other nodes in
//          the cluster does not match, then run the ocrconfig command with
//          the -repair option to correct the configuration on this node.
//          If the configurations on all of the nodes match, use the ocrdump
//          command to ensure that the existing OCR location has the latest
//          updates. Run the ocrconfig command with the -overwrite option to
//          correct the problem. If the se procedures do not correct the
//          problem, then contact Oracle Customer Support.
1012, 0, "The OCR service started on node %s."
// *Cause: The OCR was successfully started.
// *Action: None.
1013, 0, "The OCR location in an ASM disk group is inaccessible. Details in %s."
// *Cause: An error occurred while accessing the OCR file in an ASM disk group.
// *Action: Use the 'asmcmd' command to verify if the ASM instance is active. 
//          If the ASM instance aborted, it will be restarted automatically. 
//          Use 'ocrcheck -config' to discover the OCR locations configured,
//          and verify using 'asmcmd' that the disk group in question is 
//          mounted. Mount the disk group if it is not mounted. Validate if 
//          the behavior is limited to one node or whether it occurs across 
//          all of the nodes in the cluster. If nothing works, use the 
//          'ocrconfig' command with the '-replace' or '-delete' option 
//          to replace or remove the OCR location.
1014, 0, "Failed to import Oracle Cluster Registry from file %s"
// *Cause: Unable to read data from the import file and import to the 
//         cluster registry
// *Action: Check availability of the cluster registry and the details of the 
//          failure from the log file
1015, 0, "A request to terminate the Cluster Ready Service on node %s completed successfully. Details at %s in %s."
// *Cause: The Cluster Ready Service on the above listed node did not respond to an earlier 
//         request within the specified time. The Cluster Ready Service will be terminated to
//          prevent any possible cluster hangs. 
// *Action: Check the Oracle Clusterware alert log on the listed node for any problems. Check 
//          for any reason that might not allow the Cluster Ready Service to run optimally 
//          on the listed node. Verify network accessibility to the listed node from other nodes
//          in the cluster. If the problem persists, contact Oracle Support Services.
1016, 0, "The Cluster Ready Service on this node terminated because it detected a failure while upgrading the Oracle Cluster Registry format. Details at %s in %s."
// *Cause: The Cluster Ready Service on the node coordinating the upgrade of
//          the Oracle Cluster Registry format terminated.
// *Action: The Oracle Cluster Registry format upgrade will be completed 
//          by another node in the cluster. The Cluster Ready Service on the 
//          node listed above will be automatically restarted, and will be
//          able to function as soon as the upgrade completes. If the problem
//          persists, contact Oracle Support Services. 
1017, 0, "The Cluster Ready Service on this node terminated because it was unable to open the import file while upgrading the Oracle Cluster Registry format. Details at %s in %s."
// *Cause: There was a failure accessing the import file on this node. The 
//         Cluster Ready Service on this node may not have been active during
//         the Oracle Cluster Registry format upgrade.
// *Action: The Oracle Cluster Registry format upgrade will be completed 
//          by another node in the cluster. The Cluster Ready Service on this 
//          node will be automatically restarted, and will be able to function
//          as soon as the upgrade completes. If the problem persists, contact
//          Oracle Support Services. 
1018, 0, "The Cluster Ready Service on this node terminated because the OCR configuration on this node is invalid. Details at %s in %s."
// *Cause: The OCR configuration on this node did not match with the OCR 
//         configuration on the other nodes in the cluster.
// *Action: The OCR configuration on this node is automatically repaired and the
//          Cluster Ready Service will be automatically restarted. If the 
//          problem persists, contact Oracle Support Services. 
1019, 0, "The OCR Service exited on host %s. Details in %s"
// *Cause:  The OCR Service exited due to an internal error.
// *Action: Determine whether the service has restarted. Collect Clusterware
//          alert log and the CRSD log indicated in the message and contact
//          Oracle Support Services.
1020, 1, "The Oracle Cluster Registry has invalid contents. Details at %s in %s."
// *Cause: Some of the Oracle Cluster Registry contents were invalid.
// *Action: Check the log file indicated in the message for more details. Use 
//          the 'ocrcheck' command to detect errors, and the 'ocrdump' command
//          to review the registry contents. If problems exist, the registry may
//          need to be recovered or restored. If the problem persists, contact
//          Oracle Support Services.
1021, 1, "The Oracle Cluster Registry backup file in an ASM disk group is inaccessible. Details in %s."
// *Cause: Oracle Cluster Registry backup location did not exist, wasn't
//         mounted correctly, or did not have the required permissions.
// *Action: Ensure that the backup location exists, that it is mounted correctly
//          and visible to all nodes in the cluster, and that its permissions
//          are correct. Check the entries in the ASM alert log file for more
//          details.
1022, 0, "The Oracle Clusterware was forcibly upgraded without upgrading nodes %s. Version has changed from [%d, %s] to [%d, %s]. Details in %s."
// *Cause: Oracle Clusterware was forcibly upgraded when the above listed
//         nodes were not upgraded.
// *Action: Delete the above listed nodes using the procedure in the Clusterware
//          Administration and Deployment Guide.  If the nodes later become
//          accessible, they can be added back into the cluster.
/1023 is not applicable
/ 
/1024 is not applicable
/
1025, 0, "The Oracle Clusterware was upgraded to [%s] on all nodes, but the cluster operating version is still [%s]. Details in [%s]."
// *Cause: The cluster upgrade did not complete because the root upgrade script
//         failed on the last node, the root upgrade script was interrupted by
//         the user, or the cluster upgrade is ongoing.
// *Action: Check the Oracle Clusterware alert log on all nodes for any
//          problems. Rerun the root upgrade script on the last node to 
//          completion, and ensure that the cluster operating version has 
//          changed using the 'crsctl query crs activeversion' command. If the 
//          problem persists, run diagcollection.pl and contact Oracle Support 
//          Services.


///////////////////////////////////////////////////////////////////////////
/
/ 1101-1200 Clusterware upgrade specific messages
/
//////////////////////////////////////////////////////////////////////////

1101, 0, "Started to upgrade the OCR.\n"
// *Document: NO
1102, 0, "The OCR was successfully upgraded.\n"
// *Document: NO
1103, 0, "Started to upgrade the CRS.\n"
// *Document: NO
1104, 0, "The CRS was successfully upgraded.\n"
// *Document: NO
1105, 0, "Started to upgrade the CSS.\n"
// *Document: NO
1106, 0, "The CSS was successfully upgraded.\n"
// *Document: NO
1107, 0, "Started to upgrade the EVM.\n"
// *Document: NO
1108, 0, "The EVM was successfully upgraded.\n"
// *Document: NO
1109, 0, "Successfully upgraded the Oracle Clusterware.\n"
// *Document: NO

1110, 0, "The Oracle Clusterware upgrade is in unknown state [%d].\n"
// *Cause: There was an internal error upgrading the Oracle Clusterware.
// *Action: Retry the 'crsctl set crs activeversion' command. If the problem
//          persists, contact Oracle Support Services.

1111, 0, "Error upgrading the Oracle Clusterware. Details [%s].\n"
// *Cause: There was an internal error upgrading the Oracle Clusterware.
// *Action: Verify using the 'crsctl check crs' command that the CRS Service 
//          running. Retry the 'crsctl set crs activeversion' command. If the
//          problem persists, contact Oracle Support Services.

1112, 0, "Failed to set the Oracle Clusterware operating version %s"
// *Cause: There was an internal error upgrading the Oracle Clusterware.
// *Action: Retry the 'crsctl set crs activeversion' command. If the problem
//          persists, contact Oracle Support Services.

1113, 0, "Oracle Clusterware operating version was successfully set to %s\n"
// *Document: NO

1114, 0, "Invalid active version [%s] passed"
// *Cause: An invalid active version was passed.
// *Action: Use the 'crsctl query crs softwareversion' command to retrieve a 
//          valid active version. 

1115, 0, "Oracle Clusterware has already been upgraded.\n"
// *Cause: Oracle Clusterware is already running in highest possible operating
//         version.
// *Action: None

1116, 0, "Oracle Clusterware upgrade has been aborted.\n"
// *Cause: One of the Oracle Clusterware components have failed to upgrade
//         within the expected time.
// *Action: Check the Oracle Clusterware alert log and the CRS daemon log for
//          additional information.

1117, 0, "Error upgrading the Oracle Clusterware.\n"
// *Cause: An attempt was made to change the Oracle Clusterware operating
//         version before all nodes were upgraded.
// *Action: Run root.sh script on all nodes in the cluster. If the problem 
//          persists, contact Oracle Support Services.

1118, 0, "Started to upgrade the Oracle Clusterware. This operation may take a few minutes.\n"
// *Document: NO

1119, 0, "Unable to complete Oracle Clusterware upgrade while nodes %s have not yet upgraded\n"
// *Cause: An attempt was made to change the Oracle Clusterware operating
//         version before all nodes were upgraded.
// *Action: Run root.sh script and upgrade all nodes in the cluster before
//          retrying the 'crsctl set crs activeversion' command.

1120, 2, "Attempting to forcibly upgrade the Oracle Clusterware using only the nodes %s.\n"
// *Document: NO

1121, 2, "Oracle Clusterware was forcibly upgraded without upgrading nodes %s.\n"
// *Cause: Oracle Clusterware was forcibly upgraded when the above listed
//         nodes were not upgraded.
// *Action: Delete the above listed nodes using the procedure in the Clusterware
//          Administration and Deployment Guide.  If the nodes later become
//          accessible, they can be added back into the cluster.

1122, 0, "Forcibly upgraded the Oracle Clusterware.\n"
// *Document: NO

1123, 0, "Oracle Clusterware operating version was forcibly set to %s\n"
// *Document: NO

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   1201-1300: CRSD specific messages. From clsdus.msg.
/
/   NOTE TO DEVELOPER:
/              When a CRS message is added or deleted, a corresponding
/              OHAS message must be added or deleted if applicable.
/              Please do not fill holes in the message numbers because
/              the unused message numbers might be used by OHAS messages.
/   NOTE TO TRANSLATOR:
/              These CRS messages should be translated almost identical
/              to the corresponding OHAS messages (1301 - 1400).
/
/
///////////////////////////////////////////////////////////////////////////

1201, 0, "CRSD started on node %s."
// *Cause: CRSD has started, possibly due to a CRS start, or a node reboot or
//         a CRSD restart.    
// *Action: None Required. You can run the command 'crsctl check crsd' to
//          validate the health of the CRSD.
1202, 0, "CRSD aborted on node %s. Error [%s]. Details in %s."
// *Cause: Fatal Internal Error. Check the CRSD log file to determine the cause.
// *Action: Determine whether the CRSD gets auto-started.
1203, 0, "Failover failed for the CRS resource %s. Details in %s."
// *Cause:  Failover failed due to an internal error. Examine the contents of
//           the CRSD log file to determine the cause.
// *Action: None.
1204, 0, "Recovering CRS resources for node %s."
// *Cause: CRS resources are being recovered, possibly because the cluster
//         node is starting up online. 
// *Action: Check the status of the resources using the 'crsctl status resource' command.
1205, 0, "Auto-start failed for the CRS resource %s. Details in %s."
// *Cause: This message comes up when the auto-start for the resource has
//         failed during a reboot of the cluster node. 
// *Action: Start the resources using the 'crsctl start resource' command.
1206, 0, "Resource %s is in the UNKNOWN state. Make sure the resource is completely stopped, then use the 'crsctl stop -f' command."
// *Cause:  Resource went into an unknown state because the check or the stop
//          action on the resource failed.
// *Action:  Make sure the resource is completely stopped, then use the 'crsctl stop -f' command.
1207, 0, "There are no more restart attempts left for resource %s. Restart the resource manually using the crsctl command."
// *Cause: The Oracle Clusterware is no longer attempting to restart the
//         resource because the resource has failed and the Oracle Clusterware
//         has exhausted the maximum number of restart attempts.
// *Action: Use the 'crsctl start' command to restart the resource manually.
1208, 1, "Cluster Ready Service terminating, unable to start successfully. Details at %s in %s."
// *Cause: Cluster Ready Service could not initialize successfully. 
// *Action: Restart Cluster Ready Service using the command 'crsctl start clusterware'. If the problem persists, contact Oracle Support Services.
1209, 1, "Cluster Ready Service terminating, failed to register with group '%s'. Details at %s in %s."
// *Cause: Cluster Ready Service could not initialize successfully.
// *Action: Restart Cluster Ready Service using the command 'crsctl start clusterware'. If the problem persists, contact Oracle Support Services.
1210, 1, "Cluster Ready Service failed to update group data. Details at %s in %s."
// *Cause: Cluster Ready Service failed to update the group private data with new master.
// *Action: Restart Cluster Ready Service using the command 'crsctl start clusterware'. If the problem persists, contact Oracle Support Services.
1211, 1, "Cluster Ready Service noticed abnormal termination by Cluster Synchronization Service. Details at %s in %s."
// *Cause: Cluster Ready Service terminating due to abnormal termination of Cluster Synchronization Service layer. 
// *Action: Contact Oracle Support Services.
1212, 1, "Cluster Ready Service received invalid update for group private data. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.

/CRSSHR messages here
1213, 1, "Cluster Ready Service failed to retrieve user information. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
1214, 1, "Cluster Ready Service failed to initialize OLR context. Details at %s in %s."
// *Cause: Cluster Ready Service unable to access local registry.
// *Action: Use the ocrcheck utility to detect errors in the OLR. If problems exist, the registry may need to be recovered or restored.
1215, 1, "Cluster Ready Service could not get the local node number. Details at %s in %s."
// *Cause: Cluster Ready Service could not retrieve the local node incarnation number.
// *Action: Contact Oracle Support Services.
1216, 1, "Cluster Ready Service could not determine node list. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
1217, 1, "Cluster Ready Service unable to get node name. Details at %s in %s."
// *Cause: Cluster Ready Service could not determine node name. 
// *Action: Contact Oracle Support Services.
1218, 1, "Cluster Ready Service error during initialization. Details at %s in %s."
// *Cause: Cluster Ready Service could not initialize underlying layers successfully.
// *Action: Contact Oracle Support Services.
1219, 1, "Cluster Synchronization Service not available. Details at %s in %s."
// *Cause: Cluster Ready Service was unable to initialize access to CSS, which is required. 
// *Action: Contact Oracle Support Services.
1220, 1, "Cluster Ready Service could not retrieve local node number. Details at %s in %s."
// *Cause: Cluster Ready Service could not retrieve node number for local node.
// *Action: Contact Oracle Support Services.
1221, 1, "Cluster Ready Service failed to retrieve local node name. Details at %s in %s."
// *Cause: Cluster Ready Service could not retrieve node name.
// *Action: Contact Oracle Support Services.
1222, 1, "Cluster Ready Service failed to  retrieve maximum group size. Details at %s in %s."
// *Cause: Cluster Ready Service could not retrieve value for maximum group size. 
// *Action: Contact Oracle Support Services.
1223, 1, "Cluster Ready Service error while reading cluster active version. Details at %s in %s."
// *Cause: Could not retrieve cluster active version.
// *Action: Contact Oracle Support Services.
/ UiServer messages.
1224, 1, "Server authentication exception encountered, exception text is '%s'. Details at %s in %s."
// *Cause: Cluster Ready Service encountered error while authenticating user.
// *Action: This is an internal error. Contact Oracle Support Services.
1225, 1, "Invalid identity exception encountered, exception text is '%s'. Details at %s in %s."
// *Cause: Cluster Ready Service could not verify user identity.
// *Action: This is an internal error. Contact Oracle Support Services.
1226, 1, "Failed to create message to send to policy engine. Details at %s in %s."
// *Cause: Cluster Ready Service encountered communication error.
// *Action: This is an internal error. Contact Oracle Support Services.
1227, 1, "Error during initialization of communication subsystem. Details at %s in %s."
// *Cause: Cluster Ready Service encountered communication error during initialization.
// *Action: This is an internal error. Contact Oracle Support Services.
1228, 1, "Error while setting up user interface server. Details at %s in %s."
// *Cause: Cluster Ready Service encountered communication error.
// *Action: This is an internal error. Contact Oracle Support Services.
1229, 1, "Error while listening for events. Details at %s in %s."
// *Cause: Cluster Ready Service encountered communication error.
// *Action: This is an internal error. Contact Oracle Support Services.
1231, 1, "Failed to open key '%s' in OCR. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: This is an internal error. Contact Oracle Support Services.
1232, 1, "Could not get security attribute for system key '%s' in OCR. Details at %s in %s."
// *Cause: Encountered error while reading system key attributes in OCR.
// *Action: This is an internal error. Contact Oracle Support Services.
1233, 1, "Failed to initialize batch handler for OCR. Details at %s in %s."
// *Cause: Could not initialize batch handler for multiwrite in OCR.
// *Action: This is an internal error. Contact Oracle Support Services.
1234, 1, "Encountered error while setting key value for key '%s' in OCR. Details at %s in %s."
// *Cause: Encountered an error while executing a batch write in OCR.
// *Action: This is an internal error. Contact Oracle Support Services.
1235, 1, "Error while executing batch for multi writes in OCR. Details at %s in %s."
// *Cause: Encountered an error while executing a batch write in OCR.
// *Action: This is an internal error. Contact Oracle Support Services.
1236, 1, "Error enumerating subkeys for key '%s' in OCR. Details at %s in %s."
// *Cause: Encountered an error while reading subkey values in OCR.
// *Action: This is an internal error. Contact Oracle Support Services.
1237, 1, "Failed to retrieve the maximum value supported in OCR. Details at %s in %s."
// *Cause: Could not read the maximum value size from registry.
// *Action: This is an internal error. Contact Oracle Support Services.
1238, 1, "Failed to add a delete key operation for key '%s' to a batch in OCR. Details at %s in %s."
// *Cause: Encountered internal error while deleting key in OCR.
// *Action: This is an internal error. Contact Oracle Support Services.
1239, 0, "Cluster Ready Service aborted due to an unexpected error [%s]. Details at %s in %s."
// *Cause: This is an unexpected error. Look at the associated error message to fix the underlying issue.
// *Action: If the problem persists, contact Oracle Support Services.

///////////////////////////////////////////////////////////////////////////
/
/   1301-1400: OHASD specific messages.
/
/    NOTE TO DEVELOPER:
/              OHAS message number = CRS message number + 100
/              When an OHAS message is added or deleted, a corresponding
/              CRS message must be added or deleted if applicable.
/              Please do not fill holes in the message numbers because
/              the unused message numbers might be used by CRS messages.
/    NOTE TO TRANSLATOR:
/              These OHAS messages should be translated almost identical
/              to the corresponding CRS messages (1201 - 1300).
/
/
///////////////////////////////////////////////////////////////////////////

1301, 0, "Oracle High Availability Service started on node %s."
// *Cause: Oracle High Availability Service has started, possibly due to a Clusterware start, or a node reboot.
// *Action: None Required.
1302, 0, "Oracle High Availability Service aborted on node %s. Error [%s]. Details in %s."
// *Cause: Fatal Internal Error. Check the Oracle High Availability Service log file to determine the cause.
// *Action: Determine whether the Oracle High Availability Service gets auto-started.
1303, 0, "Failover failed for the OHAS resource %s. Details in %s."
// *Cause:  Failover processing for the specified resource did not complete. Examine the contents of
//           the Oracle High Availability Service log file to determine the cause.
// *Action: None.
1304, 0, "Recovering OHAS resources for node %s."
// *Cause: Oracle High Availability Service resources are being recovered, possibly because the cluster
//         node is starting up online. 
// *Action: Check the status of the resources using the crsctl command.
1305, 0, "Auto-start failed for the OHAS resource %s. Details in %s."
// *Cause: This message comes up when the auto-start for the resource has
//         failed during a reboot of the cluster node. 
// *Action: Start the resources using the 'crsctl start resource' command.
1306, 0, "Resource %s is in an unknown state. Make sure the resource is completely stopped, then use the 'crsctl stop -f' command."
// *Cause:  Resource went into an unknown state because the check or the stop
//          action on the resource failed.
// *Action: Make sure the resource is completely stopped, then use the 'crsctl stop -f' command.
1307, 0, "There are no more restart attempts left for resource %s. Restart the resource manually using the crsctl command."
// *Cause: The Oracle Clusterware is no longer attempting to restart the
//         resource because the resource has failed and the Oracle Clusterware
//         has exhausted the maximum number of restart attempts.
// *Action: Use the 'crsctl start resource' command to restart the resource manually.
1308, 1, "Oracle High Availability Service terminating, unable to start successfully. Details at %s in %s."
// *Cause: Oracle High Availability Service could not initialize successfully. 
// *Action: Restart your clusterware installation. If the problem persists, contact Oracle Support Services.
1309, 1, "Oracle High Availability Service terminating, failed to register with group '%s'. Details at %s in %s."
// *Cause: Oracle High Availability Service could not initialize successfully.
// *Action: Restart your clusterware installation. If the problem persists, contact Oracle Support Services.
1310, 1, "Oracle High Availability Service failed to update group data. Details at %s in %s."
// *Cause: Oracle High Availability Service failed to update the group private data with new master.
// *Action: Restart your clusterware installation. If the problem persists, contact Oracle Support Services.
1311, 1, "Oracle High Availability Service noticed abnormal termination by Cluster Synchronization Service. Details at %s in %s."
// *Cause: Oracle High Availability Service terminating due to abnormal termination of Cluster Synchronization Service layer. 
// *Action: Contact Oracle Support Services.
1312, 1, "Oracle High Availability Service received invalid update for group private data. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.

/CRSSHR messages here
1313, 1, "Oracle High Availability Service failed to retrieve user information. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
1314, 1, "Oracle High Availability Service failed to initialize OLR context. Details at %s in %s."
// *Cause: Oracle High Availability Service unable to access local registry.
// *Action: Use the ocrcheck utility to detect errors in the OLR. If problems exist, the registry may need to be recovered or restored.
1315, 1, "Oracle High Availability Service could not get the local node number. Details at %s in %s."
// *Cause: Oracle High Availability Service could not retrieve the local node incarnation number.
// *Action: Contact Oracle Support Services.
1316, 1, "Oracle High Availability Service could not determine node list. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
1317, 1, "Oracle High Availability Service unable to get node name. Details at %s in %s."
// *Cause: Oracle High Availability Service could not determine node name. 
// *Action: Contact Oracle Support Services.
1318, 1, "Oracle High Availability Service error during initialization. Details at %s in %s."
// *Cause: Oracle High Availability Service could not initialize underlying layers successfully.
// *Action: Contact Oracle Support Services.
1319, 1, "Cluster Synchronization Service not available. Details at %s in %s."
// *Cause: Oracle High Availability Service was unable to initialize access to CSS, which is required. 
// *Action: Contact Oracle Support Services.
1320, 1, "Oracle High Availability Service could not retrieve local node number. Details at %s in %s."
// *Cause: Oracle High Availability Service could not retrieve node number for local node.
// *Action: Contact Oracle Support Services.
1321, 1, "Oracle High Availability Service failed to retrieve local node name. Details at %s in %s."
// *Cause: Oracle High Availability Service could not retrieve node name.
// *Action: Contact Oracle Support Services.
1322, 1, "Oracle High Availability Service failed to  retrieve maximum group size. Details at %s in %s."
// *Cause: Oracle High Availability Service could not retrieve value for maximum group size. 
// *Action: Contact Oracle Support Services.
1323, 1, "Oracle High Availability Service error while reading cluster active version. Details at %s in %s."
// *Cause: Could not retrieve cluster active version.
// *Action: Contact Oracle Support Services.
/ UiServer messages.
1324, 1, "Server authentication exception encountered, exception text is '%s'. Details at %s in %s."
// *Cause: Oracle High Availability Service encountered error while authenticating user.
// *Action: This is an internal error. Contact Oracle Support Services.
1325, 1, "Invalid identity exception encountered, exception text is '%s'. Details at %s in %s."
// *Cause: Oracle High Availability Service could not verify user identity.
// *Action: This is an internal error. Contact Oracle Support Services.
1326, 1, "Failed to create message to send to policy engine. Details at %s in %s."
// *Cause: Oracle High Availability Service encountered communication error.
// *Action: This is an internal error. Contact Oracle Support Services.
1327, 1, "Error during initialization of communication subsystem. Details at %s in %s."
// *Cause: Oracle High Availability Service encountered communication error during initialization.
// *Action: This is an internal error. Contact Oracle Support Services.
1328, 1, "Error while setting up user interface server. Details at %s in %s."
// *Cause: Oracle High Availability Service encountered communication error.
// *Action: This is an internal error. Contact Oracle Support Services..
1329, 1, "Error while listening for events. Details at %s in %s."
// *Cause: Oracle High Availability Service encountered communication error.
// *Action: This is an internal error. Contact Oracle Support Services..
1330, 0, "Oracle High Availability Services aborted due to internal error."
// *Cause: Fatal Internal Error. Check the Oracle High Availability Service log file to determine the cause.
// *Action: Determine whether the Oracle High Availability Service gets auto-started.
1331, 1, "Failed to open key '%s' in OLR. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: This is an internal error. Contact Oracle Support Services.
1332, 1, "Could not get security attribute for system key '%s' in OLR. Details at %s in %s."
// *Cause: Encountered error while reading system key attributes in OLR.
// *Action: This is an internal error. Contact Oracle Support Services.
1333, 1, "Failed to initialize batch handler for OLR. Details at %s in %s."
// *Cause: Could not initialize batch handler for multiwrite in OLR.
// *Action: This is an internal error. Contact Oracle Support Services.
1334, 1, "Encountered error while setting key value for key '%s' in OLR. Details at %s in %s."
// *Cause: Encountered an error while executing a batch write in OLR.
// *Action: This is an internal error. Contact Oracle Support Services.
1335, 1, "Error while executing batch for multi writes in OLR. Details at %s in %s."
// *Cause: Encountered an error while executing a batch write in OLR.
// *Action: This is an internal error. Contact Oracle Support Services.
1336, 1, "Error enumerating subkeys for key '%s' in OLR. Details at %s in %s."
// *Cause: Encountered an error while reading subkey values in OLR.
// *Action: This is an internal error. Contact Oracle Support Services.
1337, 1, "Failed to retrieve the maximum value supported in OLR. Details at %s in %s."
// *Cause: Could not read the maximum value size from registry.
// *Action: This is an internal error. Contact Oracle Support Services.
1338, 1, "Failed to add a delete key operation for key '%s' to a batch in OLR. Details at %s in %s."
// *Cause: Encountered internal error while deleting key in OLR.
// *Action: This is an internal error. Contact Oracle Support Services.
1339, 0, "Oracle High Availability Service aborted due to an unexpected error [%s]. Details at %s in %s."
// *Cause: Look at the associated error message to fix the underlying issue.
// *Action: If the problem persists, contact Oracle Support Services.

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   1401-1600: EVMD specific messages. From clsdus.msg.
/
///////////////////////////////////////////////////////////////////////////

1401, 0, "EVMD started on node %s."
// *Cause: EVMD has started either because of a CRS start, a node reboot,
//         or an EVMD restart. 
// *Action: None required. You can run the 'crsctl check evmd' command to validate the health of EVMD.
1402, 0, "EVMD aborted on node %s. Error [%s]. Details in %s."
// *Cause:  EVMD has aborted due to an internal error. Check the EVMD log file
//          to determine the cause.
// *Action: Determine whether the EVMD is auto-started and contact Oracle Support Services.
1403, 0, "The Event Management Service terminated on node %s. Listening port %d is in use by another application. Details in %s."
// *Cause:  The Event Management Service has aborted because the
//          configured listening port is being used by another
//          application on this node.
// *Action: Make the listening port listed above available. Restart
//          the Event Management Service using 'crsctl start crs' or
//          'crsctl start cluster' command. 
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   1601-1800: CSSD specific messages. From clsdus.msg.
/
///////////////////////////////////////////////////////////////////////////

1601, 0, "CSSD Reconfiguration complete. Active nodes are %s."
// *Cause:  A node joined or left the cluster.
// *Action: None.
1602, 0, "CSSD aborted on node %s. Error [%s]; details in %s."
// *Cause:  The CSS daemon aborted on the listed node with the listed return
//          code.
// *Action: Collect the CSS daemon logs from all nodes and any CSS daemon core
//          files and contact Oracle Support.
1603, 0, "CSSD on node %s shutdown by user."
// *Cause:  The CSS daemon on the listed node was terminated by a user.
// *Action: None.
1604, 0, "CSSD voting file is offline: %s; details at %s in %s."
// *Cause:  The listed voting file became unusable on the local node.
// *Action: Verify that the filesystem containing the listed voting file is
//          available on the local node.
1605, 0, "CSSD voting file is online: %s; details in %s."
// *Cause:  The CSS daemon has detected a valid configured voting file.
// *Action: None.
1606, 0, "The number of voting files available, %d, is less than the minimum number of voting files required, %d, resulting in CSSD termination to ensure data integrity; details at %s in %s"
// *Cause:  The number of voting files has decreased to a number of files
//          that is insufficient.
// *Action: Locate previous 1604, 1613, 1614 and 1615 messages and take
//          action as indicated by those messages.
1607, 0, "Node %s is being evicted in cluster incarnation %d; details at %s in %s."
// *Cause:  The local node has detected that the indicated node is still
//          active, but not able to communicate with this node, so is
//          forcibly removing the indicated node from the cluster.
// *Action: Collect the CSS daemon logs from all nodes and any CSS daemon core
//          files and contact Oracle Support.
1608, 0, "This node was evicted by node %d, %s; details at %s in %s."
// *Cause:  The local node was evicted by the indicated node.
// *Action: Collect the CSS daemon logs from all nodes and any CSS daemon core
//          files and contact Oracle Support.
1609, 0, "This node is unable to communicate with other nodes in the cluster and is going down to preserve cluster integrity; details at %s in %s."
// *Cause:  Communication was lost with some nodes of the cluster and this
//          node detected that another sub-cluster was designated to be the 
//          surviving sub-cluster. This node went down to preserve data
//          integrity.
// *Action: Verify all network connections between cluster nodes and
//          repair any problematic connections. If there do not appear
//          to be any network problems, 
//          1. collect the CSS daemon logs, system messages and 
//             any CSS daemon core files from all nodes and 
//          2. contact Oracle Support.
/
1610,0,"Network communication with node %s (%d) missing for 90%% of timeout interval.  Removal of this node from cluster in %d.%03d seconds"
// *Cause:  Did not receive heartbeat messages from the node. This could be
//          due to network problems or failure of the listed node.
// *Action: Check if the private interconnect network used by cluster is
//          functioning properly, including all the cables, network cards,
//          switches/routers etc. between this node and listed node. Correct
//          any problems discovered.

1611,0,"Network communication with node %s (%d) missing for 75%% of timeout interval.  Removal of this node from cluster in %d.%03d seconds"
// *Cause:  Did not receive heartbeat messages from the node. This could be
//          due to network problems or failure of the listed node.
// *Action: Check if the private interconnect network used by cluster is
//          functioning properly, including all the cables, network cards,
//          switches/routers etc. between this node and listed node. Correct
//          any problems discovered.
1612,0,"Network communication with node %s (%d) missing for 50%% of timeout interval.  Removal of this node from cluster in %d.%03d seconds"
// *Cause:  Did not receive heartbeat messages from the node. This could be
//          due to network problems or failure of listed node.
// *Action: Check if the private interconnect network used by cluster is
//          functioning properly, including all the cables, network cards,
//          switches/routers etc. between this node and listed node. Correct
//          any problems discovered.

1613,0,"No I/O has completed after 90%% of the maximum interval. Voting file %s will be considered not functional in %d milliseconds"
// *Cause: Voting device I/O has not completed for a long time. This could be due  
//         some error with the device the voting file is on or in some element
//         in the path of the I/O to the device.
// *Action:Verify that the device is working properly including all elements
//         in the I/O path. The voting file listed will be considered inactive
//         in the number of milliseconds specified. Failure of a majority of
//         devices will result in node reboot.

1614,0,"No I/O has completed after 75%% of the maximum interval. Voting file %s will be considered not functional in %d milliseconds"
// *Cause: Voting device I/O has not completed for a long time. This could be due  
//         some error with the device the voting file is on or in some element
//         in the path of the I/O to the device.
// *Action:Verify that the device is working properly including all elements
//         in the I/O path. The voting file listed will be considered inactive
//         in the number of milliseconds specified. Failure of a majority of
//         devices will result in node reboot.

1615,0,"No I/O has completed after 50%% of the maximum interval. Voting file %s will be considered not functional in %d milliseconds"
// *Cause: Voting device I/O has not completed for a long time. This could be due  
//         some error with the device the voting file is on or in some element
//         in the path of the I/O to the device.
// *Action:Verify that the device is working properly including all elements
//         in the I/O path. The voting file listed will be considered inactive
//         in the number of milliseconds specified. Failure of a majority of
//         devices will result in node reboot.

1616,0, "The BMC device used for IPMI at IP address %s is not properly configured for ADMIN access; details at %s in %s"
// *Cause: The IPMI BMC is not configured to support the ADMIN access methods
//          required by Oracle Clusterware.
// *Action: Consult the clusterware admin manual for proper procedures in 
//          configuring BMC. Use the BMC configuration tool (ipmitool 
//          or ipmiutil) command to check and verify
//          that the current configuration supports either MD5 or password
//          validation for ADMIN access.

1617,0,"The information required to do node kill for node %s is incomplete; details at %s in %s" 
// *Cause: Incomplete config information stored in Cluster Registry for node 
//         kill.
// *Action: Make sure all the information pertaining to the node kill method
/           being employed is present.
        
1618,0,"The requested node kill information change could not be validated by node %s; details at %s in %s"
// *Cause: Unable to validate the node kill information for this node.
// *Action: Additional information can be found in the CRS alert log of 
//          the node that performed the validation.

1619,0,"The node kill information of node %s could not be validated by this node due to failure in connecting to the IPMI device; details at %s in %s"
// *Cause: Unable to validate the node kill information for this node.
// *Action:  Additional information can be found in the CSSD logs.

1620,0,"The node kill information of node %s could not be validated by this node due to invalid authorization information; details at %s in %s"     
// *Cause: Unable to validate the kill information for this node.
// *Action:  Additional information can be found in the CSSD logs.

1621,0,"The IPMI configuration data for this node stored in the Oracle registry is incomplete; details at %s in %s"
// *Cause: All the necessary information such as IPMI username, password and
//         IP address are not present.
// *Action: Make sure all the information(BMC IPMI username, password and
//          IP address) are present. Use commands 'crsctl set css ipmiaddr' 
//          and 'crsctl set css ipmiadmin' for this.

1622,0,"The IPMI node kill information could not be validated due to inability to connect to the IPMI device at BMC IP address provided %s; details at %s in %s"
// *Cause: Unable to validate the BMC IPMI IP address provided.
// *Action:  Additional information can be found in the CSSD logs.

1623,0,"The IPMI node kill information of BMC at IP address %s could not be validated due to invalid authorization information. The BMC username provided is '%s'; details at %s in %s"     
// *Cause: Unable to validate the BMC IPMI UserName and password provided.
// *Action:  Additional information can be found in the CSSD logs.

1624,0,"The requested Node kill information change succeeds vacuously because there is no other node in cluster to validate."
// *Cause: Unable to validate the credentials because this is the sole node in 
//         the cluster.
// *Action: To complete the valdidation, shut down the clusterware stack on 
//         this node, start another node and restart the stack on this node.

1625,0,"Node %s, number %d, was shut down"
//  *Cause: A Clustware stack shutdown command was issued for a node in the
//          cluster and was observed by this node.
//  *Action: None required.

1626,0,"A Configuration change request completed successfully"
//  *Cause:A Configuration change request completed successfully.
//  *Action:None required.

1627,0,"A Configuration change request failed because another configuration change is in progress; Details at %s in %s"
//  *Cause:Another configuration change is in still in progress.
//  *Action:Wait until the other command completes and reissue
//          the command if necessary. Message 1626 would be printed
//          if the command succeeds.

1628,0,"A Configuration change request failed because read of existing voting files failed; Details at %s in %s"
//  *Cause:CSSD was not able to read the lease blocks of a majority of Voting
//         files which is an indication of a problem with the voting files.  
//  *Action:Run the command 'crsctl query css votedisk' to get the list of currently working
//          voting files. User may delete problematic voting file or use a different set.

1629,0,"A Configuration change request failed because write to new voting files failed; Details at %s in %s"
//  *Cause:A voting file write failed, causing the associated configuration change
//         to fail.  This often results from adding a voting file that is not accessible to
//         one or more nodes.
//  *Action:Confirm that voting files added in a configuration change are accessible
//          and writeable from all cluster nodes.  If they are, contact Oracle Customer
//          Support.

1630,0,"A configuration change request failed because not all the new voting files were discovered; Details at %s in %s"
// *Cause:  One or more of the voting files being added were not discovered.
//          Message 1638 identifies the unique ID(s) of the file(s) that
//          could not be found.
// *Action: Verify if the discovery string is adequate to discover the new
//          voting files. If not, modify discovery string using command
//          'crsctl replace discoverystring xxxxx'.

1631,0,"A configuration change request failed because one or more nodes are not a sufficient Clusterware version level; Details at %s in %s"
// *Cause:  One ore more nodes are not a sufficient version level.
// *Action: Configuration change would not be successful until all nodes are at
//          at the latest version. Try after all the nodes are upgraded.
            
1632, 0, "Node %s is being removed from the cluster in cluster incarnation %d"
// *Cause:  The local node is removing the indicated node from the cluster
//          because it appears to be dead.
// *Action: Verify that the node that was removed, or the Oracle Clusterware
//          on that node, was down.  The CRS alert log of the node that was
//          removed has information regarding why the node, or clusterware
//          on the node, was no longer active.  If the node was still up
//          and Oracle Clusterware still active on that node, collect the
//          CSS daemon logs from all nodes and any CSS daemon core files
//          and contact Oracle Support.

1633, 0, "CSSD failed to register group %s in vendor clusterware; details at %s in %s"
// *Cause:  The local node is not able to register the group of
//          vendor clusterware. 
// *Action: Verify that the vendor clusterware is installed and configured correctly. 

1634, 0, "CSSD is unable to determine cluster name; details at %s in %s"
// *Cause:  Name of the cluster cannot be determined from configuration.
// *Action: Verify that Oracle Clusterware installation was successful.

1635, 0, "CSSSD failed to initialize vendor clusterware; details at %s in %s"
// *Cause:  The local node is not able to attach vendor clusterware. 
// *Action: Verify that the vendor clusterware is installed and configured correctly. 

1636, 0, "The CSS daemon was started in exclusive mode but found an active CSS daemon on node %s and is terminating; details at %s in %s"
// *Cause:  The CSS daemon was started in exclusive mode, which requires
//          that the clusterware stack is down on all other nodes to ensure
//          data integrity.  A CSS daemon was detected on another node,
//          so the CSS daemon on this node is terminating.
// *Action: Stop the Oracle clusterware stack that is running on the
//          indicated node.

1637, 0, "Unable to locate configured voting file with ID %s; details at %s in %s"
// *Cause:  The voting file with unique the ID indicated in the message
//          was not found during the voting file discovery phase of CSS
//          initialization.
// *Action: Verify that all configured voting files are accessible on this
//          node.  Any voting files that are not accessible should be
//          removed and replaced with accessible voting files using the
//          appropriate 'crsctl' commands.

1638, 0, "Unable to locate voting file with ID %s that is being added to the list of configured voting files; details at %s in %s"
// *Cause:  The voting file with the unique ID indicated in the message
//          was not found during the voting file discovery phase of CSS
//          initialization.  This voting file is in the process of being
//          added to the list of configured voting files.
// *Action: Verify that all voting files to be added are accessible on this
//          node.  Any voting files that are not accessible should be
//          removed and replaced with accessible voting files using the
//          appropriate 'crsctl' commands.

1639, 0, "Rejecting configuration change %u:%u because another configuration change is already in progress; details at %s in %s"
// *Cause:  A configuration change was requested, but another configuration
//          change is already in progress and only one configuration change
//          may be processed at a time.
// *Action: Wait for the current configuration change to complete, then
//          resubmit this configuration change.

1640, 0, "Rejecting configuration change %u:%u because one or more new voting files in the new configuration could not be found; details at %s in %s"
// *Cause:  A configuration change that involved the addition of voting
//          files is being rejected because some of the new voting files
//          were not located.
// *Action: Verify that the voting file name is correct and that it is
//          accessible on this node, if the voting files are not managed
//          by ASM.  Message number 1638 provides greater detail.

1641, 0, "Rejecting configuration change %u:%u because only %u of the required %u voting files of the new configuration were located; details at %s in %s"
// *Cause:  A configuration change that involved a change to the list of
//          voting files is being rejected because a sufficient number
//          of voting files in the new configuration could not be 
//          located.
// *Action: Verify that all voting files in the new configuration
//          are accessible on this node.

1642, 0,"Node %d is using a different CSS configuration from the one used by this node; this node is terminating to preserve integrity; details at %s in %s"
// *Cause:  Another node in the cluster is using a different set of 
//          CSS configuration values, such as misscount or voting files.
//          Inconsistency can result in data corruption, so this node is
//          terminating to avoid data corruption.
// *Action: Collect Clusterware alert log and the CSSD log indicated in
//          the message as well as the CSS daemon logs of all other nodes
//          in the cluster and contact Oracle Support Services.

1643 ,0, "Failed to format the CSS voting disk %s"
// *Cause:  Problems were encountered attempting to access the voting file.
// *Action: Verify that the voting file can be accessed, the file exists,
//          has the proper ownership and permissions, etc.

1644, 0, "The initialization of the EXADATA fencing facility failed in start with error ORA-%d; details at %s in %s"
// *Cause:  The start of the initialization of the EXADATA fencing facility
//          failed with the error code shown.
// *Action: See the Action section of the error message shown.

1645, 0, "The initialization of the EXADATA fencing facility failed in completion with error ORA-%d; details at %s in %s"
// *Cause:  The completion of the initialization of the EXADATA fencing
//          facility failed with the error code shown.
// *Action: See the Action section of the error message shown.

1646, 0, "Creation of a EXADATA fence identifier failed with error ORA-%d; details at %s in %s"
// *Cause:  An attempt to create an identifier for a fence to an EXADATA
//          device failed with the error code shown.
// *Action: See the Action section of the error message shown.

1647, 0, "Initialization of a EXADATA fence failed with error ORA-%d; details at %s in %s"
// *Cause:  An attempt to initiate a fence to an EXADATA device failed with
//          the error code shown.
// *Action: See the Action section of the error message shown.

1648, 0, "Completion of queued EXADATA fence requests failed with error ORA-%d; details at %s in %s"
// *Cause:  Previously queued fence requests to an EXADATA device failed with
//          the error code shown.
// *Action: See the Action section of the error message shown.

1649, 0, "An I/O error occured for voting file: %s; details at %s in %s."
// *Cause:  The listed voting file became inaccessible. 
// *Action: Verify that the filesystem containing the listed voting file is
//          available on the local node.

1650,0,"Configuration change %u:%u rejected by node %u %s; details at %s in %s"
// *Cause: A new configuration change request from this node was not
//         accepted due to another node rejecting the change.
// *Action: Check the CRS alert log of the node rejecting this configuration
//          change for more details.

1651,0,"Configuration change %u:%u rejected because it would make the active version of node %u lower than the current setting %s of this node; details at %s in %s"
// *Cause:  A new configuration change request from another node was not
//          accepted because the new Active Version in the request is lower 
//          than this node's Active Version.
// *Action: Ensure that the new Active Version is not lower than the current 
//          Active Version of the nodes in the cluster.

1652,0,"Starting clean up of CRSD resources."
// *Cause:  Clean up of the resources registered in CRSD started.
// *Action: None

1653,0,"The clean up of the CRSD resources failed."
// *Cause:  Clean up of the resources registered in CRSD failed.
// *Action: Check the CRS alert log.

1654,0,"Clean up of CRSD resources finished successfully."
// *Cause:  Clean up of the resources registered in CRSD finished.
// *Action: None

1655, 0, "CSSD on node %s detected a problem and started to shutdown."
// *Cause:  The CSS daemon on the listed node detected a problem and started to shutdown.
// *Action: Check the CRS alert log.

1656,0,"The CSS daemon is terminating due to a fatal error; Details at %s in %s"
// *Cause:  A fatal error occurred during CSS daemon processing.
// *Action: Check for prior errors logged in the alert log. Correct any
//          errors that can be corrected.  If there are no errors shown,
//          or the errors cannot be resolved, contact Oracle support

1657,0,"Unable to obtain the voting file discovery string; Details at %s in %s"
// *Cause:  An attempt to obtain the voting file discovery string from
//          the profile failed, causing the CSS daemon to fail.
// *Action: Collect the Clusterware alert log and the CSSD log of this
//          node as well as all CSS daemon logs of all other nodes in the
//          cluster and contact Oracle Support Services.

1658,0,"There is a mismatch of the initial cluster incarnation among the cluster nodes; Details at %s in %s"
// *Cause:  An internal error occurred.
// *Action: Collect the Clusterware alert log and the CSSD log of this
//          node as well as all CSS daemon logs of all other nodes in the
//          cluster and contact Oracle Support Services.

1659,0,"An attempt to kill node %s failed; Details at %s in %s"
// *Cause:  To protect data integrity a node kill was attempted for
//          the indicated node, but it failed.
// *Action: Collect the Clusterware alert log and the CSSD log of this
//          node as well as the CSS daemon logs of all other nodes in the
//          cluster and contact Oracle Support Services.

1660,0,"The CSS daemon shutdown has completed"
// *Cause:  A command to shut down the CSS daemon was issued by a user
//          and the shutdown processing is completed.  The CSS daemon
//          is terminated.
// *Action: No action is required.

1661, 0, "The CSS daemon is not responding. Reboot will occur in %d milliseconds; Details at %s in %s"
// *Cause:  The CSS daemon is failing to respond.
// *Action: Collect the Clusterware alert log and the CSSD log of this
//          node as well as the CSS daemon logs of all other nodes in the
//          cluster and contact Oracle Support Services.

1662, 0, "Member kill requested by node %s for member number %d, group %s"
// *Cause:  A request to kill a member of the indicated group 
//          was issued by a process on the indicated node.
// *Action: No action is required.

1663, 0, "Member kill issued by PID %s for %d members, group %s. Details at %s in %s."
// *Cause: A member kill request was issued by the indicated process
//         for the members belonging to the indicated group.
// *Action: No action is required.

///////////////////////////////////////////////////////////////////////////
/   1701-1750 CSSD Initialization failures
///////////////////////////////////////////////////////////////////////////

1701, 0, "Initialization of the required component GIPC failed; details at %s in %s"
// *Cause:  The initialization of the communications component GIPC failed,
//          causing the CSSD startup to fail.
// *Action: Collect alert log and the CSSD log indicated in the message
//          and contact Oracle Support Services.

1702, 0, "Initialization of the required component OLR failed; details at %s in %s"
// *Cause:  The initialization of the local repository component OLR failed,
//          causing the CSSD startup to fail.
// *Action: Collect clusterware alert log and daemon logs and contact 
//          Oracle Support Services.

1703, 0, "Initialization of the required component GPNP failed because the GPNP server daemon is not up; details at %s in %s"
// *Cause:  The initialization of the configuration profile service failed
//          because the associated server is not up, causing the CSSD
//          startup to fail.
// *Action: Collect clusterware alert log and daemon logs and contact 
//          Oracle Support Services.

1704, 0, "Initialization of the required component %s failed; details at %s in %s"
// *Cause:  The initialization of a component required by the CSS daemon
//          failed, causing the CSSD startup to fail
// *Action: Collect clusterware alert log and daemon logs and contact 
//          Oracle Support Services.

1705, 0, "Found %d configured voting files but %d voting files are required, terminating to ensure data integrity; details at %s in %s"
// *Cause:  The voting file discovery was unable to locate a sufficient
//          number of valid voting files to guarantee data integrity and
//          is terminating to avoid potential data corruption.
// *Action: Delete the voting files that are no longer available, as 
//          indicated by message number 1637, using appropriate 'crsctl'
//          commands, run either on another node where the clusterware
//          stack is active, or by starting the clusterware stack in
//          exclusive mode.

1706, 0, "Found %d of %d voting files in a pending configuration change but %d voting files are required, terminating to ensure data integrity; details at %s in %s"
// *Cause:  The voting file discovery was unable to locate a sufficient
//          number of voting files from the new configuration when a
//          configuration change to add or delete voting files is in
//          progress.  The CSS daemon is terminating to avoid potential
//          data corruption.
// *Action: Delete the voting files that are no longer available, as 
//          indicated by message number 1638, using appropriate 'crsctl'
//          commands, run either on another node where the clusterware
//          stack is active, or by starting the clusterware stack in
//          exclusive mode.

1707,0,"Lease acquisition for node %s number %d completed"
// *Cause:  CSSD acquired a node number through a lease acquisition procedure.
// *Action: None

1708,0,"Lease acquisition failed for node %s because all lease slots are in use; Details at %s in %s"
// *Cause:  The node failed to acquire a lease because all the lease slots 
//          were found to be occupied by other nodes.
// *Action: Using olsnodes command get the list of leased nodes. 
//          Delete the unused nodes using appropriate crsctl command.

1709,0,"Lease acquisition failed for node %s because no voting file has been configured; Details at %s in %s"
// *Cause:  At least one voting file is required for CSSD to function properly.
//          No voting files have been configured.
// *Action: Add at lease one voting file using appropriate crsctl command.

1710,0,"Lease acquisition failed for node %s because CSSD failed to access majority of voting files; Details at %s in %s"
// *Cause:  A majority of the voting files are not accessible by a node.
// *Action: Delete the voting files that are no longer available, as 
//          indicated by message number 1637, using appropriate 'crsctl'
//          commands, run either on another node where the Clusterware
//          stack is active, or by starting the Clusterware stack in
//          exclusive mode.

1711,0,"Increasing the number of leases available for new nodes from %d to %d"
// *Cause:  All the currently available leases are being used.
//          Hence the number of leases available are increased.
// *Action: None

1712,0,"Failed to save the node number acquired for node %s; Details at %s in %s"
// *Cause:  CSSD failed to save the node number acquired during startup.
//          The node number is saved to speed up the subsequent startup.
//          Hence this is not a real problem but just a performance degradation
//          on the next startup.
// *Action: Collect Clusterware alert log, CSSD logs and OHASD logs indicated 
//          in the message and contact Oracle Support Services.

1713,0,"CSSD daemon is started in %s mode"
// *Cause:  CSSD has been started on the node.
// *Action: None

1714,0,"Unable to discover any voting files, retrying discovery in %d seconds; Details at %s in %s"
//  *Cause: No voting files were discovered.  Possible reasons include:
//          - The filesystems the voting files are on are not available
//          - The voting files have been deleted
//          - The voting files are corrupted
//  *Action: Verify that the filesystems that the voting files are on 
//           are active and that the voting files have not been damaged.
//           If necessary, start the clusterware stack in exclusive mode
//           using 'crsctl start crs -excl' and add voting files using
//           'crsctl add css votedisk'

  

1715,0,"A failure occurred in the CSS daemon during initialization; Details at %s in %s"
// *Cause:  A fatal error occurred during the initialization of the CSS daemon.
// *Action: Check for prior errors logged in the alert log. Correct any
//          errors that can be corrected.  If there are no errors shown,
//          or the errors cannot be resolved, contact Oracle Support
//          Services

1716,0,"The CSS daemon cannot join the cluster because the software version %s is lower than the active version %s; Details at %s in %s"
// *Cause:  The cluster has been upgraded to the active version indicated.
//          in the message, but this node is at a lower software version,
//          as indicated in the message.
// *Action: Upgrade this node to the active version indicated in the message

1717,0,"The CSS daemon has detected a voting file add during startup and is waiting for the add to complete; Details at %s in %s"
// *Cause:  A voting file add started on another node is in progress while
//          this CSS daemon is starting.  To avoid the potential for data
//          corruption, the CSS daemon on this node must wait for the add
//          to complete.
// *Action: This is normally a temporary condition that is automatically
//          resolved. If the clusterware stack cannot start on any node,
//          this condition may be corrected by starting the clusterware
//          stack in exclusive mode using 'crsctl start crs -excl' 
//          followed by 'crsctl stop crs' on one node.  This will
//          automatically correct the condition and the clusterware can
//          be started normally on all nodes.

1719,0,"Cluster Synchronization Service daemon (CSSD) %s not scheduled for %d msecs."
// *Cause: Excessive system load has prevented threads in the Cluster
// Synchronization Service daemon (CSSD) from being scheduled for
// execution for the time indicated in the message. This indicates
// the system is overloaded. 
// *Action: Take steps to reduce the system load or increase system 
// resources to handle the load.

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   1801-1900: CLSCFG specific messages. From clsdus.msg.
/
///////////////////////////////////////////////////////////////////////////

1801, 0, "Cluster %s configured with nodes %s."
// *Cause:  None.
// *Action: None.
1802, 0, "Node %s added to cluster."
// *Cause:  None.
// *Action: None.
1803, 0, "Node %s deleted from cluster."
// *Cause:  None.
// *Action: None.
1804, 0, "Node %s upgraded to version %s."
// *Cause:  None.
// *Action: None.
1805, 0, "Unable to connect to the CSS daemon, return code %d"
// *Cause: Could not initialize the CSS connection.
// *Action: Verify that the CSS daemon is running and restart it if it
//          is not up.  Retry the operation.
1806, 0, "An error occurred when obtaining the node number of this host, return code %d"
// *Cause: The request for node number of this node failed.
// *Action: Verify that the CSS daemon is running and restart it if not
//          Retry the operation that failed after restart.
//          Look for error messages from the CSS daemon in the alert log
//          indicating any problems.
1807, 0, "An internal cluster configuration command failed in an OCR/OLR operation. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
1808, 0, "Node-specific configuration for node %s in Oracle Local Registry was upgraded to version %s."
// *Cause:  None.
// *Action: None.
1809, 1, "The cluster configuration command failed to open OCR or OLR key %s. Details at %s in %s."
// *Cause: An expected or required piece of configuration is missing from the
//         cluster or local registry.
// *Action: Use the ocrcheck utility to detect errors, and the ocrdump utility
//          to review the registry contents. If problems exist, the registry may
//          need to be recovered or restored. If the problem persists, contact
//          Oracle Support Services.
/


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   1901-2000: CRSCTL specific messages. From clsdus.msg.
/
///////////////////////////////////////////////////////////////////////////

1901, 0, "CRS service setting (%s) is changed from [%s] to [%s]."
// *Cause:  None.
// *Action: None.
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   2001-2050: CLSDM specific messages. From clsdus.msg.
/
///////////////////////////////////////////////////////////////////////////

2001, 0, "memory allocation error when initiating the connection"
// *Cause: failed to allocate memory for the connection with the target process.
// *Action: None.
2002, 0, "connection by user %s to %s refused"
// *Cause: User command cannot connect to the target process.
// *Action: The user may not have sufficient privilege to connect.
2003, 0, "error %d encountered when connecting to %s"
// *Cause: Connection to the target process failed.
// *Action: Examine whether the connection is made properly.
//          Retry again at a later time if necessary.
2004, 0, "error %d encountered when sending messages to %s"
// *Cause: User command cannot communicate with the target process properly.
// *Action: Retry again at a later time.
2005, 0, "timed out when waiting for response from %s"
// *Cause: the target process does not return acknowledgment in time.
// *Action: Retry again at a later time.
2006, 0, "error %d encountered when receiving messages from %s"
// *Cause: no meta or response message was received from the target process.
// *Action: Retry again at a later time.
2007, 0, "invalid component key name <%s> used"
// *Cause: the given component key name could not be recognized.
// *Action: re-run the command with a valid component key name.
2008, 0, "invalid message type <%d> used"
// *Cause: an unrecognized message type was sent.
// *Action: Retry with a valid command again.
2009, 0, "unable to get authentication for user %s"
// *Cause: current user was not authenticated for connection.
// *Action: Log in as another user and try again.
2010, 0, "invalid response message from %s"
// *Cause: Response message has incorrect format.
// *Action: Retry again at a later time.
2011, 0, "no response at index %d in response message from %s"
// *Cause: Response message did not contain a response at the specified index.
// *Action: If this is an unexpected result, retry again at a later time.
2012, 0, "syntax error in command"
// *Cause: The command syntax is not valid.
// *Action: Issue 'crsctl debug -h' to see command syntax details.
//          Watch out for ',' vs. ';'.
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   2101-2300: OLR specific messages
/    NOTE TO DEVELOPER:
/              OLR message number = OCR message number + 1100
/              When an OLR message is added or deleted, a corresponding
/              OCR message must be added or deleted if applicable.
/              Please do not fill holes in the message numbers because
/              the unused message numbers might be used by OCR messages.
/    NOTE TO TRANSLATOR:
/              These OLR messages should be translated almost identical
/              to the corresponding OCR messages (1001 - 1200).
/
///////////////////////////////////////////////////////////////////////////
/
2101, 0, "The OLR was formatted using version %d."
// *Cause: Successfully formatted the OLR location(s). 
// *Action: None.
2102, 3, "The OLR was restored from file %s."
// *Cause: The OLR was successfully restored from a backup file as requested
//         by the user.
// *Action: None.
2103, 0, "The OLR format was downgraded to version %d."
// *Cause: The OLR was successfully downgraded to an earlier block format
//         as requested by the user.
// *Action: None.
2104, 0, "The OLR was imported from %s."
// *Cause: Successfully imported the OLR contents from a file as requested
//         by the user.
// *Action: None.
2105, 0, "The OLR upgrade was completed. Version has changed from %d to %d. Details in %s."
// *Cause: The OLR was successfully upgraded to a newer block format.
// *Action: None.
2106, 0, "The OLR location %s is inaccessible. Details in %s."
// *Cause: An error occurred while accessing the OLR.
// *Action: Use the "ocrcheck -local" command to validate the accessibility of
//          the device and its block integrity. Check that the OLR location in
//          question has the correct permissions.
/
/2107 is not applicable to OLR
/
/
/2108 is not applicable to OLR
/
/
/2108 is not applicable to OLR
/
/
/2110 is not applicable to OLR
/
/
/2111 is not applicable to OLR
/
2112, 0, "The OLR service started on node %s."
// *Cause: The OLR was successfully started.
// *Action: None
/
/2113 is not applicable to OLR
/
2114, 0, "Failed to import Oracle Local Registry from file %s"
// *Cause: Unable to read data from the import file and import to the 
//         local registry
// *Action: Check availability of the local registry and the details of the 
//          failure from the log file
/
/2115 is not applicable to OLR
/
/2116 is not applicable to OLR
/
/2117 is not applicable to OLR
/
/2118 is not applicable to OLR
/
/2119 is not applicable to OLR
/
2120, 1, "The Oracle Local Registry has invalid contents. Details at %s in %s."
// *Cause: Some of the Oracle Local Registry contents were invalid.
// *Action: Check the log file indicated in the message for more details. Use 
//          the 'ocrcheck -local' command to detect errors, and the 
//          'ocrdump -local' command to review the registry contents. If 
//          problems exist, the registry may need to be recovered or restored.
//          If the problem persists, contact Oracle Support Services.
/
/2122 is not applicable to OLR
/

//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
/
/   2301-2400: GPNP specific messages 
/   Added in Trail Blazer 
/  
/   PLEASE NOTE: If a message is added or removed , please update
/                the enum clsgpnpmsg in has/include/clsgpnp0.h
/
//////////////////////////////////////////////////////////////


2301, 3, "GPnP: %s "
// *Cause:  This conveys a message from the GPnP layer to the alert log.
// *Action: Look up the imbedded message and respond accordingly.
/
2302, 3, "Cannot get GPnP profile. Error %s (%s). "
// *Cause: Get GPnP profile operation failed.
// *Action:
/

2303, 1, "GPNPD is not running on local node. "
// *Cause: GPNPD is not running on local node. GPnP request cannot be completed.
// *Action: Make sure GPNPD is running and retry the operation.
/

2304, 1, "GPnP profile signature verification failed. %s request aborted. "
// *Cause: GPnP profile used in GPnP request or request result does not have a valid signature. 
// *Action: If error persists, please contact Oracle Support Services. 
/

2305, 1, "GPnP resource discovery (MDNSD) is not running on local node."
// *Cause: GPnP resource discovery failed. 
// *Action: Make sure resource discovery service (MDNSD) runs on local node.
/

2306, 1, "GPnP service on host \"%s\" not found."
// *Cause: Remote GPnP service on requested host were not found in resource discovery results.
// *Action: Make sure host is up, clusterware GPnP services (MDNSD and GPNPD) are up and running and network connection is operational.
/

2307, 1, "No GPnP services on requested remote hosts."
// *Cause: GPnP failed to find operational GPnP service on remote host(s).
// *Action: Make sure GPnP services (MDNSD and GPNPD) are up and running on remote hosts, and network connection is operational.
/

// 2308, UNUSED
// *Cause:
// *Action:
// This msg id is not used.
/

// 2309, UNUSED
// *Cause: 
// *Action:
// This msg id is not used.
/

2310, 1, "Fatal error: failed to initialize NZ security facility. "
// *Cause: Error occurred while initializing GPnP security component.
// *Action: If the problem persists, contact Oracle Support Services.
/

2311, 1, "Fatal error: failed to initialize Resource Discovery. RD error: %s (%u). Make sure RD providers installed properly. "
// *Cause: Error occurred while initializing GPnP Resource Discovery (RD).
// *Action: If the problem persists, contact Oracle Support Services.
/

2312, 1, "Fatal error: failed to initialize XDK. XDK error %s (%u). "
// *Cause: Error occurred while initializing Xml Development Kit component (XDK).
// *Action: If the problem persists, contact Oracle Support Services.
/

2313, 1, "Fatal error: failed to initialize GIPC communication layer. GIPC error: %s (%u). "
// *Cause: Error occurred while initializing GIPC communication layer.
// *Action: If the problem persists, contact Oracle Support Services.
/

2314, 1, "Fatal error: cannot initialize locking subsystem. "
// *Cause: Error occurred while initializing locking subsystem.
// *Action: If the problem persists, contact Oracle Support Services.
/

2315, 1, "Fatal error: failed to initialize GPnP certkey providers. "
// *Cause: GPnP certkey provider(s) data was not found or corrupt.
// *Action: If the problem persists, contact Oracle Support Services.
/

2316, 1, "Fatal error: cannot initialize GPnP, %s (%s). " 
// *Cause: General GPnP initialization failure.
// *Action: If the problem persists, contact Oracle Support Services.
/

2317, 1, "Fatal error: cannot get local GPnP security keys (wallet). "
// *Cause: GPnP wallet(s) directory or files were not found or corrupt.
// *Action: If the problem persists, contact Oracle Support Services.
/

2318, 1, "GPNPD is not found. "
// *Cause: Local GPnP service is not found.
// *Action: Make sure GPNPD is running.
/

2319, 1, "No cluster name found in GPnP profile. "
// *Cause: Profile is invalid - it must specify a mandatory clustername parameter.
// *Action: Please contact Oracle Support Services.
/

2320, 1, "No sequence number found in GPnP profile. "
// *Cause: Profile is invalid - it must specify a mandatory profile sequence parameter.
// *Action: Please contact Oracle Support Services.
/

// 2321, UNUSED
// *Cause:
// *Action:
// This msg id is not used.
/

2322, 1, "Fatal error: Cannot get local GPnP profile. Error initializing GPnP profile cache providers. "
// *Cause: Local GPnP setup is invalid. 
// *Action: Please contact Oracle Support Services.
/

2323, 1, "Error initializing one of the GPnP profile cache providers. "
// *Cause: Local GPnP setup is invalid. 
// *Action: Please contact Oracle Support Services.
/

2324, 1, "Errors occurred while trying to push GPnP profile. "
// *Cause: GPnP profile update partially failed.
// *Action: Try to repeat the update.  If the problem  persists, contact Oracle Support Services. 
/

2325, 1, "Unable to get GPnP profile from requested cluster nodes. "
// *Cause: Get GPnP profile from remote nodes failed.
// *Action: Try to repeat the update.  If the problem persists, contact Oracle Support Services. 
/

2326, 2, "GPnP profile is different across cluster nodes. %s. "
// *Cause: GPnP profile is different across cluster nodes.
// *Action: Try to repeat the update.  If the problem persists, contact Oracle Support Services. 
/

2327, 3, "GPNPD already running on node %s. Terminating. "
// *Cause: GPnP service instance is already running on node.
// *Action: Bring down existing GPNPD instance first.
/

2328, 3, "GPNPD started on node %s. "
// *Cause: GPnP service started on node.
// *Action: None.
/

2329, 3, "GPNPD on node %s shutdown. "
// *Cause: GPnP service was shutdown by request.
// *Action: None.
/

2330, 1, "GPNPD failed to start listening for GPnP peers. " 
// *Cause: GPnP service failed to open server endpoint.
// *Action: Please check GPNPD logs for the cause. If the problem persists, contact Oracle Support Services. 
/

2331, 1, "Error getting GPnP profile from \"%s\". "
// *Cause: Get remote GPnP profile from remote node operation failed.
// *Action: Retry request. If the problem persists, contact Oracle Support Services. 
/

2332, 1, "Error pushing GPnP profile to \"%s\". "
// *Cause: Push GPnP profile to remote node operation failed.
// *Action: Retry request. If the problem persists, contact Oracle Support Services. 
/

2333, 1, "Could not write GPnP profile to local cache. "
// *Cause: GPNPD service cannot save GPnP profile to local cache.
// *Action: Make sure there is at least 10MB of free disk space in Clusterware home. If the problem persists, contact Oracle Support Services. 
/

2334, 1, "Could not delete pending GPnP profile from local cache. "
// *Cause: GPNPD service cannot delete GPnP profile from local cache.
// *Action: If the problem persists, contact Oracle Support Services. 
/

2335, 1, "Could not write pending GPnP profile to local cache. "
// *Cause: GPNPD service cannot save GPnP profile to local cache.
// *Action: Make sure there is at least 10MB of free disk space in Clusterware home. If the problem persists, contact Oracle Support Services. 
/

2336, 1, "Fatal error: GPNPD failed get local GPnP profile and cannot continue. Please check gpnpd/gpnp client logs. "
// *Cause: GPnP service cannot find a profile in local cache, and cannot continue.
// *Action: Please contact Oracle Support Services.
/

// 2337, UNUSED
// *Cause:
// *Action:
// This msg id is not used.
/

2338, 1, "Clusterwide GPnP profile updates may be impaired. "
// *Cause: GPNPD failed to advertise itself with MDNSD. 
// *Action: Make sure MDNSD is up and running. 
/

// 2339, UNUSED
// *Cause:
// *Action:
// This msg id is not used.
/

2340, 1, "Errors occurred while processing received gpnp message. " 
// *Cause: Invalid GPnP message received.
// *Action: Please check gpnp client and GPNPD logs for details. If the problem persists, contact Oracle Support Services. 
/

2341, 3, "GPNPD on node %s shutting down on signal %d. "
// *Cause: GPnP service shutting down due to received signal.
// *Action: Please contact your cluster administrator.
/

2342, 1, "GPnP messaging received error : %s (%s). "
// *Cause: GPnP message error received.
// *Action: If the problem persists, contact Oracle Support Services. 
/

// 2400, End GPNP specific messages
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
/
/
/   2401-2499: Cluster Time Synchronization Service specific messages.
/              From clsdus.msg
/
//////////////////////////////////////////////////////////////

2401, 0, "The Cluster Time Synchronization Service started on host %s."
// *Cause: The Cluster Time Synchronization Service successfully started on the
//         listed node.
// *Action: None.
/
2402, 0, "The Cluster Time Synchronization Service aborted on host %s. Details at %s in %s."
// *Cause:  The Cluster Time Synchronization Service aborted due to an internal
//          error. Check the Cluster Time Synchronization Service log file to
//          determine the cause.
// *Action: Determine whether the Cluster Time Synchronization Service has
//          auto-started.
/
2403, 0, "The Cluster Time Synchronization Service on host %s is in observer mode."
// *Cause: The Cluster Time Synchronization Service detected an active vendor time
//         synchronization service on at least one node in the cluster.
// *Action: Oracle Clusterware requires a time synchronization service in active
//          mode. Oracle Clusterware will work with a vendor service or the Cluster
//          Time Synchronization Service. If you want to change the Cluster Time
//          Synchronization Service to active mode, stop and deconfigure the vendor
//          time synchronization service on all nodes.
/
2404, 0, "The Cluster Time Synchronization Service detects that the local time is significantly different from the mean cluster time. Details in %s."
// *Cause: The difference between the local time and the time on the reference
//         node was too much to be corrected.
// *Action: Shutdown the Oracle Clusterware on the local node. Adjust the
//          clock via native platform or OS methods. Restart the Oracle
//          Clusterware on the local node. 
/
2405, 0, "The Cluster Time Synchronization Service on host %s is shutdown by user"
// *Cause: The Cluster Time Synchronization Service on listed node was
//         terminated by a user.
// *Action: None.
/
2406, 0, "The Cluster Time Synchronization Service timed out on host %s. Details in %s."
// *Cause:  A Cluster Time Synchronization Service action failed. The
//          information from the reference node was discarded.
// *Action: Verify all network connections between cluster nodes and repair any
//          problematic connections. If no network problems are found,
//          1. Run diagcollection.pl.
//          2. Contact Oracle Support Services.
/
2407, 0, "The new Cluster Time Synchronization Service reference node is host %s."
// *Cause:  A new Cluster Time Synchronization Service reference node has been elected.
// *Action: None.
/
2408, 0, "The clock on host %s has been updated by the Cluster Time Synchronization Service to be synchronous with the mean cluster time."
// *Cause:  The clock was updated to be in sync with the mean cluster time.
// *Action: None.
/
2409, 0, "The clock on host %s is not synchronous with the mean cluster time. No action has been taken as the Cluster Time Synchronization Service is running in observer mode."
// *Cause: The clock was not in sync with the mean cluster time. No action has
//         been taken as Cluster Time Synchronization Service is running in
//         observer mode.
// *Action: Verify correct operation of the vendor time synchronization service
//          on the node.
/
2410, 0, "The Cluster Time Synchronization Service on host %s is in active mode."
// *Cause: The Cluster Time Synchronization Service did not detect an active
//         vendor time synchronization service on any node in the cluster.
// *Action: None. If a vendor time synchronization service is preferred to the
//          Cluster Time Synchronization Service, then configure and start the
//          vendor time synchronization service on all nodes to change the
//          Cluster Time Synchronization Service to observer mode.
/
2411, 0, "The Cluster Time Synchronization Service will take a long time to perform time synchronization as local time is significantly different from mean cluster time. Details in %s."
// *Cause: The difference between the local time and the time on the reference
//         node was too much to be synchronized in a short period.
// *Action: (Optional) Shutdown and restart the Oracle Clusterware on this node
//          to instantaneously synchronize the time with the reference node.
/
2412, 0, "The Cluster Time Synchronization Service detects that the local time is significantly different from the mean cluster time. Details in %s."
// *Cause: The difference between the local time and the time on the reference
//         node was too large. No action has been taken as the Cluster Time
//         Synchronization Service was running in observer mode.
// *Action: Verify correct operation of the vendor time synchronization service
//          on the node. Alternatively, if you want to change the Cluster
//          Time Synchronization Service to active mode, stop and
//          deconfigure the vendor time synchronization service on all nodes.
/
2413, 0, "The Cluster Time Synchronization Service is unable to perform step time synchronization due to high network latency with the reference node. The local time is not significantly different from the mean cluster time. The Cluster Time Synchronization Service is entering slew time synchronization mode."
// *Cause: The Cluster Time Synchronization Service experienced high network
//         latency. The local time was not significantly different from the
//         mean cluster time; therefore, the Cluster Time Synchronization
//         Service will maintain the system time with slew time synchronization.
// *Action: Determine the root cause of high network latency, and perform
//          appropriate repair if necessary.
/
2414, 0, "The Cluster Time Synchronization Service is unable to perform step time synchronization due to high network latency with the reference node. The local time is significantly different from the mean cluster time. The Cluster Time Synchronization Service is aborting."
// *Cause: The Cluster Time Synchronization Service experienced high network
//         latency. The local time was significantly different from the mean
//         cluster time; therefore, the Cluster Time Synchronization Service is
//         aborting.
// *Action: Shut down the Oracle Clusterware on the local node. Determine the
//          root cause of high network latency. Perform appropriate repair if
//          necessary, then restart the Oracle Clusterware on the local node.
/


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ CRS Policy Engine error messages, added in Trail Blazer 2500-2800
/
///////////////////////////////////////////////////////////////////////////

2500, 1, "Cannot stop resource '%s' as it is not running"
// *Cause:  A request to stop a resource that is not running was received.
// *Action: Check the current state of the resource, it should no
//          longer be running.
2501, 1, "Resource '%s' is disabled"
// *Cause:  The resource is currently disabled and so may not be operated on.
// *Action: Enable the resource and re-submit your request.
2502, 1, "Resource '%s' has dependency error because of resource '%s'"
// *Cause:  The attempted operation has failed because of a dependency on the  
//          specified resource.
// *Action: Ensure that the intended operation is still desired. If so, the 
//          specified resource and its state need to be evaluated to decide on
//          the corrective action.
2503, 1, "Resource '%s' is in UNKNOWN state and must be stopped first"
// *Cause:  The resource cannot be acted upon when it is in the UNKNOWN state.
// *Action: Stop the resource manually, make sure it is OFFLINE, and then
//          re-submit the request.
2504, 1, "Resource '%s' cannot be placed on any online servers that satisfy its placement policy"
// *Cause:  The resource cannot be placed because of the constrains imposed 
//          by its placement policy.
// *Action: Either change the placement policy of the resource or re-evaluate
//          the request.
2505, 1, "Another operation is being performed on '%s'. Please retry later"
// *Cause:  Another operation is being performed on the specified object.
// *Action: Typically, waiting and retrying or using a way to queue the
//          request are the two choices to proceed.
2506, 2, "Operation on '%s' has been cancelled"
// *Cause:  A scheduled or running operation has been cancelled.
// *Action: None.
2507, 1, "Unsupported modifier '%s' in dependency '%s'"
// *Cause:  The modifier is not a valid one.
// *Action: Check the specification of the dependency, fix the problem indicated,
//     and resubmit the request.
2508, 1, "Incomplete specification of dependency '%s'"
// *Cause:  The specification does not have the dependent object specified.
// *Action: Check the specification of the dependency, fix the problem indicated,
//     and resubmit the request.
2509, 1, "Resource type '%s' used in dependency '%s' does not exist or is not registered"
// *Cause:  The resource type referenced by the dependency specification is not
//          found.
// *Action: Check the specification of the dependency, fix the problem indicated,
//     and resubmit the request.
2510, 1, "Resource '%s' used in dependency '%s' does not exist or is not registered"
// *Cause:  The resource referenced by the dependency specification is not
//          found.
// *Action: Check the specification of the dependency, fix the problem indicated,
//     and resubmit the request.
2511, 0, "Attribute '%s' cannot be specified on per-X basis for resource '%s'"
// *Cause:  The specified attribute is specified on per-X basis, which is not
//          allowed for this attribute.
// *Action: Remove the specification.
2512, 1, "Attribute format for '%s' is invalid in resource '%s'"
// *Cause:  The specification does not follow valid format.
// *Action: Correct the specification and re-submit the request.
2513, 1, "Attribute format for '%s' is invalid"
// *Cause:  The specification does not follow valid format.
// *Action: Correct the specification and re-submit the request.
2514, 1, "Dependency attribute specification '%s' is invalid in resource '%s'"
// *Cause:  The specification of relations does not follow valid format.
// *Action: Correct the specification and re-submit the request.
2515, 1, "Circular dependency found for resource '%s'"
// *Cause:  The resource dependency specification has a circular dependency.
// *Action: Circular dependencies are disallowed. Please change the profile
//          and re-submit.
2516, 1, "Server pool is not specified for resource '%s'"
// *Cause:  The resource profile does not have server pool specified.
// *Action: Please either specify a an existing server pool or
//          HOSTING_MEMBERS in the profile and re-submit the request.
2517, 1, "Required attribute '%s' is not specified for resource '%s'"
// *Cause:  A required attribute is missing from the resource profile.
// *Action: Please add the attribute to the profile and re-submit the request.
2519, 1, "Either '%s' or '%s' must be specified when '%s' is '%s'"
// *Cause:  Neither or both of the parameters was specified.
// *Action: Please specify exactly one of the two and re-submit.
2520, 1, "Invalid value '%s' for attribute '%s'"
// *Cause:  The value specified for the attribute is inappropriate or invalid.
// *Action: Review the value, correct the problem and re-submit the request.
2521, 1, "Read-only attribute '%s' cannot be modified"
// *Cause:  An attempt was made to modify a read-only attribute.
// *Action: None.
2522, 1, "No value is specified"
// *Cause:  There is nothing specified for the value.
// *Action: Provide a valid value.
2523, 1, "Invalid characters are used when specifying the value"
// *Cause:  1 or more characters used to specify a value are inappropriate.
// *Action: Provide a valid value.
2524, 1, "Value specification may only contain '%s'/'%s'/'%s'/'%s'/'%s'/'%s'"
// *Cause:  The value specified is not any of the allowed.
// *Action: The value must be one of the allowed ones, as specified. Provide a
//          valid one.
2525, 1, "All instances of the resource '%s' are already running; relocate is not allowed because the force option was not specified"
// *Cause:  All instances of the resource are running and the start request
//          does not have the force option specified.
// *Action: Either specify the force option or re-evaluate the need for the 
//          request.
2526, 1, "There are no available instances of resource '%s' to start on '%s'"
// *Cause:  All instances of the resource are already running or otherwise 
//          unavailable to be started on the specified server.
// *Action: Create more instances or re-evaluate the need for the request.
2527, 1, "Unable to start '%s' because it has a '%s' dependency on '%s'"
// *Cause:  Start/relocate of the resource is impossible because it has a dependency
//          on another entity which prevents it from being able to start.
// *Action: This message will usually be coupled with another one that details
//          the nature of the problem with the other resource. Please follow up
//          on the action recommended for that message.
2528, 1, "Unable to place an instance of '%s' as all possible servers are occupied by the resource"
// *Cause:  Out of possible servers to place the resource on, all already host an instance of the resource.
// *Action: You need to add more servers or change the resource placement parameters to allow 
//          placement on additional servers.
2529, 1, "Unable to act on '%s' because that would require stopping or relocating '%s', but the force option was not specified"
// *Cause:  Acting on the resource requires stopping or relocating other resources,
//          which requires that force option be specified, and it is not.
// *Action: Re-evaluate the request and if it makes sense, set the force option and
//          re-submit.
2530, 1, "Unable to stop '%s' because '%s' has a stop-time '%s' dependency on it"
// *Cause:  Stopping the resource is impossible because it has a dependency
//          on another resource and there is a problem with that other resource.
// *Action: This message will usually be coupled with another one that details
//          the nature of the problem with the other resource. Please follow up
//          on the action recommended for that message.
2531, 1, "Internal error while operating on '%s'"
// *Cause:  General-purpose message for highly unexpected internal errors.
// *Action: This message will usually be preceded by another one with a more
//          specific problem description. Contact Oracle Support Services.
2532, 1, "OCR write failed for '%s'"
// *Cause:  Unknown, but would usually imply corruption or unavailability of the OCR
//          or a lack of permissions to update keys or a software defect in the
//          OCR code.
// *Action: Validate that OCR is accessible, validate that key permissions match.
//          Contact Oracle Support Services.
2533, 1, "Server '%s' is down. Unable to perform the operation on '%s'"
// *Cause:  The server is down and therefore the operation cannot be performed.
// *Action: Try using a different server.
2534, 1, "Resource type '%s' is not registered"
// *Cause:  The specified resource type is not registered.
// *Action: Re-evaluate the request.
2535, 1, "Resource type '%s' does not have attribute '%s' and thus it cannot be updated"
// *Cause   An non-existing attribute cannot be modified.
// *Action: Re-evaluate the request.
2536, 1, "Required attribute '%s' is not specified for '%s'"
// *Cause:  A required attribute is missing from the entity's profile.
// *Action: Add the attribute to the profile and re-submit the request.
2537, 1, "Resource type '%s' cannot be extended directly; use its extensions instead"
// *Cause:  The type cannot be extended.
// *Action: Use a type that extends this one.
2538, 1, "Value for attribute '%s' is of incorrect type (string is expected)"
// *Cause:  The type of the value is not correct.
// *Action: Re-submit the request with the value specified in proper type.
2539, 1, "A resource with the name '%s' is already registered"
// *Cause:  A resource with specified name is already registered.
// *Action: Use a unique name for the new resource.
2540, 1, "Value for attribute '%s' is of incorrect type (integer is expected)"
// *Cause:  The type of the value is not correct.
// *Action: Re-submit the request with the value specified in proper type.
2541, 1, "Server pool '%s' is not registered"
// *Cause:  The specified server pool is not registered.
// *Action: Re-evaluate the request.
2542, 1, "The tag '%s' is mentioned in both '%s' and '%s' attributes, which is conflicting"
// *Cause:  The same tag is used to specify exclusive as well as overlapping server pools.
//          These requirements cannot be satisfied simultaneously.
// *Action: Remove the tag from one of the attributes.
2543, 1, "The type is not specified for attribute '%s'"
// *Cause:  Value type specification is missing for the attribute.
// *Action: Specify a proper type and re-submit.
2544, 1, "The name '%s' is longer than the allowed maximum of '%d' characters"
// *Cause:  The name is too long.
// *Action: Use a shorter name.
2545, 1, "Cannot operate on '%s'. %s"
// *Cause:  The entity specified is currently locked as part of another operation.
// *Action: Re-submit the request later.
2546, 1, "Server '%s' is not online" 
// *Cause:  Operation is invalid because the specified server is not online.
// *Action: Provide an online server name.
2547, 1, "Update of an internal or read-only attribute '%s' for resource '%s' is not allowed"
// *Cause:  Internal and read-only attributes may not be updated.
// *Action: Exclude internal and read-only attributes from your request.
2548, 1, "A cyclical dependency on '%s' is detected from '%s'"
// *Cause:  There is a cycle in the dependency graph. Cycles are disallowed.
// *Action: Re-evaluate the dependency graph.
2549, 1, "Resource '%s' cannot be placed on '%s' as it is not a valid candidate as per the placement policy"
// *Cause:  The resource cannot be placed because of the constrains imposed 
//          by its placement policy.
// *Action: Either change the placement policy of the resource or re-evaluate
//          the request.
2550, 1, "Resource '%s' cannot be failed-over because it has other non-OFFLINE instances on the server '%s'"
// *Cause:  The resource cannot be failed-over from the specified server because has other 
//          non-OFFLINE instances still available on that server and fail-over can only be done
//          on all instances of the resource on the server as a whole.
// *Action: None.
2551, 2, "Resource '%s' cannot be failed-over because it is of type '%s', which cannot relocate"
// *Cause:  Local resources cannot be relocated from one server to another.
// *Action: None.
2552, 1, "There are no available instances of resource '%s' to start."
// *Cause:  All instances of the resource are in the ONLINE or UNKNOWN state.
// *Action: Re-evaluate the need for the request.
2553, 1, "Server pool '%s' cannot be unregistered as it does not exist"
// *Cause:  The server pool you are trying to remove does not exist.
// *Action: Make sure the server pool you are trying to remove exists.
2554, 1, "Server pool '%s' cannot be unregistered as it is referenced by resource '%s'"
// *Cause:  The server pool you are trying to remove has references to it.
// *Action: Make sure the server pool you are trying to remove is not referenced by other entities.
2555, 1, "Resource '%s' cannot be relocated as it is a local resource"
// *Cause:  The request is impossible to complete as local resources never relocate.
// *Action: Please re-evaluate the request.
2556, 1, "Resource '%s' cannot be restored to its original state after a failed relocate attempt"
// *Cause:  After an unsuccessful attempt to relocate a resource, crsd was unable to restore the resource.
// *Action: Manual intervention may be required. Re-try starting the resource.
2557, 1, "Server pool '%s' cannot be unregistered as it is referenced by server pool '%s'"
// *Cause:  The server pool you are trying to remove has references to it.
// *Action: Make sure the server pool you are trying to remove is not referenced by other entities.
2558, 1, "Resource type '%s' may not be unregistered as there are types that are based on it."
// *Cause:  Types may not be unregistered if they have derived types.
// *Action: Remove derived types first, then remove this one.
2559, 1, "Resource type '%s' may not be unregistered as it has the following resources:%s"
// *Cause:  Types may not be unregistered if they have resources registered.
// *Action: Remove the specified resources first, then remove the type.
2560, 1, "Resource type '%s' does not exist"
// *Cause:  The resource type referenced does not exist.
// *Action: Please specify a correct type.
2561, 1, "Resource type '%s' may not be unregistered as it is referenced by resource '%s'"
// *Cause:  Types may not be unregistered if they are referenced in resource dependencies.
// *Action: Make sure there are no existing resources that reference this type in their dependencies.
2562, 1, "Resource '%s' cannot be relocated as it is not running"
// *Cause:  Only currently running resources can be relocated.
// *Action: Make sure the resource is running before issuing the request.
2563, 2, "Attempt to start resource '%s' on '%s' has failed. Will re-retry on '%s' now."
// *Cause:  Undirected (no target member) start of a resource has failed for the server; a retry is in progress.
// *Action: None, this is an informational message.
2564, 2, "Failed to relocate resource '%s'. Will attempt to restore it on '%s' now."
// *Cause:  Resource relocate operation was unable to relocate the resource to any of the possible servers.
// *Action: None, this is an informational message.
2565, 2, "Attempt to relocate resource '%s' to '%s' has failed. Will re-retry on '%s' now."
// *Cause:  Undirected (no target member) relocate of a resource has failed for the server; a retry is in progress.
// *Action: None, this is an informational message.
2566, 1, "User '%s' does not have sufficient permissions to operate on resource '%s', which is part of the dependency specification."
// *Cause: User does not have permissions to operate on the resource as it will prevent the current resource from starting or staying online in future.
// *Action: The user performing the operation must have access
// privileges to operate on the entire resource dependency tree. The
// user must either be given those privileges by modifying the dependent
// resources' access rights or another user having permissions should
// perform this operation.
2567, 1, "Error while parsing the default value for attribute '%s'"
// *Cause:  The default value specified is not proper.
// *Action: Make sure the value is proper for its type.
2568, 1, "Base resource type name '%s' does not exist"
// *Cause:  The name of a base type used is not valid.
// *Action: Use an existing type as a base.
2569, 1, "Unsupported value type is used in attribute '%s'"
// *Cause:  An unsupported value type was specified in the attribute's definition.
// *Action: Use one of the supported types.
2570, 1, "Internal Error: Number of objects '%d' is different from number of lists '%d'"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
2571, 1, "Dependency kind '%s' is specified more than once for resource '%s'"
// *Cause:  A dependency kind is used more than once in the profile of the resource.
// *Action: Combine multiple specifications of the same dependency kind into a single clause.
2572, 1, "'%s' is not a supported Special Value"
// *Cause:  The specified identifier is not a valid Special Value.
// *Action: Check the value for correctness.
2573, 1, "ACL entry for owner field is missing."
// *Cause: The complete value for the ACL attribute has been provided but it is missing a mandatory entry specifying permissions for the owner.
// *Action: Include permissions for the owner in the value of ACL attribute.
2574, 1, "ACL entry for primary group field is missing."
// *Cause: The complete value for the ACL attribute has been provided but it is missing a mandatory entry specifying permissions for the primary group.
// *Action: Include permissions for the primary in the value of ACL attribute.
2575, 1, "ACL entry for users other than the owner and those belonging to primary group is missing."
// *Cause: The ACL attribute is missing a mandatory entry specifying permissions for users other than the owner and those belonging to the primary group.
// *Action: Include permissions for other users in the value of ACL attribute.
2576, 1, "User '%s' is not a member of group '%s'"
// *Cause: The group that the caller claims to be a member of has no such user by configuration.
// *Action: Make sure the group is configured to have the calling user as a member.
2577, 1, "Use of '%s' in attributes and values is not allowed"
// *Cause: A disallowed character was detected.
// *Action: Retry without the disallowed character.
2578, 1, "Value of '%s' (%d) may not be greater than that of '%s' (%d)"
// *Cause: The specified values do not make sense - one may not be less than the other.
// *Action: Use valid values.
2579, 1, "Value '%d' may not be less than '%d'"
// *Cause: The value is less than the allowed minimum.
// *Action: Use a proper value.
2580, 1, "Value '%d' is neither '%d' nor '%d'"
// *Cause: The value must be one of the two and it is neither.
// *Action: Use a proper value.
2581, 1, "Value '%s' is not any of the following '%s', '%s', '%s'"
// *Cause: The value must be one of the ones specified and it is not.
// *Action: Use a proper value.
2582, 1, "Value '%s' does not follow expected format: <n>[s|d|m|w|h]"
// *Cause: The value specification does not follow required format.
// *Action: Use a proper value.
2583, 1, "Value '%d' must be in the '%d' - '%d' range"
// *Cause: The value is not within the allowed range.
// *Action: Use a proper value.
2584, 1, "Value '%s' is not allowed here"
// *Cause: The value is not proper in this context.
// *Action: Use a proper value.
2585, 1, "Deletion of built-in resource types is not allowed"
// *Cause: An attempt was made to delete a built-in resource type.
// *Action: Removal of built-in types is not allowed.
2586, 1, "Deletion of a running resource '%s' requires the force option"
// *Cause: An attempt was made to delete a resource that is still running.
// *Action: Stop the resource first using the 'crsctl stop resource' command. 
//          If the resource cannot be stopped, specify the force option to the 'crsctl delete' command.
2587, 1, "Attribute '%s' is internal and thus may not be overridden in type '%s'"
// *Cause: Attributes defined in built-in resource types that are
// internal to the subsystem may never be overridden in user-defined
// resource types.
// *Action: Do not specify this attribute in the new user-defined type.
2588, 1, "A cyclical dependency on '%s' is detected from '%s' via type '%s'"
// *Cause:  There is a cycle in the dependency graph, via a resource type. Cycles are disallowed.
// *Action: Re-evaluate the dependency graph.
2589, 1, "Relation modifier '%s' is invalid for relation kind '%s'"
// *Cause: An unexpected relation modifier is specified.
// *Action: Use defined modifiers only.
2590, 1, "A resource name may not be empty or contain spaces"
// *Cause: A name must not be empty or contain space character(s).
// *Action: Specify a valid name.
2591, 1, "A server pool name may not be empty or contain spaces"
// *Cause: A name must not be empty or contain space character(s).
// *Action: Specify a valid name.
2592, 1, "A type name may not be empty or contain spaces"
// *Cause: A name must not be empty or contain space character(s).
// *Action: Specify a valid name.
2593, 1, "Comparator value '%s' in the filter specification is not supported"
// *Cause: An unsupported comparator was supplied.
// *Action: Use a supported value.
2594, 1, "Filter specification '%s' is invalid"
// *Cause: The filter specification invalid or empty.
// *Action: Provide a valid filter or do not specify you have one.
2595, 1, "Server pool '%s' has already been registered"
// *Cause: A server pool with this name has already been registered.
// *Action: Provide a name that is not currently in use.
2596, 1, "Modifications to the '%s' attribute of server pools are not supported"
// *Cause: Changes to the value of the attribute are not allowed.
// *Action: Create a different pool with the desired value and use it.
2597, 1, "Server '%s' may not be moved to pool '%s'"
// *Cause: Because of one or more of configuration-related constrains, the move of
// the server is not a valid operation at the time.
// *Action: Re-evaluate the request's validity in the context
// of the entire error stack.
2598, 1, "Server pool '%s' is already at its maximum size of '%d'"
// *Cause: The pool is already at the maximum.
// *Action: The request is impossible to execute.
2599, 1, "Server '%s' is not in a parent pool of '%s'"
// *Cause: The server is not in a parent pool of the pool in question.
// *Action: The request is impossible to execute.
2600, 1, "Server '%s' is already in another top-level server pool"
// *Cause: The server is already consumed by a different top-level
// pool and all such pools are exclusive as far as server ownership.
// *Action: The request is impossible to execute.
2601, 1, "Server '%s' is not explicitly mentioned as a candidate by server pool '%s'"
// *Cause: The server is not in the list of names the pool allows
// as candidates.
// *Action: Use a server that is in the specified group.
2602, 1, "Server '%s' is in server pool '%s' which is exclusive with server pool '%s'"
// *Cause: The server is already in a pool that's configured to be
// exclusive with the one at hand.
// *Action: The request is impossible to execute.
2603, 1, "Server '%s' cannot be assigned to server pool '%s' because it is not a top-level pool"
// *Cause: Server movement is only supported between top-level server pools.
// *Action: The request is impossible to execute as such an action is
// not supported.
2604, 1, "Server '%s' is already assigned to server pool '%s'"
// *Cause: Server movement makes no sense: the server is already in the target pool.
// *Action: Check the request validity.
2605, 4, "Server '%s' may not be relocated from server pool '%s' as the pool disallows transfers"
// *Cause: The server pool is configured not to allow server transfers.
// *Action: Check the request validity.
2606, 1, "Server '%s' may not be relocated from server pool '%s' because it is not above its minimum size"
// *Cause: Server pools of identical or higher importance may not be used 
// to steal servers from if they
// are not above their minimum size.
// *Action: Update the configuration of server pools by either
// changing the importance or the minimum size or both and then
// re-submit the request.
2607, 1, "Attribute '%s' has not been specified on per-X basis for resource '%s'"
// *Cause:  The specified attribute has not been specified on per-X basis for 
//          this resource.
// *Action: Check the per-X attribute for the resource, fix and resubmit.
2608, 1, "Attribute '%s' is not a per-X value and cannot be removed"
// *Cause:  The specified attribute is not a per-X value.
// *Action: Check the per-X attribute for the resource, fix and resubmit.
2609, 1, "Server '%s' may not be relocated to server pool '%s' as the pool disallows transfers"
// *Cause: The server pool is configured not to allow server transfers.
// *Action: Check the request validity.
2610, 1, "Server '%s' is unavailable"
// *Cause: The server is not available at the moment.
// *Action: Check available servers and rerun the request with an active server.
2611, 1, "Server pool '%s' is built-in and may not be deleted"
// *Cause: Built-in server pools may never be deleted.
// *Action: None.
2612, 1, "Server pools do not have attribute named '%s'"
// *Cause: An unsupported attribute was provided as part of the
// register or update request.
// *Action: Please double check the attributes that are supplied.
2613, 1, "Could not find resource '%s'."
// *Cause:  An attempt was made to operate on a resource that is not 
//          registered.
// *Action: Check if the resource is registered.
2614, 1, "Could not find resource type '%s'."
// *Cause:  An attempt was made to operate on a resource type that is not 
//          registered.
// *Action: Check if the resource type is registered.
2615, 1, "Could not find server pool '%s'."
// *Cause:  An attempt was made to operate on a server pool that is not 
//          registered.
// *Action: Check if the server pool is registered.
2616, 1, "The owner of resource type '%s' does not have sufficient permissions to operate on resource type '%s', from which it is directly or indirectly derived."
// *Cause: Update of a resource type in the current manner is not
// allowed as it will severely limit operations on the current
// resource type and will potentially prevent resources of derived
// types from starting or staying online in future. 
// *Action: If access privileges must be changed, then they need to
// changed bottom-up in a dependency.
2617, 1, "Incorrect value of attribute flags has been specified for attribute %s. Only READONLY flag can be changed for a type attribute."
// *Cause: Attempt was made to update the flag on a resource type
// attribute. The only change allowed is to the readonly property of
// the attribute.
// *Action: Provide correct value of the attribute flag.
2618, 1, "Cannot change data type %s of existing attribute %s to type %s."
// *Cause: Attempt was made to update the data type of attribute value.
// *Action: Data type of the attribute cannot be changed.
2619, 1, "Server pool '%s' may not be edited"
// *Cause: The pool's attributes may not be edited.
// *Action: None.
2620, 1, "Attribute '%s' of server pool '%s' may not be edited"
// *Cause: Editing of the attribute of the server pool is not allowed.
// *Action: None.
2621, 1, "Server '%s' is assigned to '%s' to which you have no permission. The operation is not authorized."
// *Cause: The operation requires making the specified server a
// placement candidate for the resources owned by the requesting user.
// However, this is not allowed because the user is not authorized to
// utilize the server.
// *Action: Either specify another server that that's in the pool you
// are authorized to use or request that a cluster administrator gives you access to the
// pool to which the server is currently assigned.
2622, 1, "Server '%s' is not assigned to any server pool and thus may only be specified by a cluster administrator"
// *Cause: The operation makes use of the server that's not currently
// assigned to a server pool and the requesting user is not a cluster
// administrator. Because of that use of the server cannot be
// authorized at the moment.
// *Action: Either request a cluster administrator to perform the
// operation for you or wait until the server has joined the cluster
// and is assigned to a pool to which you have an x-permission.
2623, 1, "Server pool '%s' cannot accept server '%s' because its name is not specified in '%s'"
// *Cause: Only servers whose names are mentioned in the attribute may
// be assigned to the pool.
// *Action: None.
2624, 1, "One of '%s', '%s' must be specified when '%s' is '%s'"
// *Cause:  Neither of the parameters was specified.
// *Action: Please specify either of the two and re-submit.
2625, 1, "Owner of resource '%s' does not have execute permission to pool '%s' and may not use it"
// *Cause: Resource profile references a server pool to which the
// owner of the resource does not have the X-permission.
// *Action: Either have the pool's permission changed appropriately or
// use a different pool.
2626, 1, "Owner of server pool '%s' does not have execute permission to parent server pool '%s'"
// *Cause: Parent pool does not have the X-permission for the pool's parent.
// *Action: Either have the desired parent pool's permission changed
// appropriately or use a different pool.
2627, 1, "You must have execute permission on pool '%s' to relocate server '%s'"
// *Cause: The client requesting the operation does not have proper
// permissions to the specified pool.
// *Action: Acquire required permissions or use another server/pool.
// Permissions can be added by an authorized user using 'crsctl setperm'
// command.
2628, 1, "Server pool '%s' may not be a parent of itself"
// *Cause: An attempt was made to make a server pool a parent of itself.
// *Action: Re-evaluate the server pool dependencies.
2629, 1, "Only cluster administrators are allowed to create top-level server pools"
// *Cause: An attempt was made to create a server pool that has no parent pools. 
// Creation of such pools is only allowed for cluster administrators.
// *Action: Either acquire the role of cluster administrator or have one create
// the pool for you.
2630, 1, "Only cluster administrators are allowed to create local resources"
// *Cause: An attempt was made to create a local resource which is only 
// allowed for cluster administrators.
// *Action: Either acquire the role of cluster administrator or have
// one create the resource for you.
2631, 1, "Only cluster administrators are allowed to create cluster resources that may run anywhere in the cluster"
// *Cause: An attempt was made to create a cluster resource that may
// run anywhere in the cluster which is only for cluster administrators.
// *Action: Either acquire the role of cluster administrator or have
// one create the resource for you.
2632, 1, "There are no more servers to try to place resource '%s' on that would satisfy its placement policy"
// *Cause: After one or more attempts, the system ran out of servers
// that can be used to place the resource and satisfy its placement
// policy.
// *Action: None.
2640, 1, "Required resource '%s' is missing."
// *Cause: A resource that's configured as required is not registered.
// *Action: Register the missing resource or update the dependency
// specification so as to the missing resource is not required for
// start.
2641, 1, "The value of '%s' cannot override that defined in the resource's type: '%s'"
// *Cause: Agent filename cannot be overridden on per-resource basis.
// *Action: Define a sub-type that uses the agent. Then create a
// resource of this new type.
2642, 1, "Relocate resource is not a valid command for this configuration"
// *Cause: A relocate command was issued in the configuration where it is not possible in principle.
// *Action: None.
2643, 1, "The server pool(s) where resource '%s' could run have no servers"
// *Cause: All of the server pools the resource uses (and has permissions to use) have no servers assigned.
// *Action: Either make sure there are active servers in the pools or
// use different pools for the resource.
2644, 1, "No hosting members of '%s' are either online or are allowed to be used by the resource"
// *Cause: No server out of the enumerated as hosting members is
// online or, if it is, may be used by the resource.
// *Action: You need to either add more servers into the cluster or
// request permission to pools to which currently available servers
// are assigned.
2645, 1, "Cannot create resources of type '%s'"
// *Cause: The type is abstract.
// *Action: Only concrete extensions of the type can be created.
2646, 1, "'%s' must have a default value if specified"
// *Cause: This attribute must have a default value if specified.
// *Action: Modify the type definition so that the attribute is
// removed or has a valid default value.
2647, 1, "Attribute '%s' may not be a negative value"
// *Cause: A negative value was provided for an attribute which only
// accepts non-negative values.
// *Action: Specify a non-negative number.
2649, 1, "Attribute '%s' of '%s' is internally managed and may not be specified"
// *Cause: An internal attribute was specified as part of an add/modify request.
// *Action: Re-execute the request without any internal attribute.
2650, 1, "Resource '%s' is configured to run only on '%s' and cannot be started on '%s'"
// *Cause: An attempt was made to start a resource on a server where
// it cannot run given its placement configuration.
// *Action: Make sure you start resources where they are configured to run.
2651, 1, "Resource alias '%s' must use special values to be unique for each server"
// *Cause: Resource alias name must resolve to a unique identifier for
// every server in the cluster. To achieve that, special values that yield
// different values on for each server must be used.
// *Action: You need to special an alias with special variables that
// will make it unique for every server.
2652, 1, "%s is a resource and only resource instances can be relocated."
// *Cause: An attempt was made to relocate a resource.
// *Action: Make sure you supply a resource instance rather than a resource.
2653, 1, "Special value evaluation must be associated with a resource instance"
// *Cause: Because some special values are per-server, each special value
// evaluation request must be associated with a resource instance.
// *Action: Please specify a server for the resource using -k or -n.
2660, 1, "Resource '%s' or all of its instances are disabled"
// *Cause: This is an API return code for requests that cannot be
// performed because the resource is disabled.
// *Action: Look at the detailed error messages that should
// always accompany this error.
2661, 1, "All instances of resource '%s' are disabled"
// *Cause: All instances of the resource instances are disabled.
// *Action: In order to change a resource state through CRS, its
// instances need to be enabled.
2662, 1, "Resource '%s' is disabled on server '%s'"
// *Cause: The resource was disabled on the specified server.
// *Action: Either re-enable, or use a different server.
2663, 1, "Resource instance of '%s' with %s=%d, %s=%d is disabled"
// *Cause: The resource instance whose cardinality/degree is specified
// is disabled.
// *Action: Either re-enable or use a different resource instance.
2664, 1, "Resource '%s' is already running on '%s'"
// *Cause: The resource is already running everywhere it may run.
// *Action: None.
2665, 1, "Resource '%s' is disabled on '%s'"
// *Cause: The resource is disabled on every server it is configured
// to start on.
// *Action: None.
2666, 1, "Resource '%s' is disabled on '%s' and is already running on '%s'"
// *Cause: The resource is disabled on every server it is configured
// to start on.
// *Action: None.
2667, 1, "Resource '%s' with %s=%s may only run on servers assigned to %s and %s, both of which are empty"
// *Cause: The resource's placement policy only allows it to run on
// servers assigned to the specified pools, and they are all empty.
// *Action: Either change the placement policy of the resource, or
// change the cluster configuration so that there are servers in those
// pools.
2668, 1, "The value of attribute '%s' (%d) may not not be above '%d'"
// *Cause: Attribute value specified is above the allowed maximum.
// *Action: Use a value below the specified maximum.
2669, 1, "The value is out of range. Maximum allowed value is '%d'"
// *Cause: Attribute value is out of the valid range.
// *Action: The value needs to be in a valid range.
2670, 1, "Unable to start/relocate '%s' because '%s' has a stop-time '%s' dependency on it"
// *Cause:  Start/relocate of the resource is impossible because
// another resource has a stop-time dependency on it and the action
// requires stopping that resources.
// *Action: This message will usually be coupled with another one that details
// the nature of the problem with the other resource. Please follow up
// on the action recommended for that message.
2671, 1, "Error processing attribute '%s': %s"
// *Cause:  The value specified for the attribute is inappropriate or invalid.
// *Action: Review the value, correct the problem and re-submit the request.
2672, 3, "Attempting to start '%s' on '%s'"
// *Cause: This is a status message.
// *Action: None.
2673, 3, "Attempting to stop '%s' on '%s'"
// *Cause: This is a status message.
// *Action: None.
2674, 1, "Start of '%s' on '%s' failed"
// *Cause: This is a status message.
// *Action: None.
2675, 1, "Stop of '%s' on '%s' failed"
// *Cause: This is a status message.
// *Action: None.
2676, 3, "Start of '%s' on '%s' succeeded"
// *Cause: This is a status message.
// *Action: None.
2677, 3, "Stop of '%s' on '%s' succeeded"
// *Cause: This is a status message.
// *Action: None.
2678, 1, "'%s' on '%s' has experienced an unrecoverable failure"
// *Cause: This is a status message.
// *Action: Perform whatever steps necessary to reset the state.
2679, 3, "Attempting to clean '%s' on '%s'"
// *Cause: This is a status message.
// *Action: None.
2680, 1, "Clean of '%s' on '%s' failed"
// *Cause: This is a status message.
// *Action: None.
2681, 3, "Clean of '%s' on '%s' succeeded"
// *Cause: This is a status message.
// *Action: None.
2682, 1, "It is locked by '%s' for command '%s' issued from '%s'"
// *Cause: This message is generated for operations that have a locking conflict.
// *Action:None.
2683, 0, "It is locked by '%s' for command '%s'"
// *Cause: This message is generated for operations that have a locking conflict.
// *Action:None.
2684, 0, "Change Active Version"
// *Document: NO
2685, 0, "Check Resource State"
// *Document: NO
2686, 0, "Fail Resource"
// *Document: NO
2687, 0, "Get Permissions"
// *Document: NO
2688, 0, "Engine State Recovery"
// *Document: NO
2689, 0, "Register Resource Type"
// *Document: NO
2690, 0, "Register Server Pool"
// *Document: NO
2691, 0, "Relocate Resource"
// *Document: NO
2692, 0, "Relocate Server"
// *Document: NO
2693, 0, "Unplanned Resource State Change"
// *Document: NO
2694, 0, "Server Failure"
// *Document: NO
2695, 0, "Set Permissions"
// *Document: NO
2697, 0, "Stack Shutdown"
// *Document: NO
2698, 0, "Server Re-assignment"
// *Document: NO
2699, 0, "Start Resource"
// *Document: NO
2700, 0, "Resource Autostart"
// *Document: NO
2701, 0, "Get Status"
// *Document: NO
2702, 0, "Stop Resource"
// *Document: NO
2703, 0, "Register Resource"
// *Document: NO
2704, 0, "Unregister Resource"
// *Document: NO
2705, 0, "Unregister Server Pool"
// *Document: NO
2706, 0, "Unregister Resource Type"
// *Document: NO
2707, 0, "Upgrade Trigger"
// *Document: NO
2708, 0, "Modify Resource"
// *Document: NO
2709, 0, "Modify Resource Type"
// *Document: NO
2710, 0, "Modify Server Pool"
// *Document: NO
2711, 0, "%s : %s"
// *Document: NO
2712, 0, "%s with %s=%d"
// *Document: NO
2713, 0, "instance of %s assigned to %s"
// *Document: NO
2714, 1, "'%s' is specified multiple times in '%s' of '%s'"
// *Cause: The specified value is specified multiple times.
// *Action: Remove duplicates and retry.
2715, 1, "Update to attribute AGENT_FILENAME is not currently supported. Please recreate the resource type with new value."
// *Cause: Attempt was made to update AGENT_FILENAME attribute.
// *Action: Delete existing resource type and add it back with the new value.
2716, 1, "Failure threshold exhausted for resource '%s'"
// *Cause: The resource instance has failed more times than allowed in
// the specified time interval. It will not be restarted automatically.
// *Action: Please identify and fix the problem. Restart the resource
// manually thereafter.
2717, 1, "Server '%s' is not in any of the server pool(s) hosting resource '%s'"
// *Cause: An attempt was made to start a resource on a server that is
// not currently an active server in any of the resource's server pool(s).
// *Action: Use a server name that is currently an active server of the
// resource's server pools(s).
2718, 1, "Server '%s' is not a hosting member of resource '%s'"
// *Cause: An attempt was made to start the resource on a server not
// listed as a hosting member of the resource.
// *Action: Use a server name that is listed as a hosting member.
2719, 1, "Resource '%s' may not be started on server '%s' because the server is not in either '%s' or '%s' server pools"
// *Cause: The resource's placement policy only allows it to run in
// the specified server pools. An attempt was made to start it on a server
// assigned to a different pool.
// *Action: Either use a different server or set the value of
// SERVER_POOLS to *, which will allow the resource to run on any server.
2720, 1, "'%s' is a resource alias for '%s' and cannot be updated"
// *Cause: An attempt was made to update a resource as if it were
// a resource.
// *Action: Please update the resource which this alias refers to
// instead.
2721, 1, "'%s' is a resource alias for '%s' and cannot be unregistered"
// *Cause: An attempt was made to unregister a resource alias as if it
// were a resource.
// *Action: Either unregister the resource which this alias refers to
// or modify its ALIAS_NAME attribute to not have a resource alias.
2722, 1, "The instance of resource '%s' may only run on '%s'; check on '%s' is unnecessary"
// *Cause: A check was issued on a server for a resource instance that may only
// run on a particular server.
// *Action: Please issue a check on the server where the resource instance is
// supposed to be run.
2723, 1, "No instance of resource '%s' found on '%s'"
// *Cause: A check was issued on a server for a resource which does not have any
// offline instances and no running instances on that server.
// *Action: Please issue a check on a server where a resource instance 
// might be running.
2724, 1, "Modifications to the built-in resource type '%s' are not allowed"
// *Cause: An attempt was made to modify a built-in resource type.
// *Action: Modification of built-in resource types is not allowed.
2725, 1, "User %s does not have permission to operate on resource %s."
// *Cause: Access control list on the resource do not permit the user
// to operate on the resource.
// *Action: Access privileges on the resource must be honored or this
// user must be given appropriate permissions.
2726, 1, "Invalid permissions specified for access control."
// *Cause: Access permissions are specifies using 'r', 'w', 'x' and
// '-' characters to indicate read, write and execute permissions. '-'
// indicates no access of any kind.
// *Action: Check format for the permissions string and re-run the
// command with the correct string.
2727, 1, "Acl entry '%s' has been specified more than once."
// *Cause: Access permissions for the entry have been specified
// more than once.
// *Action: Specify permissions for each entry only once and rerun the
// command.
2728, 1, "A resource type with the name '%s' is already registered"
// *Cause:  A resource type with such name is already registered.
// *Action: Use a unique name for the new resource type.
2729, 1, "Attribute '%s' cannot be overridden for a resource type"
// *Cause: An attribute was specified that is not allowed in a resource type.
// *Action: Do not use the attribute specified in the error message for a 
// resource type.
2730, 1, "Resource '%s' depends on resource '%s'"
// *Cause: An attempt was made to unregister a resource that is
// referenced by another resource in the dependency specification(s).
// *Action: Either remove the reference to this resource or the other resource
// first. Alternatively, the operation can be retried with a force option.
2731, 1, "Resource '%s' is already running on server '%s'"
// *Cause: The resource is already running on the server; relocate is impossible.
// *Action: Select another server.
2732, 1, "Resource '%s' is already starting on server '%s'"
// *Cause: The resource is currently starting on the server.
// *Action: Wait for the request to complete.
2733, 1, "Failed to stop all required resources on '%s'; the server will be restored into the original server pool(s)"
// *Cause: In order to successfully relocate a server, all resources
// that cannot run in the new server pool(s) must be stopped. That did not happen and thus the server 
// was placed back into the its original server pool(s).
// *Action: Manual intervention in stopping resources is
// required. The operation can be retried thereafter. Alternatively,
// another server can be used.
2734, 1, "Failed to stop all required resources on '%s'; the server will stay in RECONFIGURING state"
// *Cause: In order to successfully relocate a server, all resources
// that cannot run in the new server pool(s) must be stopped. Since that did
// not happen, the server will be kept in the RECONFIGURING state
// until the resources that did not stop have been stopped or
// unregistered.
// *Action: Manually stop the resources that did not stop or
// unregister them. 
2735, 1, "The operation requires relocating resource '%s' from server '%s'"
// *Cause: The operation would end up relocating the resource and the
// force option is not specified.
// *Action: Add more servers to the cluster, stop or relocate the
// resource, or use the force option for the same command.
2736, 1, "The operation requires stopping resource '%s' on server '%s'"
// *Cause: The operation would end up stopping the resource and the
// force option is not specified.
// *Action: Add more servers to the cluster, stop or relocate the
// resource, or use the force option for the same command.
2737, 1, "Unable to register server pool '%s' as this will affect running resources, but the force option was not specified"
// *Cause: One or more running resources would be affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
// resources mentioned right before this error, or use the force option for the same command.
2738, 1, "Unable to modify server pool '%s' as this will affect running resources, but the force option was not specified"
// *Cause: One or more running resources would be affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
// resources mentioned right before this error, or use the force option for the same command.
2739, 1, "Unable to relocate server '%s' as this will affect running resources, but the force option was not specified"
// *Cause: One or more running resources would be affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
// resources mentioned right before this error, use a different server, or use the force option for the same command.
2740, 1, "Failed to relocate server '%s' to server pool '%s'. The server has been restored to original server pool(s)."
// *Cause: In order to successfully relocate a server, all resources
// that cannot run in the new server pool(s) must be stopped. That did not happen and thus the server 
// was placed back into the its original server pool(s).
// *Action: Manual intervention in stopping or unregistering resources is
// required. The operation can be retried thereafter. Alternatively,
// another server can be used.
2741, 1, "A value must be specified for attribute '%s'"
// *Cause:  The attribute was not given a value.
// *Action: Provide a value and retry.
2742, 1, "The update of resource '%s' would lose track of one or more running instances"
// *Cause: An attempt was made to modify the configuration of the
// resource such that one or more currently running instance will be
// lost track of (the new configuration would change the resource to
// have fewer instances). 
// *Action: Stop the resource and resubmit.
2743, 1, "Unable to register resource '%s' as this will affect running resources, but the force option was not specified"
// *Cause: One or more running resources would be affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
// resources mentioned right before this error, or use the force option for the same command.
2744, 1, "Unable to modify resource '%s' as this will affect running resources, but the force option was not specified"
// *Cause: One or more running resources would be affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
// resources mentioned right before this error, or use the force option for the same command.
2745, 1, "Unable to relocate server %s because it results in violation of a pool %s constraint"
// *Cause: The requested move was rejected because it would cause either the source or target pool (or both) 
// to violate a pool size constraint, as indicated.
// *Action: Either change the pool size constraint(s) to accommodate your intent with this move, or 
// choose a different server to move.
2746, 1, "Cannot act on the instance of resource '%s' which is last known to have run on '%s' where Cluster Ready Services are not properly functioning"
// *Cause: The resource had been running on the server in the past but currently there's no way to know 
// if it's still running there because the Cluster Ready Services daemon does not appear to be
// running on the server. To prevent possible configuration violation,
// any attempt to start the resource instance on another server is rejected.
// *Action: The underlying problem preventing Cluster Resource Services on the server from 
// functioning properly must be addressed. Only then the resources that used to run there 
// can be operated on again. Alternatively, the server may be shut down or the clusterware stack 
// on it stopped completely.
2747, 1, "Server reconfiguration has failed to stop resources '%s' on server '%s'. Resources that did not stop must be stopped or unregistered manually. Details at %s in %s."
// *Cause: The specified resources could not be stopped.
// *Action: Stop the specified resources manually using and retry the last action.
2748, 1, "Failed to stop resource '%s' during server reconfiguration on server '%s'."
// *Cause: The specified resources could not be stopped.
// *Action: Stop the specified resources manually and retry the last action.
2749, 1, "A write of OCR server data '%s' failed. Details at %s in %s."
// *Cause: Could not persist data to OCR.
// *Action: Use the ocrconfig and ocrcheck utilities to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2750, 1, "Cardinality violation detected on server '%s', resource '%s' is in unexpected state. Details at %s in %s."
// *Cause: The specified resource was in an unexpected state.
// *Action: Manually restart the resource.
2751, 1, "Cannot create new resource, the resource type '%s' is not supported. Details at %s in %s."
// *Cause: The specified resource had an incorrect base type.
// *Action: Check the attributes for the resource and add it using crsctl again.
2752, 1, "Unable to write event sequence number to OCR. Details at %s in %s."
// *Cause: Could not update OCR with event sequence number.
// *Action: Use the ocrconfig and ocrcheck utilities to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2753, 1, "Timed out waiting for the server pools to be unfrozen."
// *Cause: Timed out while waiting for a client to unfreeze the pools it froze.
// *Action: If the problem persists, contact Oracle Support Services.
2754, 1, "Unable to change locks for a running operation '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2755, 1, "Error reading type definition for type '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2756, 1, "Invalid tag for command '%s'. Details at %s in %s."
// *Cause: An invalid command was received by the CRS daemon.
// *Action: Contact Oracle Support Services.
2757, 1, "Command '%s' timed out waiting for response from the resource '%s'. Details at %s in %s."
// *Cause: Timeout occurred while waiting for response to specified command.
// *Action: Check that the server targeted by the command is online and responsive.
2758, 1, "Resource '%s' is in an unknown state."
// *Cause: Unable to determine the current state of specified resource.
// *Action: Manually restart the resource.
2759, 1, "Failed to read repository key for NLS language '%s'. Details at %s in %s."
// *Cause: The key for the specified language could not be read from OCR.
// *Action: Use the ocrconfig and ocrcheck utilities to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2760, 1, "Policy engine failed to initialize internal types. Details at %s in %s."
// *Cause: Error during initialization of internal data.
// *Action: If the problem persists, contact Oracle Support Services.
2761, 1, "Consistency problem in registry while processing resource '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2762, 1, "Unable to find type '%s' in registry while processing resource '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services
2763, 1, "Error while reading resources. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2764, 1, "CRSADMIN and CRSUSER keys are not in repository. Details at %s in %s."
// *Cause: Error with repository. Required keys are not present.
// *Action: Use the ocrconfig and ocrcheck utilities to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2765, 1, "Resource '%s' has failed on server '%s'."
// *Cause: The specified resource was no longer running.
// *Action: The resource will be automatically brought back online. Use crsctl to confirm that it is online.
2766, 1, "Received state change for disabled resource '%s' from server '%s'."
// *Cause: Received command to change state for a resource that was disabled.
// *Action: None.
2767, 1, "Resource state recovery not attempted for '%s' as its target state is OFFLINE"
// *Cause: Target state for resource was OFFLINE. Clusterware will not attempt to recover it.
// *Action: None.
2768, 1, "Failure threshold exhausted by resource '%s'."
// *Cause: The specified resource failed too many times. No further restart attempts will be made.
// *Action: Fix the underlying cause of resource failure and manually restart the resource.
2769, 1, "Unable to failover resource '%s'."
// *Cause: Could not failover the specified resource.
// *Action: Restart the resource manually.
2770, 1, "Resource target '%s' is offline; will not restart."
// *Cause: The target state of the specified resource was offline.
// *Action: None.
2771, 1, "Maximum restart attempts reached for resource '%s'; will not restart."
// *Cause: Specified resource had been restarted too many times.
// *Action: Change the maximum restart parameter of the resource, and restart it manually.
2772, 1, "Server '%s' has been assigned to pool '%s'."
// *Cause: The specified server had been assigned to a server pool.
// *Action: None.
2773, 1, "Server '%s' has been removed from pool '%s'."
// *Cause: The specified server had been removed from a server pool.
// *Action: None.
2774, 1, "Failed to save resource '%s' to the repository. Details at %s in %s."
// *Cause: Could not update repository with resource details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored. 
2775, 1, "Failed to update resource '%s'. Details at %s in %s."
// *Cause:  Could not update repository with resource details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2776, 1, "Failed to update server pool '%s'. Details at %s in %s."
// *Cause: Could not update repository with server pool details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2777, 1, "Failed to delete resource '%s' from repository. Details at %s in %s."
// *Cause: Unable to update resource details in repository.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2778, 1, "Failed to delete server pool '%s' from repository. Details at %s in %s."
// *Cause:  Could not update repository with server pool details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2779, 1, "Failed to delete type '%s' from repository. Details at %s in %s."
// *Cause: Failed to update repository.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2780, 1, "Could not find Access Control List for resource '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2781, 1, "Error during registration for resource '%s'. Details at %s in %s."
// *Cause: Error occurred during registration callback of new resource.
// *Action: Contact Oracle Support Services.
2782, 1, "Unable to find attributes for resource '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2783, 1, "Internal error in local placement policy for resource '%s'. Details at %s in %s."
// *Cause: Internal error in CRS Policy Engine.
// *Action: Contact Oracle Support Services.
2784, 1, "Internal error, invalid server '%s' in local placement policy. Details at %s in %s."
// *Cause:  Internal error in CRS Policy Engine.
// *Action: Contact Oracle Support Services.
2785, 1, "Failed to register resource '%s'. Details at %s in %s."
// *Cause:  Could not update repository with resource details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2786, 1, "Failed to register server pool '%s'. Details at %s in %s."
// *Cause: Could not update repository with server pool details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2787, 1, "Server pool '%s' has fallen below its minimum size. Details at %s in %s."
// *Cause: The specified server pool has fallen below its minimum size and will be reconfigured.
// *Action: None.
2788, 1, "Server reconfiguration failed to stop resources '%s'. The server '%s' has been restored into the original pool(s)."
// *Cause: The specified resources could not be stopped.
// *Action: Stop the specified resources manually and retry the last action.
2789, 1, "Cannot stop resource '%s' as it is not running on server '%s'"
// *Cause:  An request to stop a resource on a server where it is not
//          running was received
// *Action: Check the current state of the resource; it should no
//          longer be running on that server.
2790, 3, "Starting shutdown of Cluster Ready Services-managed resources on '%s'"
// *Cause: Shutdown of Cluster Ready Services and the resources it manages has started on 
// the specified server.
// *Action: None.
2791, 3, "Starting shutdown of Oracle High Availability Services-managed resources on '%s'"
// *Cause: Shutdown of Oracle High Availability Services and the resources it manages has started on the indicated server.
// *Action: None.
2792, 3, "Shutdown of Cluster Ready Services-managed resources on '%s' has completed"
// *Cause: Shutdown of Cluster Ready Services and the resources it manages on the indicated server has completed.
// *Action: None.
2793, 3, "Shutdown of Oracle High Availability Services-managed resources on '%s' has completed"
// *Cause: Shutdown of Oracle High Availability Services and the resources it manages has completed on the indicated server.
// *Action: None.
2794, 1, "Shutdown of Cluster Ready Services-managed resources on '%s' has failed"
// *Cause: The failure is associated with one or more of the resources affected by this command on the indicated server."
// *Action: Error message(s) preceding this one should have the details about the
// resources that refused to shut down. Either manually stop those
// resources or retry with the force option.
2795, 1, "Shutdown of Oracle High Availability Services-managed resources on '%s' has failed"
// *Cause: The failure is associated with one or more of the resources affected by this command on the indicated server."
// *Action: Error message(s) preceding this one should have the details about the
// resources that refused to shut down. Either manually stop those
// resources or retry with the force option.
2796, 1, "The command may not proceed when Cluster Ready Services is not running"
// *Cause: This command must stop Cluster Ready Services-managed
// resources. However, Cluster Ready Services is not running, which
// does not mean its resources are not running. 
// *Action: The underlying reason for Cluster Ready Services not
// running needs to be resolved and the command retried.
// Alternatively, the command can be retried with the force option.
2797, 3, "Shutdown is already in progress for '%s', waiting for it to complete"
// *Cause: Another shutdown command was issued for the indicated server in the
// past and it is currently in progress. This command will wait until
// the original command completes and then complete as well.
// *Action: None.
2798, 0, "State change received for resource '%s' from unexpected server '%s'. Details at '%s' in '%s'."
// *Cause: A state change was reported for an instance of the resource from a server where the resource was never started.
// *Action: Shutdown the resource on the unexpected server
2799, 3, "Failed to shut down resource '%s' on '%s'"
// *Cause: Shut down failed because the listed resource failed to stop.
// *Action: Error message(s) preceding this one should have the details about the
// resources that refused to shut down. Either manually stop those
// resources or retry with the force option.
2800, 1, "Cannot start resource '%s' as it is already in the INTERMEDIATE state on server '%s'"
// *Cause: An attempt was made to start a resource that is already in the INTERMEDIATE state.
// *Action: Determine why the resource is in the INTERMEDIATE state based on the value of the STATE_DETAILS
//  attribute. If it is due to a check timeout, no action is needed. Otherwise, manual intervention
//  is required to bring the resource out of the INTERMEDIATE state.
2801, 1, "No instance of the resource '%s' should be running"
// *Cause: An attempt was made to relocate resource and the resource's
// instances to be relocated have TARGET=OFFLINE. 
// *Action: Restart the resource to change the value of the TARGET attribute to ONLINE. 
// Examining the value of the INTERNAL_STATE attribute can be used to determine if the instances
// are being operated on currently.
2802, 1, "Purging events not published within 15 minutes"
// *Cause: The events could not be published to the Event Manager Daemon either because it is down or there are errors doing the publish.
// *Action: Check the status of the Event Manager Daemon.
2803, 1, "Attribute '%s' has already been declared in a derived type '%s'"
// *Cause: An attempt was made to add a new attribute definition to a
// resource type that has an identically named attribute already
// defined in one or more derived types. Attributes declared in base types can be overridden 
// in derived ones, but the opposite is not allowed.
// *Action: Pick a different attribute name or delete the derived
// type(s), resubmit, and then add derived types back.
2804, 0, "Internal: Server Fencing"
// *Document: NO
2805, 1, "Unable to start '%s' because it has a '%s' dependency on resource type '%s' and no resource of that type can satisfy the dependency"
// *Cause:  Start/relocate of the resource is impossible because it has a dependency
//          on a resource type no resource of which can currently be used to satisfy the dependency.
// *Action: This message will normally be coupled with one or more other messages that detail
//          the nature of the problem for each existing resource of the type. 
2806, 1, "Failed to create stop operation for resource '%s'"
// *Cause: Creating the stop operation did not complete successfully.
// *Action: Error message(s) preceding this one should have more details about the problem. 
//          Try shutting down the resource manually, or retrying with the force option.
2807, 1, "Resource '%s' failed to start automatically."
// *Cause: This message comes up when the automatic start for the resource has
//         failed during a reboot of the cluster node or restart of the clusterware stack.
//         See previous resource specific messages for more details.
// *Action: Use 'crsctl start resource' to start the resource manually.
2847, 3, "Authorization failure: operating system user '%s' does not exist on server '%s'"
// *Cause: The specified operating system user or group does not exist on the specified server. Cluster Ready Services requires that all users or groups used by the resource it manages exist on each server of the cluster.
// *Action: Add the specified operating system user or group on the specified server.
/Alert
2848, 1, "Error while reading resources: Resource: '%s' . Error: %s.  Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2849, 2, "Authorization failure:  Resource '%s'"
// *Cause: A resource operation could not be performed because authorization checking failed. This may be due to inconsistency of user or group IDs across cluster nodes. 
// *Action: Check the ownership, group, and permissions associated with the resource and ensure that the associated operating system user and group definitions are consistent on all cluster nodes.
2878, 1, "Failed to restart resource '%s'"
// *Cause: An attempt to start the resource has failed.
// *Action: If failover is not enabled, try manually starting the resource on a different server. If failover is enabled, the resource has been failed over, and any problems are reported in subsequent messages.
2879, 1, "Cannot update the ALERT_TEMPLATE attribute, because the input is not valid"
// *Cause: A resource update operation could not be performed, because the input value is not valid.
// *Action: Ensure that valid attributes are specified in a space separated list.
2907, 1, "Resource '%s' is not completely configured and cannot be operated upon."
// *Cause:  A request was made without specifying the PID_FILES or EXECUTABLE_NAMES attribute.
// *Action: Specify a value for the PID_FILES or EXECUTABLE_NAMES attribute, or specify
//          values for STOP_PROGRAM, CHECK_PROGRAM and CLEAN_PROGRAMS attributes.

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ 4000 - 4999 Reserved for CRSCTL.
/
///////////////////////////////////////////////////////////////////////////

4000, 0, "Command %s failed, or completed with errors."
// *Cause: The specified command did not complete successfully.  If the command
//   performs multiple operations internally, one or more of those operations experienced
//   an error that is reported in a previous message.
// *Action: Examine the error message(s) preceding this message and correct
//   the problem(s) they describe.
4001, 0, "Command %s partially succeeded."
4002, 0, "Initialize operation failed."
4003, 3, "Resource '%s' is registered."
4004, 3, "Resource type '%s' is registered."
4005, 3, "This command has not been implemented yet."
4006, 3, "Server pool '%s' is registered."
4007, 0, "Server pool '%s' is not registered."
4008, 0, "Error retrieving status for entity '%s'. Details can be found in CRS-%d."
4009, 3, "Server '%s' is registered."
4010, 0, "Server '%s' is not registered."
4011, 0, "Data type is missing or invalid for attribute: '%s'."
4013, 0, "This command is not supported in a single-node configuration."
4014, 0, "Oracle High Availability Services autostart was not defined."
4015, 0, "Default value must be specified for attributes added to a type."
4016, 0, "Key '%s' is missing in the OCR."
// *Cause: Internal error.
// *Action: Contact Oracle Support Services.
4017, 0, "Failed to get the value for key '%s' from OCR."
// *Cause: Internal error.
// *Action: Contact Oracle Support Services.
4018, 0, "Failed to set the value for key '%s' in OCR."
4019, 0, "User '%s' is already a CRS Admin"
4020, 0, "User '%s' is not a CRS Admin"
4021, 0, "Could not establish communications with %s."
4022, 0, "Too many parameters\n"
4023, 0, "Error while initializing APPQOS wallets.\n%s"
4024, 0, "Database name is required to create database wallets. Use -name option to supply a database name."
4025, 0, "Wallet creation failed.\n%s"
4026, 0, "Wallet deletion failed.\n%s"
4027, 0, "User name '%s' is not in wallet of type '%s'."
4028, 0, "User name '%s' is present in wallet of type '%s'." 
4029, 0, "Wallet query failed.\n%s"  
4030, 0, "Wallet of type '%s' is found."
4031, 0, "Wallet of type '%s' is not found."
4032, 0, "User name '%s' is not deleted as it was not found in wallet.\n%s."
4033, 0, "User name addition to wallet type '%s' failed.\n%s"
4034, 0, "Password of user '%s' could not be modified.\n%s"
4035, 0, "This parameter is tuned automatically. \n"
4036, 0, "Found no resources to stop."
4037, 0, "The name '%s' contains the following invalid characters: '%s'"
4038, 0, "Cannot delete invalid user '%s' from CRS Admin list."
// *Cause: An attempt was made to delete an invalid username from the CRS Admin
// list. 
// *Action: Reissue the command with a valid username.
4039, 0, "'%s' cannot be specified as an attribute for a resource type"
4041, 1, "This command is no longer supported. Use 'crsctl start resource' instead"
4042, 1, "This command is no longer supported. Use 'crsctl stop resource' instead"
4043, 1, "This command is no longer supported. Use 'crsctl set log css' instead"
4044, 0, "CRS Administrator List: %s"
// *Cause: Output message, not an error.
// *Action: None.
4045, 1, "This command is no longer supported."
4046, 1, "Invalid Oracle Clusterware configuration."
// *Cause:  The Oracle Clusterware configuration is invalid.
// *Action: Configure Oracle Clusterware or Oracle Restart.
4047, 1, "No Oracle Clusterware components configured."
// *Cause:  No Oracle Clusterware components have been configured.
// *Action: Configure Oracle Clusterware or Oracle Restart.

/////////////////////////////////////////////////
/ Usage and message for individual crsctl commands
/////////////////////////////////////////////////
/
/ Status or Stat Usage - 4048 - 4050, 4061 - 4069, 4819 - 4821
/
4048, 3, "  crsctl status serverpool [<spName>[...]|-w <filter>] [-p|-v|-f]\n     Check status of designated server pools\n\n  crsctl status serverpool {<spName>[...]} -g\n     Check status of designated server pools"
4049, 3, "\nwhere \n     spName [...]      One or more blank-separated server pool names\n     -w                Server pool filter (e.g., \"MIN_SIZE > 3\")\n     -g                Check if server pools are registered\n     -p                Print static configuration\n     -v                Print runtime configuration\n     -f                Print full configuration"

/
/ Modify 4051 - 4056, 4070, 4818
/
// Msg 4051 consists of msg 4051 and msg 4818.
4051, 3, "  crsctl modify {resource|type|serverpool} <name> <options> \nwhere \n    name         Name of the CRS entity \n    options      Options to be passed to the modify command\n\n    See individual CRS entity help for more details"
4052, 3, "  crsctl modify {resource|type|serverpool} <name> <options>\n  crsctl modify wallet <options>"
4053, 3, "  crsctl modify resource <resName> -attr \"<specification>[,...]\" [-f] [-delete] [-i]\n     <specification>:   {<attrName>=<value> | <attrName>@<scope>=<value>}\n        <scope>:   {@SERVERNAME(<server>)[@DEGREEID(<did>)] |\n                       @CARDINALITYID(<cid>)[@DEGREEID(<did>)] }\nwhere"
4054, 3, "     resName         Modify named resource\n     attrName        Attribute name\n     value           Attribute value\n     server          Server name\n     cid             Resource cardinality ID\n     did             Resource degree ID\n     -f              Force option\n     -delete         Delete named attribute\n     -i              Fail if request cannot be processed immediately"
// Msg 4055 consists of msgs 4055, 4835 and 4836
4055, 3, "  crsctl modify type <typeName> -attr \"ATTRIBUTE=<attrName>[,TYPE={string|int}][,DEFAULT_VALUE=<defaultValue>][,FLAGS=typeFlags][,...]\" [-f] [-i]\nwhere"
4056, 3, "  crsctl modify serverpool <spName> -attr \"<attrName>=<value>[,...]\" [-f] [-i]\nwhere \n     spName          Modify named server pool attributes\n     attrName        Attribute name\n     value           Attribute value\n     -f              Force option\n     -i              Fail if request cannot be processed immediately"

/
/ Relocate 4057 - 4060
/
4057, 3, "  crsctl relocate {resource|server} <name> <options>"
4058, 3, "  crsctl relocate resource {<resName> [-k <cid>]| {resName|-all} -s <server>|-w <filter>} [-n <server>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]\n     Relocate designated resources"
4059, 3, "\nwhere\n     resName        Resource named resource\n     -all           Relocate all resources\n     -s             Source server\n     -w             Resource filter\n     -n             Destination server\n     -k             Cardinality ID\n     -env           Attribute overrides for this command\n     -f             Force option\n     -i             Fail if request cannot be processed immediately"
4060, 3, "  crsctl relocate server <server> [...] -c <spName> [-f] [-i]\n     Relocate designated servers\nwhere \n     server [...]   One or more blank-separated server names\n     spName         Destination server pool name\n     -f             Force option\n     -i             Fail if request cannot be processed immediately"

/
/ Status or Stat Usage - 4048 - 4050, 4061 - 4069, 4819 - 4821
/
4061, 3, "  crsctl status {resource|type|serverpool|server} [<name>|-w <filter>] [-g] \nwhere \n    name   CRS entity name\n    -w     CRS entity filter\n    -g     Check if CRS entities are registered"
// Msg 4062 consists of msg 4062 and msg 4819.
4062, 3, "  crsctl status type [<typeName>[...]]|-w <filter>] [-p] [-f] [-g]\n     Check status of designated resource types\nwhere \n     typeName [...]    One or more blank-separated resource type names"

// Msg 4063 consists of msgs 4063, 4064, 4065 and 4820.
4063, 3, "  crsctl status resource [<resName>[...]|-w <filter>] [<-p|-v> [-e]] | [[-f|-l|-g]] | [[-k <cid>|-n <server>] [-d <did>]] | [-s -k <cid> [-d <did>]]\n     Check status of designated resources\n\n  crsctl status resource [<resName>[...]|-w <filter>] -t"

4064, 3, "     Print status of resources in tabular format\n\n  crsctl status resource [<resName>[...]] -dependency [-stop | -pullup]\n    Print resource dependencies\nwhere \n     resName [...]     One or more blank-separated resource names\n     -w                Resource filter (e.g., \"TYPE = ora.database.type\")\n     -p                Print static configuration"

4065, 3, "     -v                Print runtime configuration\n     -e                Evaluate a resource instance's special values\n     -f                Print full configuration\n     -l                Print all cardinal and degree members"

// Msg 4066 consists of msgs 4066 and 4821.
4066, 3, "  crsctl status server [<server>[...]|-w <filter>] [-g|-p|-v|-f]\n     Check status of designated servers\nwhere \n     server [...]      One or more blank-separated server names"

4067, 3, "  crsctl status <resource|type|serverpool|server> [<name>] [options]\n  crsctl status <ip|testdns> <options>"
4068, 3, "  crsctl status ip -A {<IP_name>|<IP_address>}\n     Check if the IP is alive\nWhere\n     IP_name        Name which resolves to an IP. If name is not fully qualified domain name then standard name search will be used.\n     IP_address     IP address\n" 
4069, 3, "  crsctl status testdns [-address <IP_address>] [-port <port>] [-v]\n     Check status of DNS server for specified domain\nWhere\n     IP_address          DNS server address (defaults to hostname)\n     port                The port on which the DNS server is listening. Default value for the port is 53.\n     -v                  Verbose output"

/
/ Modify 4051 - 4056, 4070, 4818
/
4070, 3, "  crsctl modify wallet -type <wallet_type> [-name <name>] -user <user_name> -passwd\n     Modify the password for the designated user\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER or APPQOSDB.\n     name            Name is required for APPQOSDB wallets.\n     user_name       User whose password is to be modified.\n     passwd          Password will be read from standard input."

/
/ Add 4071 - 4080, 4822 - 4826
/
4071, 3, "  crsctl add {resource|type|serverpool} <name> <options> \nwhere \n   name          Name of the CRS entity \n   options       Options to be passed to the add command\n\n   See individual CRS entity help for more details\n\n  crsctl add crs administrator -u <user_name> [-f] \nwhere  \n   user_name     User name to be added to the admin list or \"*\"\n   -f            Override user name validity check"
4072, 3, "  crsctl add css votedisk <vdisk>[...] <options>\nwhere \n   vdisk [...]   One or more blank-separated voting file paths\n   options       Options to be passed to the add command"
4073, 3, "  crsctl add {resource|type|serverpool} <name> <options> \n  crsctl add crs administrator -u <user_name> [-f]\n  crsctl add wallet -type <type_name> <options>\n  crsctl add css votedisk <options>"
// Msg 4074 consists of msgs 4074, 4075, 4822 and 4823
4074, 3, "  crsctl add resource <resName> -type <typeName> [[-file <filePath>] | [-attr \"<specification>[,...]\"]] [-f] [-i]\n     <specification>:   {<attrName>=<value> | <attrName>@<scope>=<value>}"
4075, 3, "        <scope>:   {@SERVERNAME(<server>)[@DEGREEID(<did>)] |\n                       @CARDINALITYID(<cid>)[@DEGREEID(<did>)] }\nwhere"
// Msg 4076 consists of msgs 4076, 4824 and 4834
4076, 3, "  crsctl add type <typeName> -basetype <baseTypeName> {-file <filePath> | -attr \"ATTRIBUTE=<attrName>,TYPE={string|int}[,DEFAULT_VALUE=<defaultValue>][,FLAGS=typeFlags][,...]\" } [-i]\nwhere"
// Msg 4077 consists of msgs 4077 and 4825
4077, 3, "  crsctl add serverpool <spName> [[-file <filePath>] | [-attr \"<attrName>=<value>[,...]\"]] [-i]\nwhere \n     spName          Add named server pool\n     filePath        Attribute file"
4078, 3, "  crsctl add crs administrator -u <user_name> [-f]\nwhere \n    user_name    User name to be added to the admin list or \"*\"\n    -f           Override user name validity check"
4079, 3, "  crsctl add css votedisk <vdisk>[...] [-purge]\nwhere\n    vdisk [...]     One or more blank-separated voting file paths\n   -purge           Purge option"
// Msg 4080 consists of msgs 4080 and 4826
4080, 3, "  crsctl add wallet -type <wallet_type> [-name <name>] [-user <user_name> -passwd]\n     Create the designated wallet and add user to it\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER or APPQOSDB."

/
/ Check 4081 - 4085, 4180 - 4184
/
4081, 3, "  crsctl check has\n     Check status of OHAS"
4082, 3, "  crsctl check crs\n     Check status of OHAS and CRS stack" 
4083, 3, "  crsctl check cluster [[-all]|[-n <server>[...]]]\n     Check status of CRS stack"
4084, 3, "  crsctl check cluster [[-all]|[-n <server>[...]]]\n    Check status of CRS stack\nwhere \n    Default          Check local server\n    -all             Check all servers\n    -n               Check named servers\n    server [. ..]    One or more blank-separated server names"
4085, 3, "  crsctl check resource {<resName> [...]|-w <filter>} [-n <server>] [-k <cid>] [-d <did>]\n     Check status of resources"

/
/ Delete 4086 - 4095
/
4086, 3, "  crsctl delete {resource|type|serverpool|node} <name> [...] [<options>] \n  crsctl delete crs administrator -u <user_name> [-f]\n  crsctl delete wallet -type <wallet_type> <options>\n  crsctl delete css votedisk <options>"
4087, 3, "  crsctl delete resource <resName> [...] [-f] [-i]\nwhere \n    resName [...]   One or more resource names to be deleted\n    -f               Force option\n    -i               Fail if request cannot be processed immediately"
4088, 3, "  crsctl delete type <typeName> [...] [-i]\nwhere \n    typeName [...]  One or more blank-separated resource type names\n    -i              Fail if request cannot be processed immediately"
4089, 3, "  crsctl delete serverpool <spName> [...] [-i]\nwhere \n    spName [...]    One or more server pool names to be deleted\n    -i              Fail if request cannot be processed immediately"
4090, 3, "  crsctl delete crs administrator -u <user_name> [-f]\nwhere \n    user_name       User name to be deleted from the admin list or \"*\"\n    -f              Override user name validity check"
4091, 3, "  crsctl delete wallet -type <wallet_type> [-name <name>] [-user <user_name>]\n     Delete the designated wallet or user from wallet\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER or APPQOSDB.\n     name            Name is required for APPQOSDB wallets.\n     user_name       User to be deleted from wallet."
4092, 3, "  crsctl delete css votedisk {<vdiskGUID>[...]|<vdisk>[...]|+<diskgroup>}\nwhere\n    vdiskGUID [...]     One or more blank-separated voting file GUIDs\n    vdisk [...]         One or more blank-separated voting file paths\n    diskgroup           The name of a diskgroup containing voting files;\n                        allowed only when clusterware is in exclusive mode"
4093, 3, "  crsctl delete node -n <nodename>\nwhere\n    nodename     Node to be deleted"
                
/
/ Getperm 4096 - 4105
/
4096, 3, "  crsctl getperm {resource|type|serverpool} <name> [[-u <user_name>]|[-g <group_name>]]"
4097, 3, "  crsctl getperm resource <resName> [[-u <user_name>]|[-g <group_name>]]\nwhere \n    resName    Get permissions for named resource\n    -u         Get permissions for user name\n    -g         Get permissions for group name"
4098, 3, "  crsctl getperm type <typeName> [[-u <user_name>]|[-g <group_name>]]\nwhere \n    typeName   Get permissions for named resource type\n    -u         Get permissions for user name\n    -g         Get permissions for group name"
4099, 3, "  crsctl getperm serverpool <spName> [[-u <user_name>]|[-g <group_name>]]\nwhere \n    spName     Get permissions for named server pool\n    -u         Get permissions for user name\n    -g         Get permissions for group name"
4100, 0, "No permission found for user '%s'"
4101, 0, "No permission found for group '%s'"

/
/ Setperm 4106 - 4115
/

4106, 3, "  crsctl setperm {resource|type|serverpool} <name> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere \n     -u           Update entity ACL\n     -x           Delete entity ACL\n     -o           Change entity owner\n     -g           Change entity primary group"
4107, 3, "  crsctl setperm {resource|type|serverpool} <name> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}"
4108, 3, "  crsctl setperm resource <resName> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update resource ACL\n     -x           Delete resource ACL\n     -o           Change resource owner\n     -g           Change resource primary group"
4109, 3, "  crsctl setperm type <typeName> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update resource type ACL\n     -x           Delete resource type ACL\n     -o           Change resource type owner\n     -g           Change resource type primary group"
4110, 3, "  crsctl setperm serverpool <spName> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update server pool ACL\n     -x           Delete server pool ACL\n     -o           Change server pool owner\n     -g           Change server pool primary pool"
// Msg 4111 consists of msgs 4111 and 4112
4111, 3, "\n\n   ACL (Access Control List) string:\n\n   { user:<user_name>[:<readPerm><writePerm><execPerm>]   |\n     group:<group_name>[:<readPerm><writePerm><execPerm>] |\n     other[::<readPerm><writePerm><execPerm>] }\nwhere\n   user         User ACL\n   group        Group ACL\n   other        Other ACL"
4112, 3, "   readPerm     Read permission (\"r\" grants, \"-\" forbids)\n   writePerm    Write permission (\"w\" grants, \"-\" forbids)\n   execPerm     Execute permission (\"x\" grants, \"-\" forbids)"

/
/ Start 4116 - 4125, 4827
/
// Msg 4116 consists of msgs 4116, 4117, 4827, 4120, 4125 and 4811 OR
//                      msgs 4116, 4117, 4827, 4119, 4122, 4125 and 4811
4116, 3, "  crsctl start resource {<resName> [...]|-w <filter>]|-all} [-n <server>] [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]\n     Start designated resources\nwhere"
4117, 3, "     resName [...]    One or more blank-separated resource names\n     -w               Resource filter\n     -all             All resources\n     -n               Server name\n     -k               Resource cardinality ID"
// Msg 4118 consists of msgs 4118, 4120, 4125 and 4811 OR
//                      msgs 4118, 4119, 4121, 4125 and 4811
4118, 3, "  crsctl start resource {<resName> [...]|-w <filter>]|-all} [-n <server>] [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]"
4119, 3, "  crsctl start crs [-excl [-nocrs]|-nowait]\n     Start OHAS on this server\nwhere\n     -excl        Start Oracle Clusterware in exclusive mode\n     -nocrs       Start Oracle Clusterware in exclusive mode without starting CRS\n     -nowait      Do not wait for OHAS to start"
4120, 3, "  crsctl start has [-nowait]\n     Start OHAS on this server\nwhere\n     -nowait      Do not wait for OHAS to start"
4121, 3, "  crsctl start cluster [[-all]|[-n <server>[...]]]"
4122, 3, "  crsctl start cluster [[-all]|[-n <server>[...]]]\n    Start CRS stack\nwhere\n    Default         Start local server\n    -all            Start all servers\n    -n              Start named servers\n    server [...]    One or more blank-separated server names"
4123, 0, "Oracle High Availability Services has been started."
4124, 0, "Oracle High Availability Services startup failed."
4125, 3, "  crsctl start ip -A {<IP_name>|<IP_address>}/<net_mask>/<interface_name>\n    Start an IP on the given interface with specified net mask\nWhere\n    IP_name              Name which resolves to an IP. If it is not a fully qualified domain name then standard name search will be used.\n    IP_address           IP address\n" 

/
/ Stop 4126 - 4135
/
4126, 3, "  crsctl stop resource {<resName>[...]|-w <filter>|-all} [-n <server>] [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]\n     Stop designated resources\nwhere"
4127, 3, "     resName [...]    One or more blank-separated resource names\n     -w               Resource filter\n     -all             All resources\n     -n               Server name\n     -k               Resource cardinality ID\n     -d               Resource degree ID\n     -env             Attribute overrides for this command\n     -f               Force option\n     -i               Fail if request cannot be processed immediately"
4128, 3, "  crsctl stop resource {<resName>[...]|-w <filter>|-all} [-k <cid>] [-d <did>] [-n <server>] [-env \"ENV1=val1,ENV2=val2,...\"] [-f] [-i]"
4129, 3, "  crsctl stop crs [-f]\n    Stop OHAS on this server\nwhere\n    -f              Force option"
4130, 3, "  crsctl stop has [-f]\n    Stop OHAS on this server\nwhere\n    -f              Force option"
4131, 3, "  crsctl stop cluster [[-all]|[-n <server>[...]]] [-f]"
4132, 3, "  crsctl stop cluster [[-all]|[-n <server>[...]]] [-f]\n    Stop CRS stack\nwhere\n    Default         Stop local server\n    -all            Stop all servers\n    -n              Stop named servers\n    server [...]    One or more blank-separated server names\n    -f              Force option"
4133, 0, "Oracle High Availability Services has been stopped."
4134, 0, "Oracle High Availability Services shutdown failed."
4135, 3, "  crsctl stop ip -A {<IP_name>|<IP_address>}/<interface_name>\n     Stop the designated IP address\nWhere\n     IP_name              Name which resolves to an IP. If it is not fully qualified domain name then standard name search will be performed\n     IP_address           IP address\n     interface_name       Interface on which IP was started"

/
/ Enable 4136 - 4140
/
4136, 3, "This message reserved for crsctl enable cluster online help"
4137, 3, "This message reserved for crsctl enable cluster online help"
4138, 3, "  crsctl enable has\n     Enable OHAS autostart on this server"
4139, 3, "  crsctl enable crs\n     Enable OHAS autostart on this server"

/
/ Disable 4141 - 4145
/
4141, 3, "This message reserved for crsctl disable cluster online help"
4142, 3, "This message reserved for crsctl disable cluster online help"
4143, 3, "  crsctl disable has\n     Disable OHAS autostart on this server"
4144, 3, "  crsctl disable crs\n     Disable OHAS autostart on this server"

/
/ LSModules 4146 - 4150
/
4146, 3, "  crsctl lsmodules {mdns|gpnp|css|crf|crs|ctss|evm|gipc}\n where\n   mdns  multicast Domain Name Server\n   gpnp  Grid Plug-n-Play Service\n   css   Cluster Synchronization Services\n   crf   Cluster Health Monitor\n   crs   Cluster Ready Services\n   ctss  Cluster Time Synchronization Service\n   evm   EventManager\n   gipc  Grid Interprocess Communications"
4147, 0, "List %s Debug Module: %s"

/
/ Debug 4151 - 4165
/
4151, 3, "DEPRECATED: use crsctl set log {css|crs|evm}"
4152, 3, "DEPRECATED: use crsctl set trace {css|crs|evm}"
4153, 3, "DEPRECATED: use crsctl set log res"
4157, 3, "  crsctl debug statedump {crs|css|evm}\n where\n   crs           Cluster Ready Services\n   css           Cluster Synchronization Services\n   evm           Event Manager"
4165, 0, "%s Error: %s"
    

/
/ Config 4166 - 4169
/
4166, 3, "This message reserved for crsctl config cluster online help"
4167, 3, "This message reserved for crsctl config cluster online help"
4168, 3, "  crsctl config has\n     Display OHAS autostart config on this server"
4169, 3, "  crsctl config crs\n     Display OHAS autostart config on this server"

/
/ Query 4170 - 4175
4170, 3, "  crsctl query crs softwareversion [<nodename>| -all]\n     Lists the version of Oracle Clusterware software installed\nwhere\n     Default         List software version of the local node\n     nodename        List software version of named node\n     -all            List software version for all the nodes in the cluster"
4171, 3, "  crsctl query crs administrator\n     Display admin list"
4172, 3, "  crsctl query crs activeversion\n     Lists the Oracle Clusterware operating version"
4173, 3, "  crsctl query crs releaseversion\n     Lists the Oracle Clusterware release version"
4174, 3, "  crsctl query crs softwareversion [<nodename>]\n     Lists the version of Oracle Clusterware software installed\nwhere\n     Default         List software version of the local node\n     nodename        List software version of named node"
4175, 3, "  crsctl query css ipmidevice\n     Checks whether the IPMI device/driver is present"
4176, 3, "  crsctl query css votedisk\n     Lists the voting files used by Cluster Synchronization Services"
4177, 3, "  crsctl query wallet -type <wallet_type> [-name <name>] [-user <user_name>]\n     Check if the designated wallet or user exists\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER or APPQOSDB.\n     name            Name is required for APPQOSDB wallets.\n     user_name       User to be queried from wallet."
4178, 3, "  crsctl query css ipmiconfig\n     Checks whether Oracle Clusterware has been configured for IPMI"

/
/ Help message for filters
/
4179, 3, "Sample filters:\n1. TYPE = type1\n2. ((TYPE = type1) AND (CHECK_INTERVAL > 50))\n3. (TYPE = type1) AND ((CHECK_INTERVAL > 30) OR (AUTO_START co never))\n\nFilter Operators: =, >, <, !=, co, st, en\n\nSample command: crsctl status res -w \"TYPE = type1\"" 

/
/ Overflow help messages
/
4180, 3, "  crsctl check install"
4181, 3, "  crsctl check css\n     Check status of Cluster Synchronization Services"
4182, 3, "  crsctl check ctss\n    Check status of Cluster Time Synchronization Services"
4183, 3, "  crsctl check evm\n     Check status of Event Manager"
4184, 3, "  crsctl check resource {<resName> [...]|-w <filter>} [-n <server>] [-k <cid>] [-d <did>]\n     Check status of resources\nwhere \n     resName [...]    One or more blank-separated resource names\n     -w               Resource filter\n     -n               Server name\n     -k               Resource cardinality ID\n     -d               Resource degree ID"
4185, 3, "  crsctl get css <parameter>\n    Displays the value of a Cluster Synchronization Services parameter\n\n    clusterguid\n    diagwait\n    disktimeout\n    misscount\n    reboottime\n    priority\n    logfilesize"
4186, 3, "  crsctl get css ipmiaddr\n    Displays the IP address of the local IPMI device as set in the Oracle registry."
4187, 3, "  crsctl get hostname\n    Displays the host name"
4188, 3, "  crsctl get nodename\n    Displays the node name"
4189, 3, "  crsctl get {css <parameter>|hostname|nodename}"
4190, 3, "  crsctl set css <parameter> <value>\n    Sets the value of a Cluster Synchronization Services parameter\n\n    diagwait\n    disktimeout\n    misscount\n    reboottime\n    priority\n    logfilesize"
4191, 3, "  crsctl set css ipmiaddr <ipmi_ip_address>\n    Set the IP address of the local IPMI device in the Oracle registry."
4192, 3, "  crsctl set css ipmiadmin <ipmi_admin_name>\n    Set the administrative login for the local IPMI device in the Oracle registry."
4193, 3, "  crsctl set css votedisk {asm <diskgroup>|raw <vdisk>[...]}\nwhere\n    diskgroup       Voting disk diskgroup\n    vdisk [...]     One or more blank-separated voting file paths"
4194, 3, "  crsctl set css {<parameter> <value>|ipmiaddr <ipmi_ip_address>|ipmiadmin <ipmi_admin_name>}"
4195, 3, "  crsctl unset css <parameter>\n    Unsets the value of a Cluster Synchronization Services parameter, restoring its default value\n\n    diagwait\n    disktimeout\n    misscount\n    reboottime\n    priority\n    logfilesize"
4196, 3, "  crsctl pin css -n <node1>[...]\n Pin the nodes (make leases non-expiring)."
4197, 3, "  crsctl unpin css -n <node1>[...]\n Unpin the nodes (allow leases to expire)." 
4198, 3, "  crsctl replace {discoverystring <ds_string>| votedisk [<+diskgroup>|<vdisk> ... <vdisk>]}\nwhere\n    ds_string   comma-separated voting file paths without spaces and enclosed in quotes\n    diskgroup   diskgroup where the voting files will be located in ASM\n    vdisk       location of the voting files outside of ASM separated by space"
4199, 3, "  crsctl set crs activeversion [<version>] [-force]\n    Sets the Oracle Clusterware operating version."

/ 4200 - 4250: crsctl ipmi (node kill/fencing) 

4200, 0, "Failed to initialize a security context during wallet IPMI credentials creation.\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Customer Support.
4201, 0, "Hash context initialization failure during wallet IPMI credentials creation\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Customer Support.
4202, 0, "String hashing failed during wallet credentials creation\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Customer Support.
4203, 0, "Hashing creation error during wallet credentials creation\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Customer Support.
4204, 0, "Failed to initialize the IPMI credentials wallet: %s\n"
// *Cause:  While trying to initialize the IPMI credentials wallet, the cluster
//          wallet subsystem returned an unexpected error. The error is
//          included with this message.
// *Action: See the documentation and follow the directions for the displayed
//          error.
4205, 0, "Failed to open the IPMI credentials wallet. The wallet does not exist.\n"
// *Cause:  The wallet does not exist.
// *Action: Configure the wallet for the IPMI device using 'crsctl set'\n"
4206, 0, "Error reading IPMI credentials wallet: '%s'\n"
// *Cause:  While trying to read the IPMI credentials wallet, the cluster
//          wallet subsystem returned an unexpected error. The error is
//          included with this message.
// *Action: See the documentation and follow the directions for the displayed
//          error.
4207, 0, "Error writing IPMI credentials wallet: '%s'\n"
// *Cause:  While trying to write the IPMI credentials wallet, the cluster
//          wallet subsystem returned an unexpected error. The error is
//          included with this message.
// *Action: See the documentation and follow the directions for the displayed
//          error.
4208, 0, "Unexpected error encountered during lookup of IPMI credentials in the wallet\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using 'crsctl set' and then retry the
//          operation. If the retry fails call customer support.
4209, 0, "IPMI credentials not contained in the wallet\n"
// *Cause:  The wallet has not been configured.
// *Action: Configure the wallet for the IPMI device using 'crsctl set'\n
4210, 0, "Failed to obtain the length of IPMI credentials while accessing the wallet.\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call customer support.
4211, 0, "Failed to allocate memory\n"
// *Cause:  Insufficient system memory resources.
// *Action: Correct the system memory resources problem and retry.
4212, 0, "Failed to obtain the secret from the wallet.\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call customer support.
4213, 0, "Secret from wallet has incorrect size\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call customer support.
4214, 0, "crsctl %s and %s wallet versions of IPMI do not match.\n"
// *Cause:  A mismatch occurred between the IPMI versions of crsctl and the
//          Cluster Synchronization Services Daemon.
// *Action: Check proper installation and configuration of crsctl and the
//          Cluster Synchronization Services Daemon.
4215, 0, "Wallet secret encoding error\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Customer Support.
4216, 0, "Unexpected error configuring the wallet contents\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call customer support.
4217, 0, "Unexpected error saving IPMI credentials wallet: %s\n"
// *Cause:  While trying to save the IPMI credentials wallet, the cluster
//          wallet subsystem returned an unexpected error. The error is
//          included with this message.
// *Action: See the documentation and follow the directions for the displayed
//          error.
4218, 0, "Unable to access an IPMI device on this system\n"
// *Cause:  A test for the availability of an IPMI device failed.  This can
//          occur if:
//           - the IPMI device driver is not installed,
//           - the installed device driver is not supported by Oracle,
//           - IPMI is not supported on this platform or operating system,
//           - no IPMI device is present, or
//           - an IPMI device is present but not configured.
// *Action: Verify that IPMI hardware supporting IPMI version 1.5 or greater
//          is present and supported on this server, that the IPMI device is
//          configured and the device driver is properly installed.
4219, 0, "Failed to open the wallet. User must be the creator of the wallet: %s\n"
// *Cause:  Not the owner/creator of the wallet. The cluster wallet subsystem
//          returned an error included with this message.
// *Action: Retry as the owner/creator of the wallet. If necessary, also see
//          the documentation and follow the directions for the displayed
//          error.
4220, 0, "IPMI BMC password:"
4221, 0, "Must specify a password\n"
// *Cause:  No password entered in response to password prompt.
// *Action: Specify a password which matches the local servers IPMI BMC
//          password.
4222, 0, "Supplied password was greater than %d bytes\n"
// *Cause:  The password specified was too long for the IPMI device.
// *Action: Supply a password with a length no greater than the indicated size
//          while still matching the password used to configure the IPMI device.
//          Retry.
4223, 0, "Username is greater than %d bytes\n"
// *Cause:  The username specified was too long for the IPMI device.
// *Action: Supply a username with a length no greater than the indicated size
//          while still matching the username used to configure the IPMI
//          device. Retry.
4224, 0, "Unable to communicate with the Cluster Synchronization Services daemon to update IPMI values.\n"
// *Cause:  crsctl modified the IPMI credential wallet but could not notify
//          the Cluster Synchronization Services Daemon.
// *Action: Retry after assuring the Cluster Synchronization Services Daemon
//          is functioning by executing csscheck.
4225, 0, "Unexpected authorization error while creating the IPMI credentials wallet: %s\n"
// *Cause:  Error creating the IPMI credentials wallet.  The cluster wallet
//          subsystem returned an unexpected error. The error is included
//          with this message.
// *Action: See the documentation and follow the directions for the displayed
//          error and retry.
4226, 0, "Unexpected authorization error while saving the IPMI credentials wallet: %s\n"
//*Cause:  While attempting to save the IPMI credentials wallet, the cluster
//         wallet sub-system returned an authorization error.  The text of
//         the authorization error text is included with this message.
//         This error was unexpected, and might have been due to an internal
//         error, because wallet creation should be authorized for anyone,
//         and, if the wallet was pre-existing, it had already been read after
//         proper authorization checks.  
//*Action: Consult the documentation for the included message to investigate 
//         the root cause of the authorization error, and retry the "set" 
//         operation if indicated.  If this fails, contact Oracle Support.
4227, 0, "Configuration data stored but IPMI IP address is required to complete the change. The change cannot be validated until the information is complete.\n"
//*Cause:  Not proceeding with Client's IPMI login change request because
//         all information such as IPMI username, password and IP address
//         need to be present.
//*Action: Please execute 'crsctl set css ipmiaddr' from crsctl.
4228, 1, "Value of attribute '%s' is missing\n"
// *Cause:  The user did not provide a value for the attribute.
// *Action: Provide a value using the format <attrName>=<value>, 
// where <value> may be empty single quotes.
4229, 0, "The IPMI information change was successful\n"
//*Cause: The IPMI address and authorization information have been validated 
//        and the change completed.
//*Action: None required.
4230, 0, "A device was found where the IPMI device should be, but the device is not an IPMI device\n"
// *Cause:  The IPMI driver may not be configured or supported by this host.
// *Action: Check the configuration of the IPMI driver and verify the server's
//          support of an IPMI version 1.5 or greater device.
4231, 0, "IPMI device and/or driver found\n"
// *Cause:  An IPMI device and/or device driver was identified on the machine.
//          Detection mechanisms for IPMI hardware vary by platform.
// *Action: None required.
4232, 0, "Configuration data stored but IPMI authorization information is required to complete the change. The change cannot be validated until the information is complete.\n"
//*Cause:  Not proceeding with Client's IPMI login change request because
//         all information (IPMI username, password and IP address)
//         need to be present.
//*Action: Please execute 'crsctl set css ipmiadmin' from crsctl.
4233, 0, "New IPMI configuration data stored, but failed validation by remote node.\n" 
//*Cause:  The supplied configuration data was stored in the Oracle
//         registry, but the resulting configuration could not be used
//         for IPMI access by a remote node.  The stored IP address
//         and/or IPMI admin credentials is/are incorrect.
//*Action: The validating node is identified in the CRS alert log, and 
//         further details can be found in the alert log on that node. 
//         Verify the credentials for the local IPMI device and reset the
//         configuration using commands 'crsctl set css ipmiadmin' and 
//         'crsctl set css ipmiaddr'
4234, 0, "IPMI configuration unset and registry entries deleted.\n"
//*Cause:  Requested operation successful.  However, if the CRS stack was
//         able to access and use the deleted configuration data, it will
//         continue to do so until it is restarted.
//*Action: None required.  Enter new configuration data or restart the CRS
//         stack if desired.
4235, 0, "Failed to delete the IPMI configuration from the Oracle Registry: '%s'\n"
//*Cause:  An error was encountered in the Oracle registry sub-system
//         while trying to clear IPMI configuration and delete the IPMI
//         configuration entries.  The detailed error message is included with
//         this message.
//*Action: See the documentation and follow the directions for the displayed
//         error.
4236, 0, "Oracle Clusterware configured to use IPMI\n"
//*Cause:  The Oracle Registry contains complete configuration data for IPMI.
//*Action: None required.
4237, 0, "Oracle Clusterware is not fully configured to use IPMI\n"
//*Cause:  The Oracle Registry does not contain complete configuration
//         data for IPMI.
//*Action: None required.


// 4251 - 4300: crsctl replace 
4251, 0, "Failed to change the discovery string\n"
// *Cause: An internal error happened during this operation.
// *Action: Please contact Oracle Support Services. 
4252, 0, "Failed to update the profile with the new discovery string\n"
//*Cause:  An internal error happened when updating the discovery string in the profile.
//*Action: Please contact Oracle Support Services. 
4253, 0, "The discovery string can not be changed because the voting files are on ASM\n"
//*Cause:  Changing the discovery string is allowed only if the voting files are not on ASM.
//*Action: None.
4254, 0, "The discovery string has already been set to this value\n"
//*Cause: The value being passed is the same as the current discovery string.
//*Action: Pass a different discovery string if necessary.
4255, 0, "Not able to find the current configured voting files with the provided discovery string\n"
//*Cause: The supplied discovery string does not discover the voting files that are
//        currently configured.
//*Action: Pass a different discovery string that includes the location of the
//         current configured voting files.
4256, 0, "Updating the profile\n"
//  *Cause:  An update to the profile is being performed.
//  *Action: None.
4257, 0, "Voting file discovery string successfully replaced\n"
//  *Cause:  A request to replace a discovery string completed.
//  *Action: None.
4258, 0, "Addition and deletion of voting files are not allowed because the voting files are on ASM\n"
//*Cause:  A voting file add or delete request was issued, but voting files
//         have been configured on ASM storage. Once voting files are 
//         configured for ASM, changes in the configuration can be made only
//         with 'crsctl replace votedisk'.
//*Action:  Use 'crsctl replace votedisk' to modify the voting file 
//         configuration.
4259, 0, "Only one ASM diskgroup may be specified\n"
//*Cause:  If the voting files will be on ASM, no more than one diskgroup should
//         be specified.
//*Action: Specify the correct ASM diskgroup.
4260, 0, "Voting file %s is already configured\n"
//*Cause:  The location provided is already configured as a voting file.
//*Action: Specify another location that is not a current voting file.
4261, 0, "Diskgroup %s is already configured with voting files\n"
//*Cause:  The diskgroup name provided is already configured with voting files.
//*Action: Specify another location for the voting files.
4262, 0, "Failure when retrieving information from the GPnP profile\n"
//*Cause:  An internal error happened when accessing GPnP profile.
//*Action: Contact Oracle Support Services. 
4263, 0, "This operation is not allowed\n"
//*Cause: Replacing a list of non-ASM voting files with a different list of voting files is
//        not supported.
//*Action: To change the list of non-ASM voting files and add new voting files,
//         use 'crsctl add css votedisk <vfile> ... <vfile>'.
4264, 0, "The operation could not be validated\n"
// *Cause:  An internal error happened during the validation of the discovery
//          string.
// *Action: Contact Oracle Support Services. 
4265, 0, "The operation cannot be performed because the profile is busy with another operation\n"
// *Cause:  Another operation on the profile is taking place.
// *Action: Let the other operation finish and retry.
4266, 0, "Voting file(s) successfully replaced\n"
//  *Cause:  A request to replace a voting files(s) completed.
//  *Action: None.
4267, 0, "Error while updating the profile with ASM discovery string\n"
// *Cause:  An internal error happened while updating the ASM discovery
//          string.
// *Action: Contact Oracle Support Services. 
4268, 0, "'-name' option is supported only with APPQOSDB type wallets"
// *Cause: The '-name' option was specified in a wallet command for APPQOSDB type wallet.
// *Action: Use the '-name' option only for actions on APPQOSDB type wallets.
4269, 0, "Successful get priority %d %s for Cluster Synchronization Services.\n"
// *Cause: The 'get' operation was performed successfully.
// *Action: None.
/
/ CRSCTL messages
/
4301, 0, "Usage: crsctl add       - add a resource, type or other entity"
4302, 0, "       crsctl check     - check a service, resource or other entity"
4303, 0, "       crsctl config    - output autostart configuration"
4304, 0, "       crsctl debug     - obtain or modify debug state"
4305, 0, "       crsctl delete    - delete a resource, type or other entity"
4306, 0, "       crsctl disable   - disable autostart"
4307, 0, "       crsctl discover  - discover DHCP server"
4308, 0, "       crsctl enable    - enable autostart"
4309, 0, "       crsctl get       - get an entity value"
4310, 0, "       crsctl getperm   - get entity permissions"
4311, 0, "       crsctl lsmodules - list debug modules"
4312, 0, "       crsctl modify    - modify a resource, type or other entity"
4313, 0, "       crsctl query     - query service state"
4314, 0, "       crsctl pin       - pin the nodes in the node list"
4315, 0, "       crsctl relocate  - relocate a resource, server or other entity"
4316, 0, "       crsctl replace   - replaces the location of voting files"
4317, 0, "       crsctl release   - release a DHCP lease"
4318, 0, "       crsctl request   - request a DHCP lease"
4319, 0, "       crsctl setperm   - set entity permissions"
4320, 0, "       crsctl set       - set an entity value"
4321, 0, "       crsctl start     - start a resource, server or other entity"
4322, 0, "       crsctl status    - get status of a resource or other entity"
4323, 0, "       crsctl stop      - stop a resource, server or other entity"
4324, 0, "       crsctl unpin     - unpin the nodes in the node list"
4325, 0, "       crsctl unset     - unset an entity value, restoring its default"
/
/CRSCTL parse messages
/
4381, 3, "Missing additional arguments"
4382, 3, "Invalid combination of arguments:"
4383, 0, "For complete usage, use:\n    crsctl [-h | --help] \nFor detailed help on each command and object and its options use:\n    crsctl <command> <object> -h  For example, crsctl relocate resource -h"
4384, 0, "Brief usage:"
4385, 0, "Parse error:"
4386, 0, "Argument '%s' is already specified"
4387, 0, "Argument '%s' is missing a value"
4388, 0, "More than one value"
4389, 3, "Argument '%s' is a required argument"
4390, 3, "'%s' is an invalid argument"
4391, 0, "Version:"
4392, 0, "Usage: crsctl <command> <object> [<options>]\n    command: enable|disable|config|start|stop|relocate|replace|status|add|delete|modify|getperm|setperm|check|set|get|unset|debug|lsmodules|query|pin|unpin|discover|release|request\nFor complete usage, use:\n    crsctl [-h | --help]\nFor detailed help on each command and object and its options use:\n    crsctl <command> <object> -h  e.g. crsctl relocate resource -h"
4393, 0, "Usage:"

/
/ CRSCTL error and return messages
/
4400, 0, "Negative values are not allowed for parameter %s.\n"
4401, 0, "CRSCTL Internal Error: %s code=%d\n"
4402, 0, "The CSS daemon was started in exclusive mode but found an active CSS daemon on node %s, number %s, and is terminating"
// *Cause:  The CSS daemon was started in exclusive mode, which requires
//          that the clusterware stack is down on all other nodes to ensure
//          data integrity.  A CSS daemon was detected on another node,
//          so the CSS daemon on this node is terminating.
// *Action: If this message displays as part of the install process, no
//          action is required, otherwise stop the Oracle clusterware
//          stack that is running on the indicated node. The name and number
//          of the active node may be unknown.
4403, 0, "Values which are negative or greater than 4 are not allowed for parameter %s.\n"
4404, 0, "The following nodes did not reply within the allotted time:\n%s"
// *Cause:  The clusterized command timed out before the specified nodes
//          responded to the command.
// *Action: Check if the nodes are online; also check for communications problems. 
//          Consider issuing the command locally on the specified node(s).
4405, 0, "The following nodes are unknown to Oracle High Availability Services:\n%s"
// *Cause:  The local Oracle High Availability Services is not in contact
//          with Oracle High Availability Services on the specified nodes.
// *Action: Check if the nodes are online and Oracle High Availability Services is running.
//          Check for communications problems and consider issuing the
//          command locally on the specified node(s).
/
/ CRSCTL translation message errors
/
4421, 0, "Failure %d retrieving translation for %s error %d.\n"
4422, 0, "Failure allocating %d bytes at error translation (%s/%d).\n" 
4423, 0, "Failure %d at %s with status %d.\n" 

/
/ Node key errors
/
4431, 0, "Insufficient resources to complete operation."

/
/ Cluster Synchronization Services connection errors
4451, 0, "Unable to communicate with the Cluster Synchronization Services daemon.\n"
4452, 0, "Failure in Cluster Synchronization Services initialization of the Oracle Cluster Registry.\n"
4453, 0, "Failure %d at Cluster Synchronization Services context initialization\n"

/
/ CLU init error
4460, 0, "Failure %d at CLU context initialization.\n"

/
/ Oracle Cluster Registry init failures
4471, 0, "Insufficient privileges at Oracle Cluster Registry initialization: %s\n"
4472, 0, "Oracle Cluster Registry initialization failed accessing Oracle Cluster Registry device: %s\n"
4473, 0, "Oracle Cluster Registry initialization failed with invalid format: %s\n"
4474, 0, "Unable to allocate memory in Oracle Cluster Registry initialization: %s\n"
4475, 0, "Unable to locate Oracle Home in Oracle Cluster Registry initialization: %s\n"
4476, 0, "Failure %d in main Oracle Cluster Registry context initialization: %s\n"

/
/ SCLS init errors
4480, 0, "Unable to allocate %d bytes at sclsctx.\n"

4481, 1, "Unable to spawn a process.\n"
//  *Cause:  There was an internal error while spawning a process.
//  *Action: Report the error to Oracle Support.
 
4482, 1, "A child process terminated abnormally.\n"
//  *Cause:  A child process exited due to an internal error.
//  *Action: Report the error to Oracle Support.
/
/ network errors
4501, 0, "Failed %d to retrieve max nodename size (%d) from Cluster Synchronization Services \n"
4502, 0, "Unable to allocate %d bytes for network name\n"
4503, 0, "Failed %d to retrieve local node number from Cluster Synchronization Services\n"
4504, 0, "Failed (%d/%d/%d) to retrieve private interconnect name\n"
4505, 0, "Unable to allocate %d bytes for network address\n"
4506, 0, "Failed %d to bind listening endpoint: %s\n"
4507, 0, "Insufficient user privileges\n"
4508, 0, "Failure %d querying configuration size from Cluster Synchronization Services.\n"
4509, 0, "Failure %d querying maximum nodename size from Cluster Synchronization Services.\n"
4510, 0, "Unable to allocate %d bytes at clssnsnodevec. \n"
4511, 0, "Unable to allocate %d bytes for nodenames. \n"
4512, 0, "Failure %d querying node configuration from Cluster Synchronization Services.\n"
4513, 0, "Failure %d querying nodename for node %d.\n"
4514, 0, "Unable to allocate %d bytes for nodename %d.\n"
4515, 0, "Failure %d looking up nodename for node %d.\n"
4516, 0, "Unable to allocate %d bytes of memory for node status\n"
4517, 0, "Failure %d looking up nodestate.\n"
4518, 0, "Unable to allocate %d bytes at crshome.\n"
4519, 0, "Insufficient privileges to read Cluster Synchronization Services voting file '%s'.\n"
4520, 0, "Unable to open Cluster Synchronization Services voting file '%s' with read access.\n"
4521, 0, "Failure %d checking the Cluster Synchronization Services voting file '%s'.\n"
4522, 0, "Not able to read adequate number of voting files\n"
4523, 0, "Wait duration (in seconds) not supplied.\n"
4524, 0, "Expecting the CRS daemons to be up within %d seconds.\n"
4525, 0, "Cluster Synchronization Services is active on these nodes. \n"
4526, 0, "Cluster Synchronization Services is inactive on these nodes. \n"
4527, 0, "Local node checking complete. Run root.sh on remaining nodes to start CRS daemons.\n"
4528, 0, "Cluster Synchronization Services is active on all the nodes. \n"
4529, 0, "Cluster Synchronization Services is online\n"
4530, 0, "Communications failure contacting Cluster Synchronization Services daemon\n"
4531, 0, "Permissions failure contacting Cluster Synchronization Services daemon\n"
4532, 0, "Failure %d contacting Cluster Synchronization Services daemon\n"
4533, 0, "Event Manager is online"
4534, 0, "Cannot communicate with Event Manager"
4535, 0, "Cannot communicate with Cluster Ready Services"
4536, 0, "reslist creation failed \n"
4537, 0, "Cluster Ready Services is online"
4538, 0, "Try again\n"
4539, 0, "User does not have privilege to check status of CRS \n"
4540, 0, "Cluster Synchronization Services initialization failed\n"
4541, 0, "Cant find initialized Oracle Cluster Registry \n"
4542, 0, "CRS does not appear to be healthy\n"
4543, 0, "clsz init failed while trying to start resources."
4544, 0, "Unable to connect to OHAS"
4545, 0, "Starting resources."
4546, 0, "Error while starting resources. Possible cause: CRSD is down."
4547, 0, "Successfully started CRS resources"
4548, 0, "Unable to connect to CRSD"
4549, 0, "Unexpected disconnect while executing shutdown request."
4550, 0, "Fatal CLSC error received."
4551, 0, "Successfully stopped Oracle Clusterware resources"
4552, 0, "Shutting down the Cluster Synchronization Services daemon. \n"
4553, 0, "Shutdown request successfully issued.\n"
4554, 0, "Communications failure sending shutdown.\n"
4555, 0, "Failure %d issuing shutdown request.\n"
4556, 0, "Attempting to start Oracle Clusterware stack \n"
4557, 0, "The CRS stack will be started shortly\n"
4558, 0, "Stopping Cluster Synchronization Services. \n"
4559, 0, "Failed %d to retrieve local node number from Cluster Synchronization Services.\n"
4560, 0, "Failed %d to retrieve nodename from Cluster Synchronization Services.\n"
4561, 0, "Failed %d to retrieve hostname from Cluster Synchronization Services."
4562, 0, "Configuration parameter %s is not defined.\n"
4563, 0, "Insufficient user privileges.\n"
4564, 0, "Configuration parameter %s is now set to %d for node %s.\n"
4565, 0, "Configuration parameter %s is now set to %d.\n"
4566, 0, "Configuration parameter %s was already undefined.\n"
4567, 0, "Configuration parameter %s is now undefined for node %s.\n"
4568, 0, "Configuration parameter %s is now undefined. \n"
4569, 0, "Missing Oracle username parameter.\n"
4570, 0, "Operation presently unsupported. \n"
4571, 0, "Cluster Synchronization Services data dump triggered.\n"
4572, 0, "Communications failure contacting Cluster Synchronization Services daemon.\n"
4573, 0, "Permissions failure contacting Cluster Synchronization Services daemon.\n"
4574, 0, "Failure %d contacting Cluster Synchronization Services daemon.\n"
4575, 0, "Missing module name parameter.\n"
4576, 0, "Module parameter is longer than 256 characters.\n"
4577, 0, "Token=%s\n"
4578, 0, "Module=%s Level=%s\n"
4579, 0, "%s\nFailed to make a debug message\n"
4580, 0, "Failed to set Cluster Synchronization Services trace level to Oracle Cluster Registry"
4581, 0, "Set CRSD Debug Module: %s  Level: %s\n"
4582, 0, "Dumping State for %s objects\n"
4583, 0, "Set Resource Debug Module: %s  Level: %s\n"
4584, 0, "Cluster Synchronization Services trace dump triggered.\n"
4585, 0, "The following are the Cluster Synchronization Services modules:: \n"
4586, 0, "The following are the CRS modules:: \n"
4587, 0, "The following are the Event Manager modules:: \n"
4588, 0, "Failure in memory allocation for prochdl.\n"
4589, 0, "CLSFMT returned with error [%d].\n"
4590, 0, "Failed %d to query Cluster Synchronization Services configuration information.\n"
4591, 0, "Failed to allocate memory for %d nodes\n"
4592, 0, "Failed %d to determine bitmap of configured nodes.\n"
4593, 0, "Voting disk file name %s too big.\n"
4594, 0, "Now formatting voting disk: %s.\n"
4595, 0, "Specify a single disk %s and %s.\n"
4596, 0, "Cluster is not in a ready state for online disk addition\n"
4597, 0, "Failed %d to initialize Oracle Cluster Registry security attributes.\n"
4598, 0, "Voting file named %s already configured as %s.\n"
4599, 0, "Failure %d opening root of Oracle Cluster Registry.\n"
4600, 0, "Failure %d adding keys to Oracle Cluster Registry.\n"
4601, 0, "Failed to initialize voting file %s.\n"
4602, 0, "Failed %d to add voting file %s.\n"
// *Cause: An attempt to add a voting file failed.  The number following
//        "Failed" is a return code, which can be:
//         1 - internal OCSSD server error;
//         8 - rejected by OCSSD;  
//         15- insufficient privileges for this operation; 
//         19- version incompatibility between client and server;
// *Action: Respond based on the return code as follows:  
//         15 - adjust privileges or use a different userid
//         19 - ensure that compatible versions are installed
//         others - report to Oracle Support Services
4603, 0, "Successful addition of voting disk %s.\n"
4604, 0, "Cluster is not in a ready state for online disk removal\n"
4605, 0, "No voting files are configured, skipping the operation.\n"
4606, 0, "No voting file found that matches the path specified %s.\n"
4607, 0, "Only one voting file %s configured. Add another disk before deleting the last one.\n"
4608, 0, "Failure %d with Cluster Synchronization Services while deleting voting disk.\n"
// *Cause: An attempt to delete a voting disk failed.  The number following
//        "Failed" is a return code, which can be:
//         1 - internal OCSSD server error;
//         8 - rejected by OCSSD;  
//         15- insufficient privileges for this operation; 
//         16- either the specified voting disk does not exist 
//             or you tried to delete a majority of voting disks;
//         19- version incompatibility between client and server;
// *Action: Respond based on the return code as follows:  
//         15 - adjust privileges or use a different userid
//         16 - review the voting disk configuration displayed by 
//              'crsctl query css votedisk' and 
//              correct your request accordingly
//         19 - ensure that compatible versions are installed
//         others - report to Oracle Support Services
4609, 0, "Error %d while trying to open voting file Oracle Cluster Registry key.\n"
4610, 0, "Failed %d to delete Oracle Cluster Registry keys for voting file.\n"
4611, 0, "Successful deletion of voting disk %s.\n"
4612, 0, "Located %d voting disk(s).\n"
4613, 0, "Failure %d in clssqlnum \n"
4614, 0, "Failure %d in clssnsqname for nodenum %d\n"
4615, 0, "Failure %d in clsvswversion for node %s\n"
// *Cause: Internal error.
// *Action: Contact Oracle Support Services.
4616, 0, "Oracle Clusterware version on node [%s] is [%s]\n"
4617, 0, "Failure %d in clsvactversion \n"
/ Related to message 4706.
4618, 0, "Oracle Clusterware active version on the cluster is [%s]\n"
4619, 0, "Failure at %s with code %d\n"
4620, 0, "Internal Error Information: \n  Category: %d\n Operation: %s\n  Location: %s\n  Other: %s\n  System Dependent Information: %s\n"
4621, 0, "Oracle High Availability Services autostart is disabled."
4622, 0, "Oracle High Availability Services autostart is enabled."
4623, 0, "Node name not supplied.\n"
4624, 0, "Failure %d in clssnsqanum for node %s\n"
4625, 0, "Failure to allocate %d bytes for username.\n"
// *Cause:  System is out of memory.
// *Action: Free up memory on system and retry.
4626, 0, "The requested setting must be between %d and %d.\n"
// *Cause:  An attempt to change a setting to an out of bounds value.
// *Action: Retry with the setting within the proper limits.
4627, 0, "Unable to lock the configuration before making changes. %d\n"
// *Cause:  Failure in a CSS API acquiring a lock.
// *Action: Retry or contact support for information on the error code.
4628, 0, "Change to configuration failed, but was successfully rolled back.\n"
// *Cause:  See accompanying messages for explanation of cause.
// *Action: No action is required. This indicates that no damage was done.
4629, 0, "Unable %d to mark unformat information on voting file %s\n"
// *Cause:  Probably an unreadable / unwritable voting file was being removed.
// *Action: If cause is correct, this is ignorable, but not ideal.
4630, 0, "Unable to apply correct permissions to new voting file %s.\n"
// *Cause:  An attempt to set permissions on a new voting file failed.  
//          This message is accompanied by others that provide OS-specific 
//          details of the error.
// *Action: Examine the OS-specific error and correct it if possible; 
//          otherwise, specify a different voting file.
4631, 0, "Unable %d to undo initialization of voting file.\n"
// *Cause:  Could not roll back format of voting file.
// *Action: Disk should be cleaned out before an attempt to add again.
4632, 0, "Unable %d to roll back OCR settings for voting file.\n"
// *Cause:  Could not remove temporary changes to OCR adding voting file.
// *Action: Shut down the cluster and restart. 
//          New voting file must be removed with "crsctl delete css votedisk".
4633, 0, "This could take several minutes.\n"
// *Cause: CRS daemons is engaged in an activity take could potentially take a long time.
// *Action: None.

4634, 0, "Retrying stop resources.\n"
// *Cause: crsctl command is trying again to stop resources.
// *Action: None.

4635, 1, "Internal error '%d' while attempting to send shutdown request"
// *Cause: This is an internal error.
// *Action: If retrying does not work, contact Oracle support

4636, 0, "Failure %d in clsvrelversion"
// *Cause: Internal error.
// *Action: Contact Oracle Support Services.

4637, 0, "Oracle High Availability Services release version on the local node is [%s]\n"
// *Cause: Output message, not an error.
// *Action: None.
4638, 0, "Oracle High Availability Services is online"
4639, 0, "Could not contact Oracle High Availability Services"
4640, 0, "Oracle High Availability Services is already active"
4641, 0, "Oracle Clusterware autostart is enabled"
4642, 0, "Oracle Clusterware autostart is disabled"
4643, 1, "Oracle Clusterware autostart is incorrect or inconsistent"
4647, 0, "Configuration parameter %s is reset to default operation value.\n"
4648, 0, "Failed to create voting files on disk group %s.\n"
4649, 0, "Successfully replaced voting disk group with %s.\n"
4650, 0, "Failed to replace voting disk group with %s.\n"
4651, 1, "No resources found on server '%s'."
// *Cause: The server has no resources associated with it.
// *Action: Provide a server with resources running.
4652, 0, "Failure %d in clsvswversion for the local node"
// *Cause: Internal error.
// *Action: Contact Oracle Support Services.
4653, 1, "Server name '%s' contains invalid characters."
// *Cause: The name provided contains invalid characters.
// *Action: Use a server name with only alphanumeric characters.
4654, 1, "Server '%s' could not be found."
// *Cause: The name provided is not a known server's name.
// *Action: Use a known server's name.
4655, 1, "Resource '%s' could not be found."
// *Cause: The name provided is not a known resource's name.
// *Action: Use a known resource's name.
4656, 1, "Resource '%s' is not running on server '%s'."
// *Cause: The resource is not on the server the user specified.
// *Action: User must type a known server.
4657, 1, "Source and destination servers are the same."
// *Cause: The source and destination servers may not be the same.
// *Action: Specify a different destination server.
4658, 1, "The clusterware stack on node %s is not completely down.\n" 
// *Cause: There is indication that the clusterware stack is still up. 
// *Action: Please shutdown the entire clusterware stack before deleting the node.
4659, 1, "Error while trying to unpin node %s.\n"
// *Cause: An internal error happened during this operation.
// *Action: Please contact Oracle Support Services.  
4660, 1, "Could not find node %s to delete.\n"
// *Cause: The node to be deleted could not be found because it has not been a
//         member of this cluster recently.
// *Action: Please check the name provided.  If the name is correct, the node has
//          been automatically deleted because it was inactive for a long time and
//          no further action is required to delete the node from the cluster.
4661, 1, "Node %s successfully deleted.\n"
//  *Cause: A request to delete a node completed.
//  *Action: None. 
4662, 1, "Error while trying to delete node %s.\n"
// *Cause: Some internal error happened during this operation.
// *Action: Please contact Oracle Support Services. 
4663, 1, "Could not find node %s to pin.\n"
// *Cause: The indicated node is not an active node in the cluster.
// *Action: Ensure that the node name is correct and that Oracle Clusterware 
//          is running on the node.
4664, 3, "Node %s successfully pinned.\n"
//  *Cause: A request to pin a node completed.
//  *Action: None. 
4665, 1, "Error while trying to pin node %s.\n"
// *Cause: An internal error happened during this operation.
// *Action: Please contact Oracle Support Services. 
4666, 1, "Could not find node %s to unpin.\n"
// *Cause: The indicated node is not an active node in the cluster.
// *Action: Ensure that the node name is correct and that Oracle Clusterware 
//          is running on the node.
4667, 3, "Node %s successfully unpinned.\n"
//  *Cause: A request to unpin a node completed.
//  *Action: None. 
4668, 1, "This ASM diskgroup does not contain voting disks to be deleted\n"
//  *Cause: The ASM diskgroup name provided does not contain voting files.
//  *Action: Provide the right ASM diskgroup name.
4669, 4, "Failed to set parameter %s to %d due to conflicting parameter %s; the new value for %s must be less than %d.\n"
//  *Cause: An attempt was made to set a new value to a configuration
//          parameter which conflicts with another parameter's current value.
//  *Action: Set the value of this parameter to a lower value than
//           what is indicated in the message.
4670, 3, "Failed to unset parameter %s due to conflicting parameter %s currently set to %d.\n"
//  *Cause: An attempt was made to unset a configuration parameter which
//          conflicts with another parameter's current value.
//  *Action: Set the conflicting parameter to a value which can coexist with
//           proposed parameter change before submitting this parameter change.
4671, 1, "This command is not supported for ASM diskgroups.\n"
//  *Cause: The command 'crsctl add css votedisk' contains one or more ASM 
//          diskgroups in the list of voting files. Voting files may be 
//          migrated to and from ASM, but diskgroups cannot be added or
//          deleted.
//  *Action: Use an appropriate 'crsctl set' command to add ASM diskgroups. 
//           Use 'crsctl replace votedisk' command to migrate voting files to ASM.
//           
4672, 3, "Successfully backed up the Voting File for Cluster Synchronization Service.\n"
//  *Cause: The backup of the voting file completed successfully.
//  *Action: None. 
4673, 0, "Oracle High Availability Services version on the local node is [%s]\n"
// *Cause: Output message, not an error.
// *Action: None.
4674, 0, "Cannot add invalid user '%s' to CRS Admin list."
// *Cause: An attempt was made to add an invalid username to the CRS Admin
// list. 
// *Action: Reissue the command with a valid username.
 

4675, 0, "Failed to get logfilesize for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Please contact Oracle Support Services. 
4676, 0, "Successful get logfilesize %d for Cluster Synchronization Services.\n"
// *Cause: The operation is done successfully for Cluster Synchronization Services.
// *Action: None.
4677, 0, "Failed to get %s for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Please contact Oracle Support Services. 
4678, 0, "Successful get %s %d for Cluster Synchronization Services.\n"
// *Cause: The 'get' operation was performed successfully.
// *Action: None.
4679, 0, "Failed to unset logfilesize for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Please contact Oracle Support Services. 
4680, 0, "Successful unset logfilesize for Cluster Synchronization Services.\n"
// *Cause: The 'unset' operation was performed successfully.
// *Action: None.
4681, 0, "Failed to unset priority for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Please contact Oracle Support Services. 
4682, 0, "Successful unset priority for Cluster Synchronization Services.\n"
// *Cause: The 'unset' operation was performed successfully.
// *Action: None.

4683, 0, "Failed to set parameter %s to %d for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Please contact Oracle Support Services. 

4684, 0, "Successful set of parameter %s to %d for Cluster Synchronization Services.\n" 
// *Cause: The 'set' operation was performed successfully for Cluster Synchronization Services.
// *Action: None.

4685, 0, "Failed to set logfilesize %d for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Please contact Oracle Support Services. 
4686, 0,"Successful set logfilesize %d for Cluster Synchronization Services.\n"
// *Cause: The 'set' operation was performed successfully for Cluster Synchronization Services.
// *Action: None.
4687, 1, "Shutdown command has completed with errors."
// *Cause: Processing of a shutdown command has completed with errors.
// *Action: Refer to preceding error message(s) for information about
// the errors that occurred.
4688, 2, "Oracle Clusterware is already stopped on server '%s'"
// *Cause: Oracle Clusterware is not running on the indicated server.
// *Action: None.
4689, 2, "Oracle Clusterware is already stopped"
// *Cause: Oracle Clusterware is not running.
// *Action: None.
4690, 1, "Oracle Clusterware is already running on '%s'"
// *Cause: Oracle Clusterware is already running on the indicated server.
// *Action: None.
4691, 1, "Oracle Clusterware is already running"
// *Cause: Oracle Clusterware is already running.
// *Action: None.
4692, 0, "Cluster Ready Services is online in exclusive mode"
// *Cause: Cluster Ready Services is limited to providing internal
//         services to other Oracle Clusterware components. External
//         Cluster Ready Services are not available.
// *Action: When in exclusive mode, Oracle Clusterware components are
//          dedicated to the repair or reconfiguration of the Oracle
//          Cluster Registry, voting files or both.  Oracle Clusterware
//          should be down and remain down on every other cluster node.
//          Only commands that check or stop the stack, interact with
//          Cluster Synchronization Services or aid in Clusterware repair
//          or reconfiguration should be issued.


4693, 1, "Failed to back up the voting file for Cluster Synchronization Service.\n"
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services. 
4694, 0, "Number of voting files cannot exceed %d. Failed to add voting files.\n"
// *Cause: The request to add voting files would cause the maximum number 
//         allowed to be exceeded.
// *Action: Specify fewer voting files to add so that the maximum is not exceeded, 
//          or include the -purge option on 'crsctl add css votedisk' to replace 
//          the existing set of files with an allowable number of new files. 


4695, 0, "Voting disk addition failed because this disk %s is a duplicate of an existing voting disk with matching File Universal ID %s.\n"
// *Cause:  This disk is already a part of the current cluster.
// *Action: None needed.
4696, 4, "Failed to set parameter %s to %d due to conflicting parameter %s; the new value for %s must be greater than %d.\n"
//  *Cause: An attempt was made to set a new value to a configuration
//          parameter which conflicts with another parameter's current value.
//  *Action: Set the value of this parameter to a higher value than
//           what is indicated in the message.
4697, 0, "This command must be executed by Operating System user '%s'."
//  *Cause: A crsctl command was executed by the wrong Operating System user.
//  *Action: The specified Operating System user should execute the command.

/ CRSCTL - CTSSD (4700 - 4729)
4700, 3, "The Cluster Time Synchronization Service is in Observer mode.\n"
//  *Cause: Vendor time synchronization software exists on at least one of the
//          nodes in the cluster.
//  *Action: None
4701, 3, "The Cluster Time Synchronization Service is in Active mode.\n"
//  *Cause: Vendor time synchronization software is not detected on any of the
//          nodes in the cluster.
//  *Action: None
4702, 3, "Offset (in msec): %s\n"
//  *Cause: None
//  *Action: None
4703, 3, "The Cluster Time Synchronization Service is Offline.\n"
//  *Cause: The Cluster Time Synchronization Service is not running on the
//          current node.
//  *Action: None
4704, 3, "Shutdown of Clusterware failed on node %s.\n"
// *Cause: The shutdown did not complete successfully. One or more of the
//         internal operations experienced an error that is reported in
//         previous messages.
// *Action: Examine the error message(s) preceding this message and correct
//          the problem(s) they describe.
4705, 3, "Start of Clusterware failed on node %s.\n"
// *Cause: The start did not complete successfully. One or more of the
//         internal operations experienced an error that is reported in
//         previous messages.
// *Action: Examine the error message(s) preceding this message and correct
//          the problem(s) they describe.
/ Related to message 4618.
4706, 0, "Oracle Clusterware active version on the cluster is [%s]. The cluster upgrade state is [%s].\n"

//////////////////////////////////////////
/ CRSCTL - SET|GET JAZN (4730 - 4750)
/////////////////////////////////////////
4730, 1, "Command aborted due to an internal error\n"
//  *Cause: An inconsistent internal state was detected.
//  *Action: Call Oracle Support Services.
4731, 1, "Specified file %s could not be created.\n"
//  *Cause: JAZN configuration file required by the OC4J container could not 
//           be created.
//  *Action: Ensure that the directory path exists and that its permissions 
//           will allow the file to be created by oracle owner of clusterware
//           home.
4732, 1, "Could not be open file %s.\n"
//  *Cause: JAZN configuration file required by the OC4J container could not 
//          be opened.
//  *Action: Ensure that the directory path exists and that its permissions 
//           will allow the file to be created by oracle owner of clusterware
//           home.
4733, 1, "File %s does not exist.\n"
//  *Cause: The JAZN configuration file required by the OC4J container does 
//           not exist.
//  *Action: Ensure that the directory path exists and that its permissions 
//           will allow the file to be created oracle owner of the clusterware
//           home. 
4734, 1, "Filename was not specified.\n"
//  *Cause: filename was not supplied or was an empty string.
//  *Action: Re-try the command by specifying a valid JAZN configuration 
//           filename.
4735, 1, "Expected OCR key does not exist\n"
//  *Cause:  An infrastructure error occured because a required OCR key 
//           was missing.
//  *Action: Call Oracle Support Services.
4736, 1, "Operation on OCR key failed\n"
//  *Cause:  Operation on OCR key failed due to an OCR error.
//  *Action: Re-issue the command as oracle owner of clusterware home.
4737, 1, "Failed to allocate %d bytes of memory\n"
//  *Cause:  Could not allocate memory for internal buffers due to 
//           insufficient system memory resources
//  *Action: Correct the system memory resources problem and retry the command
4738, 1, "Size of file %s is too large\n"
//  *Cause:  Specified file size exceeds 65536 bytes.
//  *Action: Re-issue the command after reducing the size of the file.
4739, 1, "Could not close file %s \n"
//  *Cause: Due to an internal error the specified file could not be closed
//  *Action: Re-issue the command after verifying disk space, permissions 
//           and path.
4740, 1, "I/O operation on file %s failed.\n"
//  *Cause: Due to an internal error an I/O operation on the specified file 
//          failed.
//  *Action: Call Oracle Support if the problem persists.
4741, 1, "Insufficient permissions on OCR key\n"
//  *Cause:  Operation on OCR key failed due to insufficient permissions.
//  *Action: Re-issue the command as oracle owner of clusterware home.
4742, 1, "OCR updated with contents of %s (New = %d, Old = %d bytes)"
// *Cause: set jazn command was issued and OCR key was updated.
// *Action: None Required.
4743, 1, "File %s was updated from OCR(Size: %d(New), %d(Old) bytes)"
// *Cause: get jazn command was issued and specified file was updated with 
//         the contents from OCR key.
// *Action: None Required. 
4744, 0, "The CSSD is not running with real-time priority. It is running with priority base + nice.\n"
// *Cause: Priority value returned from 'crsctl get css priority' was as
//         displayed. In single instance high availability configurations,
//         the Cluster Synchronization Services daemon (CSSD) always has
//         priority Base + Nice and does not run real-time or at elevated 
//         priority.
// *Action: None Required. 
/

/
/ Overflow help messages
/
4801, 3, "  crsctl add {resource|type} <name> <options> \nwhere \n   name          Name of the OHAS entity \n   options       Options to be passed to the add command\n\n   See individual OHAS entity help for more details"
4802, 3, "  crsctl add {resource|type} <name> <options>"
4803, 3, "  crsctl delete {resource|type} <name> [...] [<options>]\n  crsctl delete wallet -type <wallet_type> <options>"
4804, 3, "  crsctl query has releaseversion\n    Lists the Oracle Clusterware release version"
4805, 3, "  crsctl query has softwareversion\n    Lists the version of Oracle Clusterware software installed on the local node"
4806, 3, "  crsctl backup votedisk\n     Backup the voting disk." 
4807, 3, "  crsctl get clientid dhcp -cluname <cluster_name> -viptype <vip_type> [-vip <VIPResName>] [-n <nodename>]\n    Generate client ID's as used by RAC agents for configured cluster resources\nwhere\n    cluster_name    name of the cluster to be configured\n"
4808, 3, "  crsctl discover dhcp -clientid <clientid> [-port <port>]\n     Discover DHCP server\nwhere\n      clientid         client ID for which discovery will be attempted\n      port             The port on which the discovery packets will be sent\n"
4809, 3, "  crsctl request dhcp -clientid <clientid> [-port <port>]\n     Request DHCP lease for the client ID specified\nwhere\n      clientid         client ID for which DHCP lease request will be attempted\n      port             The port on which the DHCP lease request packets will be sent\n"
4810, 3, "  crsctl release dhcp -clientid <clientid> [-port <port>]\n     Release DHCP lease for the client ID specified\nwhere\n      clientid         client ID for which DHCP lease release request will be attempted\n      port             The port on which the DHCP lease release packets will be sent\n"
4811, 3, "  crsctl start testdns [-address <IP_address>] [-port <port>][-domain <GNS_domain>] [-once][-v]\n    Start a test DNS listener that listens on the given address at the given port and for specified domain\nWhere\n    IP_address          IP address to be used by the listener (defaults to hostname)\n    port                The port on which the listener will listen. Default value is 53.\n    domain              The domain query for which to listen. By default, all domain queries are processed."
4812, 3, "  crsctl stop testdns [-address <IP_address>] [-port <port>] [-v]\n    Stop the test DNS listener that listens on the given address and at the given port\nWhere\n    IP_address          IP address on which testdns was started (defaults to hostname)\n"
4813, 3, "  crsctl query dns -servers\n     Lists the system configured DNS server, search paths, attempt and timeout values\n"
4814, 3, "  crsctl query socket udp [-address <address>] [-port <port>]\n     Verifies that a daemon can listen on specified address and port\nWhere\n       address             IP address on which socket needs to be created\n       port                port on which socket needs to be created"
4815, 3, "  crsctl query dns -name <name> [-dnsserver <DNS_server_address>] [-port <port>] [-attempts <attempts>] [-timeout <timeout>] [-v]\n    Returns a list of addresses returned by DNS lookup of the name with the specified DNS server\nWhere\n    name                Fully qualified domain name to lookup\n    DNS_server_address  Address of the DNS server on which name needs to be looked up\n" 
4816, 3, "    vip_type        Type of VIP resource: HOSTVIP, SCANVIP, or APPVIP\n    VIPResName      User defined application VIP name (required for APPVIP vip_type)\n    nodename        Node for which the client ID is required (required for HOSTVIP vip_type)\n"
4817, 3, "\n     port                The port on which the listener is listening. Default value for the port is 53. \n    -v                  Verbose output"
// Msg 4051 consists of msg 4051 and msg 4818.
4818, 3, "  crsctl modify wallet -type <wallet_type> <options> \nwhere \n    wallet_type   Type of wallet i.e. , APPQOSADMIN, APPQOSUSER or APPQOSDB.\n    options       Options to be passed to the modify command"
// Msg 4062 consists of msg 4062 and msg 4819.
4819, 3, "     -w                Resource type filter (e.g., \"BASE_TYPE = cluster_resource\")\n     -g                Check if resource types are registered\n     -p                Print static configuration\n     -f                Print full configuration"
// Msg 4063 consists of msgs 4063, 4064, 4065 and 4820.
4820, 3, "     -g                Check if resources are registered\n     -k                Cardinality ID\n     -d                Degree ID\n     -n                Server name\n     -s                Get target servers for relocation\n     -t                Tabular display\n     -dependency       Display resource dependencies, default is start dependencies\n     -stop             Display resource stop dependencies\n     -pullup           Display resource pullup dependencies"
// Msg 4066 consists of msgs 4066 and 4821.
4821, 3, "     -w                Server filter (e.g., \"STATE = ONLINE\")\n     -g                Check if servers are registered\n     -p                Print static configuration\n     -v                Print runtime configuration\n     -f                Print full configuration"
// Msg 4074 consists of msgs 4074, 4075, 4822 and 4823
4822, 3, "     resName         Add named resource\n     typeName        Resource type\n     filePath        Attribute file\n     attrName        Attribute name\n     value           Attribute value\n     server          Server name"
4823, 3, "     cid             Resource cardinality ID\n     did             Resource degree ID\n     -f              Force option\n     -i              Fail if request cannot be processed immediately"
// Msg 4076 consists of msgs 4076, 4824 and 4834
4824, 3, "     typeName       Add named resource type\n     baseTypeName   Base resource type\n     filePath       Attribute file\n     attrName       Attribute name\n     defaultValue   Default value"
// Msg 4077 consists of msgs 4077 and 4825
4825, 3, "     attrName        Attribute name\n     value           Attribute value\n     -i              Fail if request cannot be processed immediately\n     -f              Force option"
// Msg 4080 consists of msgs 4080 and 4826
4826, 3, "     name            Name is required for APPQOSDB wallets.\n     user_name       User to be added to wallet.\n     passwd          Indication that password will be specified. Password will be read from standard input."
// Msg 4116 consists of msgs 4116, 4117, 4827, 4120, 4125 and 4811 OR
//                      msgs 4116, 4117, 4827, 4119, 4122, 4125 and 4811
4827, 3, "     -d               Resource degree ID\n     -env             Attribute overrides for this command\n     -f               Force option\n     -i               Fail if request cannot be processed immediately"
4828, 3, "    net_mask             Subnet mask for the IP to start\n    interface_name       Interface on which to start the IP\n"
4829, 3, "    port                Port on which DNS server is listening\n    attempts            Number of retry attempts\n    timeout             Timeout in seconds\n"
4830, 3, "  crsctl unset css ipmiconfig\n    Unsets the IPMI configuration and deletes the associated Oracle Registry entries."
4831, 3, "  crsctl set css <parameter> <value>\n    Sets the value of a Cluster Synchronization Services parameter\n"
4832, 3, "  crsctl set css {ipmiaddr|ipmiadmin} <value>\n    Sets IPMI configuration data in the Oracle registry\n"
4833, 3, "  crsctl set css votedisk {asm <diskgroup>|raw <vdisk>[...]}\n    Defines the set of voting disks to be used by CRS\n"
// Msg 4076 consists of msgs 4076, 4824 and 4834
4834, 3, "     typeFlags      One or more flag values separated by '|':\n       CONFIG         Attribute may be configured\n       READONLY       Attribute is read-only\n       REQUIRED       Attribute value is required\n     -i             Fail if request cannot be processed immediately"
// Msg 4055 consists of msgs 4055, 4835 and 4836
4835, 3, "     typeName       Modify named resource type attributes\n     attrName       Attribute name\n     defaultValue   Default value\n     typeFlags      One or more flag values separated by '|':"
4836, 3, "       CONFIG         Attribute may be configured\n       READONLY       Attribute is read-only\n       REQUIRED       Attribute value is required\n     -f             Force option\n     -i             Fail if request cannot be processed immediately"

/
/ Get/Set log/trace 4900 - 4950
/
4900, 3, "  crsctl get {log|trace} {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>,...\"\n    Get the log/trace levels for specific modules"
4901, 3, "  crsctl get {log|trace} {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>,...\"\n where \n   mdns          multicast Domain Name Server\n   gpnp          Grid Plug-n-Play Service\n   css           Cluster Synchronization Services\n   crf           Cluster Health Monitor\n   crs           Cluster Ready Services\n   ctss          Cluster Time Synchronization Service\n   evm           EventManager\n   gipc          Grid Interprocess Communications\n   <name1>, ...    Module names (\"all\" for all names)"
4902, 3, "  crsctl get log res <resname> \n    Get the log level for an agent"
4903, 3, "  crsctl get log res <resname> \n where\n   <resname>     Resource name"
4904, 3, "  crsctl set {log|trace} {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>=<lvl1>,...\"\n    Set the log/trace levels for specific modules within daemons"
// Msg 4905 consists of msg 4905 and msg 4924.
4905, 3, "  crsctl set {log|trace} {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>=<lvl1>,...\"\n where \n   mdns          multicast Domain Name Server\n   gpnp          Grid Plug-n-Play Service\n   css           Cluster Synchronization Services\n   crf           Cluster Health Monitor\n   crs           Cluster Ready Services\n   ctss          Cluster Time Synchronization Service\n   evm           EventManager"
4906, 3, "  crsctl set log res <resname>=<lvl>\n    Set the log levels for agents"
4907, 3, "  crsctl set log res <resname>=<lvl>\n where\n <resname>     Resource name\n   <lvl>                  Agent log levels"
4908, 0, "%s Module: %s ignored; log level not specified"
4909, 0, "%s Module: %s ignored; trace level not specified"
4910, 0, "Set %s Module: %s  Log Level: %d"
4911, 0, "Set %s Module: %s  Trace Level: %d"
4912, 0, "Get %s Module: %s  Log Level: %d"
4913, 0, "Get %s Module: %s  Trace Level: %d"
4914, 0, "%s Module: %s ignored invalid component key name used"
4915, 0, "Argument '%s' has an incorrect number of parameters"
4916, 0, "Add %s Log Module: %s"
4917, 0, "Add %s Trace Module: %s"
4918, 0, "Remove %s Log Module: %s"
4919, 0, "Remove %s Trace Module: %s"
4920, 0, "Set Resource %s Log Level: %s"
4921, 0, "Get Resource %s Log Level: %s"
4922, 0, "%s module: %s ignored; module level out of bounds (range 0 - 65535)"
// *Cause: Module log/trace level was out of bounds (range 0 - 65535).
// *Action: Specify a log/trace level within the valid range (0 - 65535).
4923, 0, "%s module: %s ignored; module level is invalid (range 0 - 65535)"
// *Cause: Module log/trace level was invalid (range 0 - 65535).
// *Action: Specify a log/trace level within the valid range (0 - 65535).
4924, 3, "   gipc          Grid Interprocess Communications\n   <name1>, ...    Module names (\"all\" for all names)\n   <lvl1>, ...     Module log/trace levels"
4925, 3, "'all' module keyword was specified with other module names"
// *Cause: The module keyword 'all' already refers to all module names.
// *Action: When referring to all modules, use 'all' without duplicate references to other module names.
/
/ Resource/type parsing messages 4980 - 4999
/
4980, 3, "Duplicate value %s specified for resource attribute %s"
// *Cause: A duplicate value was specified for a resource attribute.
// *Action: Specify only one value for a resource attribute.
4981, 3, "Duplicate value %s specified for type attribute keyword %s"
// *Cause: A duplicate value was specified for a type attribute keyword.
// *Action: Specify only one value for DEFAULT_VALUE, FLAGS and TYPE per type attribute.
4982, 3, "Valid type attribute keyword %s specified outside a type attribute"
// *Cause: A valid type attribute keyword was specified outside a type attribute.
// *Action: Specify the ATTRIBUTE type attribute keyword before specifying the DEFAULT_VALUE, FLAGS or TYPE type attribute keywords.
4983, 3, "Invalid type attribute keyword %s specified"
// *Cause: An invalid type attribute keyword was specified.
// *Action: Specify only the valid type attribute keywords ATTRIBUTE, DEFAULT_VALUE, FLAGS and TYPE.
//          
4984, 3, "Duplicate definition for type attribute %s"
// *Cause: The same type attribute was named on more than one ATTRIBUTE keyword.
// *Action: Define a type attribute only once.
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ 5000 - 5500 Reserved for RAC Agents
/
///////////////////////////////////////////////////////////////////////////

5000, 0, "Expected resource %s does not exist in agent process"
// *Cause: The expected resource must have been created by Oracle Configuration tools.
// *Action: Check that the resource was not manually deleted. If not the case call Oracle Support.
5001, 0, "Expected dependency in resource %s on a resource of type %s does not exist"
// *Cause: The expected resource dependency must have been created by Oracle Configuration tools.
// *Action: Check that the resource dependency was not manually removed.
5002, 0, "Agent action was aborted"
// *Cause: Agent action was aborted either due to action timeout expiry or the user canceled the action.
// *Action: Retry the operation.
/
5003, 0, "Invalid attribute value: '%s' for attribute %s"
// *Cause: An attribute value passed to the Agent was NULL or invalid.
// *Action: Give the correct value to the attribute and retry.
/
5004, 0, "Cannot find listener endpoint for listener %s"
// *Cause: listener endpoint not found.
// *Action: Check listener.ora for that listener.
/
5005, 0, "IP Address: %s is already in use in the network"
// *Cause: The VIP resource attempted to use an IP address already in use in
// the network.
// *Action: Use srvctl to re-create vip or scanvip specifying an IP address 
// which is not being used in the network and retry the operation.
/
5006, 0, "Unable to automatically select a network interface which has subnet mask %s and subnet number %s"
// *Cause: The subnet mask and subnet number configured for the resource did not
// match the subnet mask and subnet number of any network interface on 
// this node.
// *Action: Provide a subnet mask and subnet number which matches at least one
// network interface's subnet mask and subnet number using srvctl remove and add
// vip and retry the operation.
/
5007, 0, "Cannot remove the primary IP %s from the network interface"
// *Cause: The primary IP of the network interface was incorrectly configured as
// the VIP.
// *Action: Use 'srvctl remove' and 'srvctl add vip' or 'srvctl remove' and 
// 'srvctl add scan' to provide the correct IP address for the VIP and 
// retry the operation. 
/
5008, 0, "Invalid attribute value: %s for the network interface"
// *Cause: The network interface value did not match the 
// subnet mask and subnet number of any network interface on the node.
// *Action: Modify the network interface's value such that the subnet mask and 
// subnet number matches the subnet mask and subnet number of at least one 
// network interface on the node using 'srvctl remove' and 'srvctl add vip' and 
// retry the operation.
/
5009, 0, "The VIP address %s does not belong to the subnet %s"
// *Cause: The VIP's subnet number and the network interface's subnet
// number did not match.
// *Action: Make the VIP's subnet number match the network interface's 
// subnet number using 'srvctl remove' and 'srvctl add vip' or 'srvctl remove' 
// and 'srvctl add scan' and retry the operation. 
/
5010, 0, "Update of configuration file \"%s\" failed: details at \"%s\" in \"%s\""
// *Cause: An attempt to open the specified file failed. Common causes are
// that the file does not exist, or the file permissions prohibit access.
// *Action: Check that the file exists and has the proper permissions.
/
5011, 0, "Check of resource \"%s\" failed: details at \"%s\" in \"%s\""
// *Cause: The check of the database or Automatic Storage Management instance
// failed.
// *Action: Check the database or ASM instance alert log and the referenced 
// Oracle Clusterware trace file for additional information.
//  Recover the instance if necessary.
//
/
5012, 0, "Check of service resource \"%s\"  failed: details at \"%s\" in \"%s\""
// *Cause: The check of the preconnect service failed because it could not
// run on the same node as the main service.
// *Action: Check the referenced Oracle Clusterware trace file for additional
// information. 
// Start the preconnect service on a different node.
//
/
5013, 0, "Agent \"%s\" failed to start process \"%s\" for action \"%s\": details at \"%s\" in \"%s\""
// *Cause: The named agent failed to start the named process for the
//  named action.
// *Action: Check the referenced Oracle Clusterware trace file for additional
// operating system specific information. Refer to operating system
// documentation to correct the error.
//
/
5014, 0, "Agent \"%s\" timed out starting process \"%s\" for action \"%s\": details at \"%s\" in \"%s\""
// *Cause: The named agent aborted the named process because the process
// failed to respond within the timeout period. 
// *Action: Check the agent log files for further information
//  
/
/
5015, 0, "Agent timed out waiting for a response from the DHCP server"
// *Cause: Agent and the DHCP server were not able to communicate with 
// each other. Common causes of this failure are due to the DHCP server not 
// running, or improper DHCP server configuration, or the DHCP server
// running out of DHCP leases. 
// *Action: Identify the cause of the problem from the DHCP server
// log files. If the problem is due to the DHCP server running out of leases, 
// increase the number of addresses which can be served by the DHCP server. 
/
5016, 0, "Process \"%s\" spawned by agent \"%s\" for action \"%s\" failed: details at \"%s\" in \"%s\""
// *Cause: The named process failed to complete succesfully.
// *Action: Check details in the agent log for error information from the spawned process. 
//
/
5017, 0, "The resource action \"%s %s\" encountered the following error: \n%s. For details refer to \"%s\" in \"%s\"."
// *Cause:  The following error occured during the resouce action.
// *Action: Examine the accompanying error messages and respond accordingly.
//
/
5018, 0, "%s Removed unused HAIP route:  %s / %s / %s / %s"
// *Cause: A potentially conflicting route in the same subnet as the HAIP
//  addresses was found and removed to prevent routing conflicts.
// *Action: Validate that the route described was not actually in use.
/
5019, 0, "All OCR locations are on ASM disk groups [%s], and none of these disk groups are mounted. Details are at \"%s\" in \"%s\"."
// *Cause: OCR was configured on ASM disk groups, and all of the listed
//  disk groups failed to mount.
//  The possible causes are:
//  1. A disk was not accessible.
//  2. A disk  in a normal or high redundancy disk group failed after the
//     most recent dismount.
//  3. The ASM_DISKSTRING in the SPFILE or the GPnP profile was incorrect.
// *Action:
//  Check the ASM alert logs for more information.
//  To correct disk access or failure issues either:
//    a) restore access to the disks in the disk group and mount
//    the disk group (via ASMCMD or SQL).
//    or
//    b) Issue a force mount to the disk group to offline missing
//    disks and mount a normal or high redundancy disk group.
//  To correct the ASM_DISKSTRING in the SPFILE and propagate the
//  change to the GPnP profile, in sqlplus, issue the SQL command
//  "ALTER SYSTEM SET ASM_DISKSTRING <discovery_string> SCOPE=BOTH"
/
5020, 0, "Not all endpoints are registered for listener %s"
// *Cause: Listener agent failed to register all endpoints to listener.
// *Action: Check listener log file for that listener.
/
/Alert
5021, 0, "Check of storage failed: details at \"%s\" in \"%s\""
// *Cause: The check of ASM storage failed because the storage was not accessible.
// *Action: Check the Oracle Clusterware alert log and the referenced Oracle Clusterware
// trace file for additional information.
/
/Alert
5022, 0, "Stop of resource \"%s\" failed: current state is \"%s\""
// *Cause: The named resource failed to stop.
// *Action: Ensure no one is using the resource and reissue the stop.
// 
/
/Alert
5023, 0, "Failed to unmount file system \"%s\"; details at \"%s\" in \"%s\""
// *Cause: The named file system resource failed to unmount.
// *Action: Determine which operating system processes are accessing the mount point using an
// operating system command such as 'fuser' or 'lsof' for UNIX-based platforms or 'handle' 
// for Windows. Close, shut down, or terminate applications and processes 
// accessing the mount point, then retry.
// 
/
/Alert
5024, 0, "Unmounting file system \"%s\""
// *Cause: A 'stop' of the file system resource mounted on the indicated path 
// started.
// *Action: This is an informational message only.
// 
/
/Alert
5025, 0, "File system \"%s\" unmounted"
// *Cause: A 'stop' of the file system resource mounted on the indicated path 
// completed normally.
// *Action: This is an informational message only.
// 
/
/Alert
5026, 0, "Failed to clean mount point \"%s\"; details at \"%s\" in \"%s\""
// *Cause: The clean of the volume failed because one or more processes on the
// system were accessing the mount point.
// *Action: Determine which operating system processes are accessing the mount point using an
// operating system command such as 'fuser' or 'lsof' for UNIX-based platforms or 'handle' 
// for Windows. Close, shut down, or terminate applications and processes 
// accessing the mount point, then retry.
// 
/
/Alert
5027, 0, "Agent failed to initialize ARP devices required for starting the HAIP resource"
// *Cause: The resource could not be started because the ARP devices failed to start on the same node.
// *Action: Manually check the ARP devices on the same node and then start the resource.
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ 5501 - 5600 Reserved for Reporter
/
///////////////////////////////////////////////////////////////////////////

5501, 0, "Unable to connect to eONS server on port %d"
// *Cause: The eONS server may not be active or listening on a different port.
// *Action: Ensure that the eONS resource is ONLINE and listening on the above port.
5502, 0, "Invalid event template %s"
// *Cause: The event template specified is invalid.
// *Action: The event template format must be <PROPERTY|ELEMENT>(<attribute name>=<literal|%resource attribute name%>) ...
5503, 0, "Error creating the eONS subscriber"
// *Cause: The eONS server may not be active.
// *Action: Ensure that the CRS eONS resource is in ONLINE state.
5504, 1, "Node down event reported for node '%s'."
// *Cause: The specified node was not responsive.
// *Action: Restart the specified node.

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////
/
/   5601-5700: MDNS specific messages
/
//////////////////////////////////////////////////////////////////////

5601, 0, "MDNS: %s"
// *Cause:  None, generic bypass mdns message.
// *Action: None.
/
5602, 0, "mDNS service stopping by request."
// *Cause:  MDNSD stopping by OHASD request.
// *Action: None.
/


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ Placement Policy specific messages: 5701 - 5800
/
///////////////////////////////////////////////////////////////////////////

5701, 1, "Unknown placement policy name: '%s'\n\"Balanced\" used"
5702, 1, "Resource '%s' is already running on '%s'"
5703, 1, "Target member should not be in the exclusion list"
5704, 1, "Trying to start on a dead member ..."
5705, 1, "Failed to get required resources"
// *Cause:  There was an internal error while evaluating the required 
//          resources for the subject resource.
// *Action: Contact Oracle Support Services.
5706, 1, "No more members to consider"
// *Cause:  There was no host found on which to start the resource based on 
//          the placement policy. 
// *Action: Check the placement policy and the required resources for the
//          subject resource.
5707, 1, "Failed after successful dependency consideration"
// *Cause:  There was no host found on which to start the resource based on 
//          the placement policy. 
// *Action: Check the placement policy and the required resources for the
//          subject resource.
5708, 1, "Resource '%s' is not relocatable (current and target state not running)"
5709, 1, "Resource '%s' is already running on member '%s'"
// *Cause:  An attempt was made to start a resource on a host while it is 
//          already running on that host.
// *Action: This is an insignificant error. Check the operation being 
//          performed. 
5711, 1, "Trying to relocate to a dead member ..."
5712, 1, "Failed to get connected resources"
5715, 1, "Failed to get resources depending on this resource"
5716, 1, "Resources depending on '%s' are running"
5717, 1, "Resource %s (%s) is not available on %s"
5718, 1, "Resource %s (%s) is already running on %s"
5719, 1, "Resource %s (%s) cannot run on %s"
5722, 1, "Resource %s (%s) is running on %s"
5723, 1, "Trying to relocate a non-runnable resource '%s'?"
5724, 1, "Failed to failover any subset of the connected resources to '%s'"
5725, 1, "Trying to start a non-runnable resource '%s'?"
5726, 1, "Trying to stop a non-runnable resource '%s'?"
5727, 1, "Resource '%s' cannot be failed over (wrong state)"
5728, 1, "Dependency analysis failed because of:\n'%s'"

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ AGFW specific messages : 5801 - 5999
/
///////////////////////////////////////////////////////////////////////////
5801, 1, "Agent path is null or does not resemble a filesystem path"
// *Cause: Unable to spawn the agent program because of incorrect agent path.
// *Action: Fix the agent path using 'crsctl modify type'.
5802, 1, "Unable to start the agent process"
// *Cause: An attempt to start the agent process failed. 
// *Action: Ensure that the agent path is correct and has the proper permissions, and retry the command.
5803, 1, "Agent is not running"
5804, 1, "Communication error with agent process"
5805, 1, "Missing the required action callback in agent"
// *Cause: Unable to execute resource's command.
// *Action: Ensure that agent executable or action script contains the missing function.
5806, 1, "Agent internal error"
5807, 1, "Agent failed to process the message"
5808, 1, "Unknown message received by the agent process"
5809, 1, "Failed to execute '%s' value of '%s' for '%s'. Error information '%s', Category : %d, OS error : %d"
// *Cause: Unable to spawn the resource action script due to incorrect path value or incorrect permissions or other OS error.
// *Action: Correct the action script path and permissions or check and fix the reported OS error.
5810, 1, "Attempt to add a duplicate resource '%s'. Details at %s in %s."
// *Cause: An identical resource was already being monitored.
// *Action: Rename the resource and retry the operation.
5811, 1, "Failed to read ORA_CRS_HOME from environment. Details at %s in %s."
// *Cause: The ORA_CRS_HOME environment variable was not set correctly.
// *Action: This variable is set during CRS installation. If necessary, reinstall CRS.
5812, 1, "Could not get local hostname. Details at %s in %s."
// *Cause: The hostname could not be read.
// *Action: Check that the hostname for the local machine is valid. If the problem persists, contact Oracle Support Services.
5813, 1, "Could not change directory to '%s'. Details at %s in %s."
// *Cause: The specified path is inaccessible to the agent process.
// *Action: Check that the specified path exists.
5814, 1, "Agent '%s' started with invalid arguments. Details at %s in %s."
// *Cause: An invalid parameter was supplied to the agent.
// *Action: Contact Oracle Support Services.
5815, 1, "Agent '%s' could not find any base type entry points for type '%s'. Details at %s in %s."
// *Cause: Action entry points were not defined for this agent.
// *Action: No action necessary if this is a script agent. If this is not a script agent, define action points in your agent code.
5816, 1, "Agent '%s' could not start implicit monitoring for resource '%s'. Details at %s in %s."
// *Cause: The resource was currently disabled and hence could not be monitored.
// *Action: Enable the resource.
5817, 1, "Caught exception from user code for command '%s'. Details at %s in %s."
// *Cause: An exception was thrown from the user code when an action entry point was called.
// *Action: This is due to an error in the agent user code. Modify the agent's code to resolve this.
5818, 1, "Aborted command '%s' for resource '%s'. Details at %s in %s."
// *Cause: Execution of the specified command was aborted due to a timeout.
// *Action: Restart the resource manually. If the problem persists, contact Oracle Support Services.
5819, 1, "Could not abort command '%s' for resource '%s'. Details at %s in %s."
// *Cause: Attempt to abort the specified command failed.
// *Action: Define an abort action entry point for the agent. 
5820, 1, "Agent '%s' failed to initialize server process address. Details at %s in %s."
// *Cause: Agent could not connect to the server process.
// *Action: Contact Oracle Support Services.
5821, 1, "Agent '%s' is started with wrong user '%s'. Details at %s in %s."
// *Cause: An incorrect owner was specified for the agent.
// *Action: Make sure CRSD has enough privileges to spawn programs as the value specified as the 'owner' in the ACL attribute.
5822, 1, "Agent '%s' disconnected from server. Details at %s in %s."
// *Cause: Agent could not connect to server process.
// *Action: Contact Oracle Support Services.
5823, 1, "Could not initialize agent framework. Details at %s in %s."
// *Cause: Initialization of the agent failed.
// *Action: Contact Oracle Support Services.
5824, 1, "Could not initialize server connect string '%s'. Details at %s in %s."
// *Cause: Incorrect server connect string was specified in the environment.
// *Action: Contact Oracle Support Services.
5825, 1, "Agent '%s' is unresponsive and will be restarted. Details at %s in %s."
// *Cause: The specified agent did not respond and will be restarted automatically.
// *Action: None.
5826, 1, "Agent '%s' could not read environment variable '%s'. Details at %s in %s."
// *Cause: The agent could not read a required environment variable.
// *Action: Contact Oracle Support Services.
5827, 1, "Could not find information for resource '%s'. Details at %s in %s."
// *Cause: The specified resource was not found in the internal list of resources.
// *Action: Check the agent parameters and restart the resource manually.
5828, 1, "Could not start agent '%s'. Details at %s in %s."
// *Cause: Creation of the agent process failed. 
// *Action: Contact Oracle Support Services.
5829, 1, "Failed to get definition for resource '%s'. Details at %s in %s."
// *Cause: The definition of the resource could not be determined.
// *Action: Delete the resource and add it again using the crsctl command.
5830, 1, "Invalid path '%s' found for agent filename. Details at %s in %s."
// *Cause: The path that was specified for the agent was incorrect.
// *Action: Check that the path exists and is readable.
5831, 1, "Agent '%s' has exceeded maximum failures and has been disabled. Details at %s in %s."
// *Cause: The specified agent has failed too many times.
// *Action: Contact Oracle Support Services.
5832, 1, "Agent '%s' was unable to process commands. Details at %s in %s."
// *Cause: Agent was unable to process commands.
// *Action: Contact Oracle Support Services.
5833, 1, "Cleaning resource '%s' failed as part of reboot-less node fencing"
// *Cause: A resource 'clean' action associated with reboot-less node eviction
//         encountered an error. This is an expected occurence in most cases.
// *Action: None
5837, 1, "Unable to open environment file '%s'."
// *Cause: The environment file specified could not be opened.
// *Action: Verify that the filename, its location and its permissions are correct.
5838, 1, "Syntax error in environment file '%s'."
// *Cause: The environment file specified did not have key value pairs in the
//         correct format.
// *Action: Correct the key value format and retry. Consult the Clusterware Administration
//          manual for the correct format.

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ CRSD specific messages: 6001 - 6999
/
///////////////////////////////////////////////////////////////////////////

6001, 1, "User does not have permission to start CRSD."
// *Cause: Unable to start CRSD due to insufficient permissions.
// *Action: Start CRSD as a privileged user.
6002, 1, "Directory '%s' not found."
6003, 3, "CRSD exiting. '%s'."
6004, 1, "Could not fork background process."
6005, 1, "Could not get hostname."
6006, 1, "Another CRSD may be running, could not obtain lock file '%s'." 
6007, 1, "Could not communicate with Event Manager."
// *Cause: Unable to communicate with Event Manager daemon.
// *Action: Run the 'crsctl check evmd' command to determine whether Event Manager daemon is properly configured and is running.
6008, 1, "CRSD can not create UI socket."
6009, 1, "CRSD can not create message socket."
6010, 1, "portmap error, mapping E2E on port %d."
6011, 1, "All network reserved ports in use."
6012, 3, "Usage \"CRSD [-0|-1|-2]\""
6013, 1, "Unable to send '%s' request to running Manager"
6014, 1, "Could not establish dependency graph."
6015, 1, "Oracle Clusterware has experienced an internal error. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.

/
/ License checking error
6020, 0, "Software is not licensed for use on this system."

6021, 2, "Could not set system resource limits for Clusterware: \"ulimit -%s %s\"."
// *Cause: A ulimit command issued internally to set system resource limits failed.
// *Action: Ensure that the correct resource limit values are set in the user profile and limits.conf.


///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
/
// Messages used as "pass-through" for various components.
/
///////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////
/
// GPnP Error Code translations. (7000 - 7999)
/
///////////////////////////////////////////////////////////////////////

7000, 1,  "Generic GPnP success"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7001, 1,  "Generic GPnP error"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support. 
/

7002, 1, "Not enough memory"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support. 
/

7003, 1, "GPnP facility initialization failed"
// *Cause:
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7004, 1, "This feature is unsupported or not implemented"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/
 
7005, 1, "Requested item not found"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7006, 1, "Insufficient buffer size"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7007, 1, "Error in file I/O operation"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7008, 1, "Invalid permissions for the operation"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7009, 1, "Bad authority id"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7010, 1, "Key does not exist"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7011, 1, "Bad key"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7012, 1, "Hostname not found"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7013, 1, "GPNPD daemon is not running"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7014, 1, "Attempting to set a bad value"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7015, 1, "Bad hostname value"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7016, 1, "Bad authority id value"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7017, 1, "Not a cluster member"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7018, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7019, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7020, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7021, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7022, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7023, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7024, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/


7025, 1, "Duplicate profile"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7026, 1, "Profile is not given or not available"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7027, 1, "Badly formed profile"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7028, 1, "Profile is too big to be valid"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7029, 1, "Profile is older than the current"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7030, 1, "Profile exists in memory only, not saved"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7031, 1, "Request retry message from GPNPD"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7032, 1, "Value already set in profile"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7033, 1, "Request timed out"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7034, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7035, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7036, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7037, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7038, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7039, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7040, 1, "Generic XML error"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7041, 1, "GPnP XML profile is not well formed"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7042, 1, "Invalid GPnP SOAP message"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7043, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7044, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7045, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7046, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/


7047, 1, "Communication timeout"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7048, 1, "Communication error"
// *Cause: Other than timeout. 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7049, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7050, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7051, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7052, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7053, 1, "Resource discovery error"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7054, 1, "Invalid URL for discoverable resource"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7055, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7056, 1, "OCR Init error"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7057, 1, "Reinit OCR to a different bootlevel"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7058, 1, "OCR error"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7059, 1, "Global OCR is not available"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7060, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7061, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7062, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7063, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7064, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7065, 1, "GPnP wallet error"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7066, 1, "Requested GPnP wallet is not found"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7067, 1, "Invalid GPnP wallet password given"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7068, 1, "GPnP wallet is too big to be valid"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7069, 1, "GPnP wallet is corrupted or invalid"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7070, 1, "Bad or missing private key in GPnP wallet"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7071, 1, "Bad or missing public key in GPnP wallet"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7072, 1, "Bad or missing certificate in GPnP wallet"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7073, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7074, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7075, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7076, 1, "Failed to init crypto libraries"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7077, 1, "Crypto library error"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7078, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7079, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7080, 1, "GPnP profile has too many signatures"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7081, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7082, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7083, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7084, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7085, 1, "GPnP profile unsigned"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7086, 1, "GPnP profile signature invalid" 
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7087, 1, "GPnP profile valid peer signature"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7088, 1, "GPnP profile valid PA signature"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7089, 1, "GPnP profile was signed with a different wallet"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

// 7090, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7091, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7092, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7093, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

// 7094, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7095, 1, "GPnP tool usage"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

7096, 1, "GPnP tool version"
// *Cause: 
// *Action: This error should not be visible to the user. If it occurs, please
//          contact Oracle Customer Support.
/

////////////////////////////////////////////////////////////////////////////
//
//      End GPnP error messages.
//
////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////
/
// Reboot Advisory (AKA Last Gasp) alert log messages (8000-8199)
/
///////////////////////////////////////////////////////////////////////

08000, 0, "unable to obtain local host name for reboot advisory log file scan"
// *Cause:  An attempt to retrieve the local host name failed.  The scan
//          for reboot advisory files will not use host name criteria and so
//          may report occurrences for other nodes as well as this one.
// *Action: Report this error to Oracle Support Services.
/

08001, 0, "an error occurred accessing reboot advisory log file location: %s"
// *Cause:  The scan for reboot advisory log files was unable to access the
//          indicated file system location.  The location was skipped, so
//          any reboot advisory files that it contains will not be reported.
//          This message is accompanied by CLSU- messages containing
//          details of the access error.
// *Action: Respond based on the error described by the accompanying CLSU-
//          messages.  This may involve re-creating the directory or
//          changing its permissions.
/

08002, 0, "an error occurred searching reboot advisory log file location: %s"
// *Cause:  The scan for reboot advisory log files was unable to read the next
//          file name from the indicated file system location.  No further
//          processing of reboot advisory files from that location occurs.
//          This message is accompanied by CLSU- messages containing
//          details of the access error.
// *Action: Respond based on the error described by the accompanying CLSU-
//          messages.
/

08003, 0, "reboot advisory log file: %s is unexpectedly empty"
// *Cause:  The scan for reboot advisory log files encountered a file that
//          was empty.  This might happen (rarely) if a component is
//          initializing its use of reboot advisory at the same time the scan
//          is running.  Processing of other files in the location continues.
// *Action: Frequent occurrence of this message should be reported to
//          Oracle Support Services.
/

08004, 0, "an error occurred reading reboot advisory log file: %s"
// *Cause:  The scan for reboot advisory log files experienced a read error
//          on a reboot advisory file.  No further processing is done for that
//          file, but the scan continues with other files.  This message
//          is accompanied by CLSU- messages containing details of the
//          read error.
// *Action: Respond based on the accompanying CLSU- messages.
/

08005, 0, "an error occurred closing reboot advisory log file: %s"
// *Cause:  The scan for reboot advisory log files experienced a close error on
//          a reboot advisory file.  The scan continues with other files.  This
//          message is accompanied by CLSU- messages containing details of
//          the close error.
// *Action: Report this error to Oracle Support Services.
/

08006, 0, "an error occurred opening reboot advisory log file: %s"
// *Cause:  The scan for reboot advisory log files experienced an error when it
//          opened a reboot advisory file.  The scan continues with other files.
//          This message is accompanied by CLSU- messages containing details
//          of the open error.
// *Action: If the error indicated in the accompanying CLSU- messages is one that
//          can be corrected, do so.  Otherwise, report this error to Oracle
//          Support Services.
/

08007, 0, "an error occurred closing reboot advisory log file location: %s"
// *Cause:  The scan for reboot advisory log files experienced an error when it
//          closed the indicated file system location.  Processing of other
//          reboot advisory locations (if any) continues normally.
//          This message is accompanied by CLSU- messages containing
//          details of the close error.
// *Action: Report this error to Oracle Support Services.
/

08008, 0, "%s"
// *Cause:  Operating system error data related to reboot advisory file
//          processing was returned.  The error data is packaged in a CLSU- message
//          that follows "CRS-08008:".  One or more of these messages
//          appears after a message announcing the error condition.
// *Action: Look up the embedded CLSU- message for an explanation of the
//          operating system error data.  If there is no CLSU- message ID present,
//          contact Oracle Support Services.
/

08009, 0, "reboot advisory log file: %s contains invalid data (length %d, error code %d)"
// *Cause:  A reboot advisory log record read from the indicated file contained
//          incorrect data.
// *Action: Report this error to Oracle Support Services.
/

08010, 0, "invalid network reboot advisory message detected (length %d, error code %d)"
// *Cause:  A reboot advisory record received over the network was improperly
//          formed or contained incorrect data.
// *Action: Report this error to Oracle Support Services.
/

08011, 0, "reboot advisory message from host: %s, component: %s, with time stamp: %s"
// *Cause:  A reboot advisory message was detected.  During Oracle Clusterware
//          startup on a given host, messages recently written to disk on that host
//          before a reset or reboot are detected and announced.  Subsequently,
//          network reboot advisory messages may be announced as they occur.  These
//          are reported by hosts other than the one being reset or rebooted.
//          This message is accompanied by other messages containing details on
//          what led to the reset or reboot.  The time stamp in this message
//          begins with either 'U' (denoting UTC time) or 'L' (denoting
//          local time as viewed by the issuing host).  Note that a given
//          reset or reboot event can produce multiple occurrences of these
//          messages on multiple hosts in the cluster.
// *Action: Use the reboot advisory message(s) to determine why Oracle Clusterware
//          caused a reset or reboot of the affected host, and respond
//          accordingly.  Refer to the discussion of reboot advisories in the
//          Oracle Clusterware administration documentation for additional
//          guidance.
/

08012, 0, "reboot advisory message from a higher Oracle Clusterware version detected"
// *Cause:  A reboot advisory message from a higher version installation of
//          Oracle Clusterware was detected.  This is an expected
//          occurrence with network reboot advisories when there are nodes with
//          a higher Oracle Clusterware version than this node (such as during
//          an upgrade).  It is an unexpected condition with file reboot
//          advisories.
// *Action: The reboot advisory message is displayed in a following CRS-08013
//          message in a "raw" text form.  In the case of network reboot
//          advisories, the explanatory message text should be readable and
//          useful to determine the cause of the node reboot.  If the
//          reboot advisory message is from a file, report this message to
//          Oracle Support Services.
/

08013, 0, "reboot advisory message text: %s"
// *Cause:  An explanatory text message associated
//          with a reboot advisory announced in a preceding CRS-08011 or CRS-08012
//          message was displayed.  These text messages are always written in US English
//          locale.
// *Action: Refer to the descriptions of messages CRS-08011 and -08012, and
//          to the Oracle Clusterware documentation on reboot advisories.
/

08014, 0, "reboot advisory binary data (%d bytes%s) follows:"
// *Cause:  Binary data associated with a reboot advisory message was displayed.
//          It is followed by one or more lines of CRS-08015 message containing
//          the binary data formatted in hexadecimal.  If an asterisk appears
//          inside the parentheses, an invalid data length was detected.
// *Action: Refer to the description of message CRS-08011 and -08012, and
//          to the Oracle Clusterware documentation on reboot advisories.
/

08015, 0, "%04X    %s"
// *Cause:  Hexadecimal display of binary data included in a reboot advisory log
//          message was displayed.  The first number is an offset and is
//          followed by up to 16 bytes of data.
// *Action: Refer to the description of message CRS-08011 and -08012, and
//          to the Oracle Clusterware documentation on reboot advisories.
/

08016, 0, "an error occurred determining the location for reboot advisory log files"
// *Cause:  The search for reboot advisory log files was unable to determine
//          the file system location used for those files.  Processing
//          of reboot advisory files is skipped.  This message is accompanied
//          by CLSU- messages containing failure details.
//          This is an internal error.
// *Action: Report this error to Oracle Support Services.
/

08017, 0, "location: %s has %d reboot advisory log files, %d were announced and %d errors occurred"
// *Cause:  This summary message is written during Oracle Clusterware startup if
//          one or more reboot advisory log files was found and examined.
// *Action: This message is informational, but if the error count is nonzero
//          the associated messages (earlier in the alert log) should be examined.
/

08018, 0, "warning: missing cluster identity data for reboot advisory message validation"
// *Cause:  During Oracle Clusterware start up, an attempt to obtain the identity of
//          the cluster failed.  Processing continues normally, but network
//          reboot advisories from nodes in other clusters may be reported in
//          this cluster's alert log.
// *Action: Report this error to Oracle Support Services.

08019, 0, "warning generated by the initialization of the reboot advisory in the CSS agent, %s"
// *Cause:  During initialization of the reboot advisory, a warning was generated
// *Action: Report this warning to Oracle Support Services.

08020, 0, "error generated by the initialization of the reboot advisory in the CSS agent, %s"
// *Cause:  During initialization of the reboot advisory, an error was generated.
// *Action: Report this error to Oracle Support Services.
///////////////////////////////////////////////////////////////////////
/
// end of Reboot Advisory alert log messages (8000-8199)
/
///////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////
/
// CHM/IPD related messages (9000-9999)
/
///////////////////////////////////////////////////////////////////////

//OCLUMON CLIENT SIDE MESSAGES
9000, 0, "Failed to allocate memory."
// *Cause: During intialization, memory could not be allocated.
// *Action: Report this error to Oracle Support Services.

9001, 0, "Internal Error"
// *Cause: An internal error occurred.
// *Action: Report this error to Oracle Support Services.

9002, 0, "%s"

//9003, 0, This message is free
// *Cause: 
// *Action: 

9004, 0, "Error reading from standard input"
// *Cause: Could not read commands from the command line.
// *Action: Report this error to Oracle Support Services.

9005, 0, "Quoted string not ended"
// *Cause: An unmatched " was found in the command entered.
// *Action: Put in the corresponding quote or remove the unmatched quote.

9006, 0, "Could not set environment, exiting."
// *Cause: Error occurred during initialization of oclumon.
// *Action: Report this to Oracle Support Services.

// 9007, 0, This message is free
// *Cause: 
// *Action: 

9008, 0, "Unknown verb %s"
// *Cause: Unknown or invalid verb passed to oclumon.
// *Action: Use 'oclumon -h' in command line or help command in interactive mode
//          to see the supported verbs.

9009, 0, "Error %s: Parsing error. Invalid arguments given."
// *Cause: Invalid or unknown arguments passed. 
// *Action: Refer to product documentation or to command online help for an
//          explanation of verbs and arguments.

9010, 0, "Error %s: mandatory data not supplied"
// *Cause: Mandatory data not supplied to the command.
// *Action: Refer to product documentation or to command online help for an
//          explanation of verbs and arguments.

9011, 0, "Error %s: Failed to initialize connection to the Cluster Logger Service"
// *Cause: Error occurred while connecting to the Cluster Logger Service.
// *Action: Ensure that Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the given node.

9012, 0, "Error %s: Error sending query to the Cluster Logger Service"
// *Cause: Error occurred while sending query to the Cluster Logger Service.
// *Action: Ensure that the Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the given node.

9013, 0, "Error %s: Invalid data received from the Cluster Logger Service"
// *Cause: Invalid or unknown data received from the Cluster Logger Service.
// *Action: Ensure that the Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the given node.

9014, 0, "Error: Corrupt reply from the Cluster Logger Service"
// *Cause: Invalid or unknown data received from the Cluster Logger Service.
// *Action: Make sure that the version of both master and client installation
//          is same. Also, check the connectivity between master and client
//          using the 'ping'.

9015, 0, "Error %s: Connection timed out"
// *Cause: Connection timed out while connecting to the Cluster Logger Service.
// *Action: Ensure that the Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the given node.

// 9016, 0, This message is free
// *Cause: 
// *Action:

9017, 0, "Error: Invalid or unknown reply received from the Cluster Logger Service"
// *Cause: Error occurred in the data received.
// *Action: Make sure that the version of both master and client installation
//          is same. Also, check the connectivity between master and client.

9018, 0, "Error %s: No arguments supplied"
// *Cause: No argument was supplied with the command.
// *Action: Some commands need arguments with them. Refer to the product
//          documentation or to the online help display.

9019, 0, "Error %s: No parameter %s supported"
// *Cause: A wrong parameter was passed with the command.
// *Action: Refer to the command help and pass the correct parameters.

9020, 0, "Error %s: No master node name given"
// *Cause: The master node name was not passed in the command.
// *Action: Pass the appropriate master node name with the command.

9021, 0, "Error %s: Invalid or no start time given"
// *Cause: A start time was not provided or the time was passed in 
//         the wrong format.
// *Action: Pass the correct start time. For correct format, refer to 
//          command help.

9022, 0, "Error %s: Invalid or no end time given"
// *Cause: A end time was not provided or the time was passed in 
//         the wrong format.
// *Action: Pass the correct end time. For correct format, refer to 
//          command help.

9023, 0, "Error %s: Time not given or in wrong format or invalid"
// *Cause: Time was not provided or was invalid.
// *Action: Pass the correct and valid time. For correct format, refer to command
//          help.

9024, 0, "Error %s: No node name given"
// *Cause: Node name not provided.
// *Action: Provide a node name in the command. Refer to the product
//          documentation or to the command online help for information.

9025, 0, "Error %s: No disk ID name given"
// *Cause: Disk ID was not given in the command with -diskid.
// *Action: Pass a valid disk ID with -diskid option.

9026, 0, "Error %s: No parameter given"
// *Cause: The parameter was not passed in the query.
// *Action: Pass appropriate parameter for query. Refer to the product
//          documentation or to the command online help for information.

9027, 0, "Error %s: Parameter %s is not supported with this verb"
// *Cause: Invalid or unknown parameter passed.
// *Action: Pass the correct parameter. Refer to the product
//          documentation or to the command online help for information.

9028, 0, "Error %s: No NIC ID given"
// *Cause: NIC ID was not given in the command with -nicid.
// *Action: Pass a valid NIC ID with -nic option.

9029, 0, "Error %s: No PID given"
// *Cause: PID was not given in the command with -pid.
// *Action: Pass a valid PID with -pid option.

9030, 0, "Error %s: No region given"
// *Cause: Incorrect or no region given with -c option.
// *Action: Pass a valid region with -c option. Refer to the product
//          documentation or to the command online help for information.

9031, 0, "Argument %s not supported with this verb %s. -h for help."
// *Cause: Unknown or invalid argument passed with the command.
// *Action: Refer to the product documentation or to the command 
//          online help for information on supported arguments.

9032, 0, "Invalid hour given in the time argument"
// *Cause: Invalid hour in the time string was passed.
// *Action: Pass a valid time string in accordance with the format. 
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9033, 0, "Invalid minutes given in the time argument"
// *Cause: Invalid minutes in the time string was passed.
// *Action: Pass a valid time string in accordance with the format. 
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9034, 0, "Invalid seconds given in the time argument"
// *Cause: Invalid seconds in the time string was passed.
// *Action: Pass a valid time string in accordance with the format. 
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9035, 0, "Arguments not in proper format, or invalid arguments"
// *Cause: Invalid arguments given. 
// *Action: Pass  a valid verb and correct arguments for it.
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9036, 0, "Invalid Cluster Health Monitor repository size given"
// *Cause: Non-numeric value or value out of range given for Cluster Health Monitor repository size.
// *Action: Specify Cluster Health Monitor repository size in the valid range.
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9037, 0, "%s Error: Node name not given. -disk, -nic and -proc need node name"
// *Cause: The required node name was not provided for -disk, -nic, or -proc.
// *Action: Provide a node name with -n option. Refer to the product
//          documentation or to the command online help for information
//          on supported arguments.

9038, 0, "Error: -s and -e need to be specified together"
// *Cause: Either -s or -e is missing.
// *Action: Start and end time need to be given together for range queries,
//          which cannot be unbounded. Refer to the product documentation 
//          or to the command online help for information on supported arguments. 

9039, 0, "Error %s: -i is not allowed with the range query"
// *Cause: The -i option was specified on an oclumon range query. 
// *Action: Use -i only in continuous mode.  Refer to the command inline
//          help or product documentation for more information.

9040, 0, "Error %s: Band value not given or incorrect"
// *Cause: The band value was not passed with -t option or was invalid.
// *Action: Provide a valid band value. Refer command help.

9041, 0, "Error %s: The -repos argument was specified without an option."
// *Cause: -repos was not provided with the option, generating a parsing error.
// *Action: Provide a valid option to -repos. Refer to the product documentation
//          or to the command online help for information on supported
//          arguments. 

9042, 0, "Error %s: No size given with resize"
// *Cause: A valid value was not provided with resize.
// *Action: Provide a valid numerical value with 'resize'. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments.

9043, 0, "Error %s: Non-numeric or invalid value for size: %s"
// *Cause: An invalid or non-numeric value was provided for size.
// *Action: Provide a valid numeric size. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments.

9044, 0, "No key specified with -getkey"
// *Cause: An option was not given with -getkey.
// *Action: Provide a valid key as an option with -getkey. 

9045, 0, "No key given for -get"
// *Cause: An option was not provided with -get.
// *Action: Provide a valid option with -get. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments.

9046, 0, "Invalid key given"
// *Cause: An unknown key was provided with -get.
// *Action: Provide a supported key with -get. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments. 

9047, 0, "Error %s: Error Dumping Log (return code:%d ) for node %s"
// *Cause: An error occurred while dumping local log.
// *Action: Report this error to Oracle Support Services. Cluster Health Monitor repository directory may be
//          unreachable, unreadable or incorrect.

9048, 0, "Error %s: No data received from the Cluster Logger Service after %d attempts"
// *Cause: Data was not received from the Cluster Logger Service after the given number of
//         attempts or data was not available. 
// *Action: None.

9049, 0, "Error %s: Cannot get environment variable CRFHOME"
// *Cause: An internal error occurred.
// *Action: Report this error to Oracle Support Services.

9050, 0, "Error %s: Too many host names"
// *Cause: Too many host names were provided. 
// *Action: Provide valid number of host names. Refer to the product
//          documentation or to the command online help for information. 

9051, 0, "Error %s: Invalid interval size given"
// *Cause: Non-numeric or invalid interval provided.
// *Action: Provide a valid numerical value for interval size. Refer to the
//          product documentation or to the command online help for 
//          information 

9052, 0, "Error %s: %s control not supported"
// *Cause: The given debug control was not supported.
// *Action: Provide a supported control. Refer to the
//          product documentation or to the command online help for
//          information.

9053, 0, "Key:value pair missing"
// *Cause: A required key:value pair was missing.
// *Action: Provide a valid key:value pair. Refer to the
//          product documentation or to the command online help for
//          information

9054, 0, "Incomplete or invalid parameters %s"
// *Cause: Incomplete or invalid parameters supplied.
// *Action: Provide the complete and correct parameters. Refer to the
//          product documentation or to the command online help for
//          information

9055, 0, "module:level given in invalid format or invalid value"
// *Cause: Invalid format or value specified for module:level.
// *Action: Provide correct module:level. Refer to the
//          product documentation or to the command online help for
//          information
 
9056, 0, "Error %s: Invalid Cluster Health Monitor repository location given"
// *Cause: Invalid Cluster Health Monitor repository location provided.
// *Action: Provide a directory with read and write permissions for Cluster Health Monitor repository location. Refer to the
//          product documentation or to the command online help for 
//          information. 

9057, 0, "Error %s: No response received from the Cluster Logger Service"
// *Cause: No data received from the Cluster Logger Service for the query.
// *Action: Ensure that the Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the given node.

9058, 0, "Error %s: Changing log level failed due to authentication failure"
// *Cause: Log level could not be changed due to authentication failure.
// *Action: Ensure that this command is run as root.

9059, 0, "Error %s: Changing log level failed due to connection failure"
// *Cause: A connection failure occurred while changing the log.
// *Action: Ensure that the daemons are running and are reachable from the
//          client node by using the 'ping' command for the given node.

9060, 0, "Error %s: Unable to send message due to memory allocation failure"
// *Cause: Memory could not be allocated for debug message.
// *Action: Report this error to Oracle Support Services.

9061, 0, "Error %s: Changing log level failed due to response time-out"
// *Cause: A time out happened while waiting for response.
// *Action: Report this error to Oracle Support Services.

9062, 0, "Error %s: Error in changing log level"
// *Cause: An error occured while changing log level.
// *Action: Report this error to Oracle Support Services.

9063, 0, "Given time range is more than 1 hour"
// *Cause: The time range provided with showtrail command was more than one
// hour.
// *Action: Provide a range of less than 1 hour for showtrail.

// 9064, 0, This message is free
// *Cause: 
// *Action:

9065, 0, "Disk ID not found"
// *Cause: Given disk ID was not found or not present in the interesting
// list.
// *Action: Provide a disk ID which is available at the start of the query
// range.

9066, 0, "Process ID not found"
// *Cause: Given process ID was not found.
// *Action: Provide a process ID which is available at the start of the query
// range.

9067, 0, "NIC ID not found"
// *Cause: Given NIC ID was not found.
// *Action: Provide a correct NIC ID.

9068, 0, "Error %s: -allnodes and -n must not be used together"
// *Cause: Both -allnodes and -n were supplied on a dumpnodeview command.
// *Action: Specify either -allnodes or -n with specific nodes.

9069, 0, "The new Cluster Health Monitor repository location is %s."
// *Cause:  The Cluster Health Monitor repository location was successfully replaced.
// *Action: None.

9070, 0, "The new Cluster Health Monitor repository retention time is %d seconds."
// *Cause:  The Cluster Health Monitor repository retention time was successfully modified.
// *Action: None.

// LOGUI side messages

9100, 0, "Error setting Cluster Health Monitor repository size"
// *Cause: An error occurred while setting Cluster Health Monitor repository size on the Cluster Logger Service.
// *Action: Report this error to Oracle Support Services.

9101, 0, "Error updating Cluster Health Monitor repository size in configuration file."
// *Cause: An error occurred while writing the Cluster Health Monitor repository size to configuration 
//         files.
// *Action: Report this error to Oracle Support Services.

9102, 0, "No data for the node at the given time"
// *Cause: Data was not found for the given node.
// *Action: This is an informational message only.

9103, 0, "No data available"
// *Cause: Data was not available for the query. 
// *Action: Make sure the System Monitor Service is running on the given node.

9104, 0, "No data available for the given nodes"
// *Cause: Data was not available for given nodes.
// *Action: Make sure the System Monitor Service is running on the given nodes.

9105, 0, "Internal Error on master"
// *Cause: An internal error on master caused this error.
// *Action: Report this error to Oracle Support Services.

9106, 0, "Data requested was outside Cluster Health Monitor retention time limits."
// *Cause: A request for data outside Cluster Health Monitor repository limit caused this error.
// *Action: Data needs to be requested in the proper Cluster Health Monitor repository limits. 
//          Refer to the product documentation for more information.

9107, 0, "Start time greater than end time"
// *Cause: A start time greater [or later] than end time caused an error.
// *Action: Make sure the start time is less than the end time 
//          for the given range query.

9108, 0, "Threshold out of acceptable range"
// *Cause: A threshold was specified that is outside the allowed range. 
// *Action: Make sure threshold is within the acceptable range. Refer
//          documentation or online help for more information

9109, 0, "New Cluster Health Monitor repository location same as the old location on node %s"
// *Cause: The new location specified for Cluster Health Monitor repository is same as the old location. 
// *Action: Provide a different location for Cluster Health Monitor repository. Refer
//          documentation or online help for more information.

9110, 0, "Cluster Health Monitor repository location not changed as the location provided does not exist on node %s."
// *Cause: The new location specified for Cluster Health Monitor repository does not exist. 
// *Action: Provide a different location for Cluster Health Monitor repository. Refer
//          documentation or online help for more information.

9111, 0, "Error updating Cluster Health Monitor repository location %s in configuration file."
// *Cause: An error occurred while writing the Cluster Health Monitor repository location to configuration files.
// *Action: Report this error to Oracle Support Services.

9112, 0, "Cluster Health Monitor repository location change on master completed. Changing on other nodes."
// "Document: NO"

9113, 0, "Cluster Health Monitor repository location change completed on all nodes. Restarting Loggerd."
// "Document: NO"

9114, 0, "Cluster Health Monitor repository location change failed on one or more nodes. Aborting location change."
// *Cause: An error occurred while setting Cluster Health Monitor repository location on the Cluster Logger Service.
// *Action: Retry specifying a valid location.

9115, 0, "Cluster Health Monitor repository size change completed on all nodes."
// "Document: NO"

9116, 0, "Cluster Health Monitor repository retention change failed on one or more nodes. Aborting retention change."
// *Cause: An error occurred while setting Cluster Health Monitor repository size on the Cluster Logger Service.
// *Action: Retry specifying a valid location.



// HELP MESSAGES FOR OCLUMON
//9200, 3, "For help from command line   : oclumon <verb> -h\nFor help in interactive mode : <verb> -h\nCurrently supported verbs are  :\nshowtrail, showobjects, dumpnodeview, manage, version, debug, analyze, quit, exit, and help\n"
9200, 3, "For help from command line   : oclumon <verb> -h\nFor help in interactive mode : <verb> -h\nCurrently supported verbs are  :\nshowobjects, dumpnodeview, manage, version, debug, quit, exit, and help\n"

// Manage help (9221 - 9240)
9221, 3, "\nMANAGE verb usage\n=================\n  manage [[-repos {resize <time>|changesize <memsize>|reploc <new_loc> [[-maxtime <time>]|\n         [-maxspace <memsize>]] }]|[-get <key1> <key2>..]]\n\n*Where\n"

9222, 3, ""
// Left blank so that it can be used in future when we bring back -m option
9223, 3, "  -repos       = Required to specify Cluster Health Monitor repository related options\n  -get         = Fetch manage information for one or more named keys\n  <key1> <key2>= <key> can be repsize, reppath, master, and replica\n  resize       = Option for resizing Cluster Health Monitor repository\n  <time>       = Size of Cluster Health Monitor repository in number of seconds\n"
9224, 3, "                 must be more than %d (1 hour) and less than %d (%d days)\n"
9225, 3, "  changesize   = Option for Change Cluster Health Monitor repository space limit\n  <memsize>    = Size of Cluster Health Monitor repository in megabytes\n"
9226, 3, "  reploc       = Option for Change Repository Location\n  <new_loc>    = Path to new directory e.g.: /opt/db\n  -maxtime     = Option to specify Cluster Health Monitor repository size in terms of elapsed seconds of data capture for new location\n  -maxspace    = Option to specify space limit for new Cluster Health Monitor repository location\n\n"
9227, 3, "*Requirements\n  The local system monitor service must be running to resize the Cluster Health Monitor repository.\n  The Cluster Logger Service must be running to resize Cluster Health Monitor repository.\n\n*Example :\n  manage -get MASTER REPLICA\n  manage -repos resize 86400\n  manage -repos changesize 6000\n  manage -repos reploc /opt/oracrfdb\n  manage -repos reploc /opt/oracrfdb -maxtime 86400\n  manage -repos reploc /opt/oracrfdb -maxspace 6000\n"

//  Debug Help (9241-9260)
9241, 3, "\ndebug verb usage\n================\ndebug [log <daemon> <module:level>][version]\n\n*Where\n  log            = To change log levels\n  <daemon>       = Daemon whose log level has to be changed\n                   Following daemons are supported :\n"
9242, 3, "                   osysmond, ologgerd, client, all\n"
9243, 3, "                   osysmond, ologgerd, client, all\n"
9244, 3, "  <module:level> = Module and level pair\n                   Supported osysmond modules:\n                   CRFMOND, CRFM, allcomp\n                   Supported ologgerd modules:\n                   CRFLOGD, CRFLDREP, CRFM, allcomp\n                   Supported client modules:\n                   OCLUMON, CRFM, allcomp\n"
9245, 3, "                   Supported oproxyd modules:\n                   CRFPROXY, allcomp\n"
9246, 3, "                   Supported log levels:\n                   0, 1, 2, 3\n  version        = To display versions\n\n*Note\n  modules supported for 'all' daemons: allcomp\n  All daemons support: CRFM, allcomp\n\n*Example:\n  debug log osysmond CRFMOND:3\n "

// Dumpnodeview help (9261-9300)
//9261, 3, "\ndumpnodeview verb usage\n=======================\ndumpnodeview [[-locallog [<path>] [-n <node1> <node2>]]|[[-allnodes]|[-n <node1> <node2>] [-last <time1>]|\n             [-cont]|[-s <time> -e <time>][-i <interval>][-v][-alert]]]\n\n"
//9261, 3, "\ndumpnodeview verb usage\n=======================\ndumpnodeview [[-allnodes]|[-n <node1> <node2>..] [-last <time1>]|\n             [-cont [-i <interval>]]|[-s <time> -e <time>][-v][-alert]]]\n\n"
9261, 3, "\ndumpnodeview verb usage\n=======================\nThe dumpnodeview command reports monitored records in the text format. The\ncollection of metrics for a node at a given point in time (a timestamp) is\ncalled a node view.\n\n* Usage\n  dumpnodeview [[-allnodes|-n <node1> ...] [-last <duration>|\n                -s <timestamp> -e <timestamp>][-v][-warning]]\n\n"
9262, 3, "*Where\n  -n <node1> ...   = Dump node views for given nodes\n"
9263, 3, "  -allnodes        = Dump node views for all nodes\n  -s <timestamp>   = Specify start time for range dump of node views\n  -e <timestamp>   = Specify end time for range dump of node views\n"
9264, 3, "                     Absolute timestamp should be in \"YYYY-MM-DD HH24:MI:SS\"\n                     format, for example \"2007-11-12 23:05:00\"\n  -warning         = Print node views with warnings only\n  -last <duration> = Dump the latest node views for a specified duration\n"
9265, 3, "                     Duration should be in \"HH24:MI:SS\" format, for example\n                     \"00:45:00\"\n"
9266, 3, "  -v               = Dump verbose node views\n\n"
9267, 3, "*Requirements and notes\n  To stop continuous display, use Ctrl-C on Linux or UNIX and Esc on Windows.\n  -s and -e need to be given together for range dumps of node views.\n  The local System Monitor Service (osysmond) should be running to get dumps.\n"
9268, 3, "  The Cluster Logger Service (ologgerd) should be running to get dumps.\n  When -warning is used in continuous mode, the prompt waits until interrupted.\n\n"
9269, 3, "*Defaults :\n  Mode      : Continuous mode\n\n*Example :\n  oclumon dumpnodeview -n node1 node2 node3 -last \"12:00:00\"\n\n"

// Showtrail Help  (9301-9340)
9301, 3, "\nSHOWTRAIL verb usage\n====================\n  showtrail [-n <node>] [[-diskid <diskid> <discparam>]|\n            [-nicid <nicid> <nicparam>]|[-pid <pid> <procparams>]|\n            [-sys <systemparam>]]\n"
9302, 3, "            [-c <regions>][-s <time> -e <time>]|[-last <time1>] [-h]\n\n*Where\n"
9303, 3, "  -n           = show trail for given node\n  <node>       = node name for which trail needs to be shown\n  -s           = To specify time for the start of range queries\n"
9304, 3, "  -e           = To specify time for the end of range queries\n  <time>       = Absolute time to be specified within quotes in\n                 \"YYYY-MM-DD HH24:MI:SS\" format, like \"2007-11-12 23:05:00\"\n"
9305, 3, "  -last        = To specify time for last queries\n  <time1>      = Time in \"HH24:MI:SS\" format to be given with -last option,like  \"00:45:00\"\n  -diskid      = To request trail of disk parameters\n"
9306, 3, "  -pid         = To request trail of process parameters\n  -nicid       = To request trail of NIC parameters\n  -sys         = To request trail of system-wide parameters\n  <diskid>     = Disk name whose parameter's trail is required\n"
9307, 3, "  <nicid>      = NIC ID whose parameters's trail is required\n  <pid>        = Process id whose parameter's trail is required\n  <discparams> = Disk parameter whose trail is required\n                 Following disk parameters are available:\n                 qlen, totalwaittime\n"
9308, 3, "  <nicparams>  = NIC parameter whose trail is required\n                 Following NIC parameters are available:\n                 effectivebw , errors\n"
9309, 3, "  <procparams> = Process parameters whose trail is required\n                 Following process parameters are available:\n                 cputimepc, memusage, shmem, ioops,thcount, and fdcount\n"
9310, 3, "  <sysparams>  = System  parameters whose trail is required\n                 Following system parameters are available:\n                 usagepc, cpuqlen, cpunumprocess, openfds, numrt,\n                 numofiosps, memfree,  numofthreads, and iowaitpc\n"
9311, 3, "  -c           = To request particular regions of interest\n  <regions>    = List of regions of interest\n                 Following regions are available\n                 red,green,yellow,and orange\n\n"
9312, 3, "*Requirements\n  -s and -e need to be specified together for range queries\n  The local System Monitor Service should be running to get trail.\n  The Cluster Logger Service should be running to get trail.\n\n*Defaults :\n  Region    : ALL\n  Time      : Last 30 min\n\n"
9313, 3, "*Example :\n  showtrail -n stadn59 -diskid hda1 qlen totalwaittime -s \"2007-11-12 23:05:00\" -e \"2007-11-12 23:15:00 \" -c \"red\" \"yellow\"\n"

// Showgaps usage (9341-9380)
9341, 3, "\nshowgaps verb usage\n====================\n  showgaps -n <node> [[-s <time> -e <time>]|  [-last <time1>]]\n           [-t <gapsize>] [-h]\n\n*Where\n"
9342, 3, ""
9343, 3, "  -n        = showgaps for given node\n  <node>    = node name for which gaps need to be shown\n  -s        = To specify time for the start of range queries\n  -e        = To specify time for the end of range queries\n"
9344, 3, "  <time>    = Absolute time to be specified within quotes in\n              \"YYYY-MM-DD HH24:MI:SS\" format, like \"2007-11-12 23:05:00\"\n  -last     = To specify time for last queries\n  <time1>   = Time in \"HH24:MI:SS\" format to be given with -last option,like \"00:45:00\"\n"
9345, 3, "  -t        = To specify minimum threshold for a gap\n  <gapsize> = Gap size in seconds \n\n"
9346, 3, "*Requirements\n  -s and -e need to be specified together for range queries\n  The local System Monitor Service should be running to get gaps.\n  The Cluster Logger Service should be running to get gaps.\n\n*Defaults :\n  Threshold: 3 (least size of gap)\n  Time: Last 30 min\n\n" 
9347, 3, "*Example:\n  showgaps -n stadn59 -s \"2007-11-12 23:05:00\" -e \"2007-11-12 23:15:00\" -t 10\n" 

// Showobject help (9381-9420)

9381, 3, "\nshowobjects verb usage\n======================\nshowobjects [[-allnodes]|[-n <node> [[-disk]|[-proc]|[-nic]]]][-time <time> [-b <band>]]\n\n*Where\n"
9382, 3, ""
9383, 3, "  -n           = Show objects for given node\n  <node>       = Node name for which objects need to be shown\n  -time        = Time at which objects are required\n  <time>       = Absolute time to be specified within quotes in\n                 \"YYYY-MM-DD HH24:MI:SS\" format, like \"2007-11-12 23:05:00\"\n  -disk"
9384, 3, "        = To request list of disks\n  -nic         = To request list of network interface cards\n  -proc        = To request list of processes\n  -allnodes    = Shows all the nodes which can be queried\n  -b           = For specifying maximum look up around <time> in seconds\n  <band>       = Size of band in seconds\n\n"
9385, 3, "*Requirements\n  Local System Monitor Service should be running to get objects.\n  Master loggerd should be running to get objects.\n\n*Defaults :\n  Time    : Current\n  Option  : -allnodes\n\n*Example :\n  showobjects -n stadn59 -disk -time \"2008-02-20 02:01:48\"\n "

// Cluster Health Monitor specific clusterware alert messages (9500 - 9599)

9500, 0, "The system monitor service aborted on host %s. Details at %s in %s."
// *Cause:  The system monitor service aborted due to an internal
//          error.
// *Action: If the problem persists, contact Oracle Support Services.

9501, 0, "The Cluster Logger Service aborted on host %s. Details at %s in %s."
// *Cause:  The Cluster Logger Service aborted due to an internal
//          error.
// *Action: If the problem persists, contact Oracle Support Services.

9502, 0, "The Cluster Health Monitor repository location %s is inaccessible. Details at %s in %s."
// *Cause: An error occurred while accessing the Cluster Health repository.
// *Action: Check that the Cluster Health Monitor repository location in question has the 
//          correct permissions. Determine whether this behavior is limited
//          to one node or whether it occurs across all of the nodes in 
//          the cluster. Use the 'oclumon manage -repos reploc <location>'
//          command to replace the Cluster Health Monitor repository location.

9503, 0, "The system monitor service on this host is unable to communicate with the Cluster Logger Service on host %s, and will log data to the local repository."
// *Cause:  Communication was lost with the Cluster Logger Service node.
// *Action: Verify all network connections between cluster nodes and repair
//          any problematic connections. If no network problems are found,
//          1. Run diagcollection.pl.
//          2. Contact Oracle Support Services.

9504, 0, "The Cluster Logger Service on host %s is dropping the Cluster Health Monitor node view. Details at %s in %s."
// *Cause: The Cluster Logger Service was unable to insert Cluster Health Monitor node view into  Cluster Health Monitor repository .
// *Action: Contact Oracle Support Services.

9505, 0, "The Cluster Health Monitor repository is deleted due to corruption and the Cluster Logger Service is disabled on %s. Details at %s in %s."
// *Cause: A critical error occurred while operating on Cluster Health Monitor repository.
// *Action: Contact Oracle Support Services.

9506, 0, "The system monitor service local repository is disabled on the host %s. Details at %s in %s."
// *Cause: An internal error occurred while writing to the system monitor service local repository.
// *Action: Contact Oracle Support Services.

9507, 0, "The maximum Cluster Health Monitor repository retention time is reached. Deleting the oldest Cluster Health Monitor node views in age order."
// *Cause: The maximum time for which the oldest Cluster Health Monitor node view will be 
//         available on Cluster Health Monitor repository was reached.
// *Action: If necessary, use 'oclumon manage -repos resize <size>' command to 
//          change the retention time.

9508, 0, "The Cluster Health Monitor repository retention time cannot be changed due to lack of disk space on node %s."
// *Cause: The Cluster Health Monitor retention time condition could not be
//       fulfilled because the Cluster Health Monitor repository ran out
//      of disk space at run time at the repository location.
// *Action:  Use the 'oclumon manage -repos reploc <location>' command to replace
//           the Cluster Health Monitor repository with a disk location that has at least 
//           1GB of available space per cluster node.

9509, 0, "The new Cluster Logger Service master is %s."
// *Cause:  A new Cluster Logger Service master node was elected.
// *Action: None.

9510, 0, "The new Cluster Logger Service replica is %s."
// *Cause:  A new Cluster Logger Service replica node was elected.
// *Action: None.

9520, 0, "The storage of Grid Infrastructure Management Repository is %u%% full. The storage location is '%s'."
// *Cause: The storage of Grid Infrastructure Management Repository was close to full. This storage can be a shared file system or an Oracle ASM disk group.
// *Action: Make sure there is sufficient free space in repository location.

// Daemon messages (9600 - 9618)

9600, 0, "Failed to initialize %s daemon"
// *Cause: An error occurred during initialization.
// *Action: Report this error to Oracle Support Services.

9601, 0, "Failed to allocate memory"
// *Cause: An error occurred while allocating memory.
// *Action: Report this error to Oracle Support Services.

//9602, 0, This message is free.
// *Cause:
// *Action:

9603, 0, "Failed to read configuration files"
// *Cause: An error encountered while retrieving information from configuration files.
// *Action: Report this error to Oracle Support Services.

9604, 0, "Failed to update configuration files"
// *Cause: An error encountered while updating information in configuration files.
// *Action: Report this error to Oracle Support Services.

//9605, 0, This message is free.
// *Cause:
// *Action:

//9606, 0, This message is free. 
// *Cause:
// *Action:

9607, 0, "Cannot spawn thread for %s"
// *Cause: An error encountered while spawning thread.
// *Action: Report this error to Oracle Support Services.

9608, 0, "ASM disk method failed"
// *Cause: An error encountered with ASM disks configuration.
// *Action: Report this error to Oracle Support Services.


9609, 0, "Encountered cssd failure. Reinitializing CSSD layer."
// *Cause: An error was encountered with CSSD layer while retrieving information.
// *Action: Report this error to Oracle Support Services.

9610, 0, "Encountered a fatal internal error. Daemon %s exiting." 
// *Cause: A fatal error occurred with CSSD layer.
// *Action: Report this error to Oracle Support Services.

9611, 0, "Mark %s disks encountered errors" 
// *Cause: An error occurred while accessing disk.
// *Action: Report this error to Oracle Support Services.

9612, 0, "Mark %s disks failed" 
// *Cause: A fatal error occurred while accessing disk.
// *Action: Report this error to Oracle Support Services.

9613, 0, "Internal error occurred" 
// *Cause: Internal error occurred.
// *Action: Report this error to Oracle Support Services.

//9614, 0, This message is free
// *Cause:
// *Action:

9615, 0, "Disk method Failure : %s" 
// *Cause: Internal error occurred.
// *Action: Report this error to Oracle Support Services.

9616, 0, "Daemon started : %s" 
// *Cause: A daemon process started successfully.
// *Action: None.

9617, 0, "Invalid message type encountered" 
// *Cause: An invalid or corrupted message was received. 
// *Action: Report this error to Oracle Support Services.

9618, 0,"Daemon stopped : %s" 
// *Cause: A daemon process stopped successfully.
// *Action: None

///////////////////////////////////////////////////////////////////////
/
// end of CHM/IPD related messages (9000-9999)
/
///////////////////////////////////////////////////////////////////////

10000, 0, "%s"
// *Documented: NO
// *Cause:
// *Action:

// Grid Naming Service
10001, 0, "%s"
// *Documented: NO
// *Cause:
// *Action:
/
////////////////////////////////////////////////////////////////////
/
// 10002-10050 - crsctl_net messages
/
////////////////////////////////////////////////////////////////////
10002, 1, "failed to allocate memory\n"
// *Cause: Memory allocation failed.
// *Action: Correct the system memory problem and retry.
/
10003, 3, "IP address %s could be reached from current node"
// *Document: NO
// *Cause:
// *Action:
/
10004, 1, "unable to reach %s address from local node"
// *Cause: An attempt to reach the IP address specified failed.
// *Action: Make sure that the specified IP address is a valid IP address and is 
//          assigned to an interface. Make sure that there are no firewalls 
//          between local node and node on which specified IP address is hosted.
/
10005, 1, "unable to determine local hostname"
// *Cause: The hostname could not be read.
// *Action: Check that the hostname for the local machine is valid. Look at the accompanying messages. If the problem persists, contact Oracle Support Services.
/
10006, 1, "APPVIP type needs a VIP name. Specify a VIP name using -vip commandline option"
// *Cause: VIP resource name was missing in the command line for APPVIP type.
// *Action: Specify a VIP name using -vip option.
/
10007, 3, "client ID : %s"
// *Document: NO
// *Cause:
// *Action:
/
10008, 1, "unable to generate client ID for VIP type %s, cluster name %s, VIP resource name %s"
// *Cause: An attempt to generate client ID for specified cluster name, VIP type and resource name failed. 
// *Action: Make sure that cluster name and VIP resource name do not exceed 252
//          characters. Make sure that VIP type is a valid VIP type. Refer to
//          'crsctl get clientid -help' for more information.
/
10009, 3, "DHCP server returned server: %s, loan address : %s/%s, lease time: %d"
// *Document: NO
// *Cause:
// *Action:
/
10010, 1, "unable to discover DHCP server in the network listening on port %d for client ID %s"
// *Cause: An attempt to discover DHCP server listening on port specified failed.
// *Action: Make sure that DHCP servers exist on the network and are listening on 
//          port specified. If they are listening on a different port specify then 
//          specify that port using the -port option. For more information refer 
//          to help for 'crsctl discover dhcp' command. 
/
10011, 1, "unable to request DHCP lease for client ID %s on port %d"
// *Cause: An attempt to request DHCP lease for the specified client ID on specified port failed.
// *Action: Make sure that there are DHCP servers with IP addresses available on the network. 
//          If other DHCP servers are available which are listening on a different port specify
//          an alternative port using the -port option. For more information refer to help for 'crsctl request dhcp' command.
/
10012, 3, "released DHCP server lease for client ID %s on port %d"
// *Document: NO
// *Cause:
// *Action:
/
10013, 1, "unable to release DHCP lease for client ID %s, on port %d"
// *Cause: An attempt to release DHCP lease for the specified client ID on specified port failed.
// *Action: Make sure that there are DHCP servers listening on port specified. If the DHCP server 
//          is listening on a different port specify an alternative port using -port option. For more
//          information refer to help for 'crsctl release dhcp' command.
/
/
10014, 1, "HOSTVIP type needs a node name. Specify a node name using -n option"
// *Cause: Node name was missing in the command line for HOSTVIP type.
// *Action: For HOSTVIP type node name needs to be specified via -n option.
/
10015, 1, "VIP type %s is invalid"
// *Cause: An invalid VIP type was specified for DHCP client ID generation.
// *Action: Make sure that VIP type is a valid VIP type. Refer to 
//          'crsctl get clientid -help' for more information.
/
10016, 1, "error obtaining local host DNS resolver configuration"
// *Cause: An attempt to obtain local host DNS configuration failed.
// *Action: Make sure that the user executing the command has sufficient permission
//          to read local system configuration.
/
10017, 1, "the %d name servers configured on this system exceeds the %d maximum allowed"
// *Cause: An attempt to obtain local host DNS configuration failed because more 
//         name servers were found then allowed on this operating system.
// *Action: Reduce the number of name servers configured to the maximum allowed.
/
10018, 3, "the following configuration was found on the system:"
// *Document: NO
// *Cause:
// *Action:
/
10019, 3, "There are %d domains in search order. They are:"
// *Document: NO
// *Cause:
// *Action:
/
10020, 3, "number of retry attempts for name lookup is: %d"
// *Document: NO
// *Cause:
// *Action:
/
10021, 3, "timeout for each name lookup is: %d\n"
// *Document: NO
// *Cause:
// *Action:
/
10022, 3, "There are %d name servers. They are:\n"
// *Document: NO
// *Cause:
// *Action:
/
10023, 1, "Domain name look up for name %s failed. Operating system error: %s"
// *Cause: An attempt to query DNS servers for name specified failed.
// *Action: Look at accompanying messages for more information on the failure.
/
10024, 3, "DNS server returned %s for name %s"
// *Document: NO
// *Cause:
// *Action:
/
10025, 3, "successfully created socket on port %d at address %s"
// *Document: NO
// *Cause:
// *Action:
/
10026, 3, "successfully created socket on port %d on local node"
// *Document: NO
// *Cause:
// *Action:
/
10027, 3, "port %d at address %s is in use by some other application"
// *Document: NO
// *Cause:
// *Action:
/
10028, 3, "port %d on local node is in use by some other application"
// *Document: NO
// *Cause:
// *Action:
/
10029, 3, "could not verify if port %d at address %s is in use"
// *Cause: An attempt to verify if port at address specified is in use failed.
// *Action: Make sure that the user has permission to create socket at port 
//          specified. For ports < 1024 user should be root. Also look at the
//          accompanying messages for more information.
/
10030, 3, "could not verify if port %d on local node is in use"
// *Cause: An attempt to verify if port specified on local node is in use failed.
// *Action: Make sure that the user has permission to create socket at port
//          specified. For ports < 1024 the user should be root. Also look at the
//          accompanying messages for more information.
/
10031, 3, "successfully stopped the DNS listening daemon running on port %d at address %s"
// *Document: NO
// *Cause:
// *Action:
/
10032, 3, "successfully stopped the DNS listening daemon running on port %d on local node"
// *Document: NO
// *Cause:
// *Action:
/
10033, 1, "could not stop the DNS listening daemon running on port %d at address %s"
// *Cause: An attempt to stop the DNS listening daemon running on port and address specified failed.
// *Action: Make sure that the user has permission to send packets at the port specified.
//          For ports < 1024 the user should be root. Also look at the accompanying 
//          messages for more information.
/
10034, 1, "could not stop the DNS listening daemon running on port %d on local node"
// *Cause: An attempt to stop the DNS listening daemon on local node running on port specified failed.
// *Action: Make sure that the user has permission to send packets at the port specified.
//          For ports < 1024 the user should be root. Also look at the accompanying 
//          messages for more information.
/
10035, 1, "invalid name server '%s' specified in command line"
// *Cause: An invalid IPv4 address was specified on the command line for -dnsserver option.
// *Action: Specify a valid IPv4 address on the command line.
/
10036, 1, "value for command line parameter '%s' is not an integer"
// *Cause:  An invalid value was specified for the specified command line parameter.
// *Action: Re-submit the request with an integer value.
/
10037, 3, "    -once               Flag indicating that DNS listener should exit after one DNS query packet is received\n    -v                  Verbose output"
// *Document: NO
// *Cause:
// *Action:
/
10038, 3, "invalid IP address '%s' specified"
// *Cause:  An invalid IP address was supplied on command line.
// *Action: Supply an IP address that conforms to IETF RFC-791.
/
10039, 3, "invalid subnet '%s' specified"
// *Cause:  An invalid subnet was supplied to crsctl.
// *Action: Supply a subnet address that conforms to IETF RFC-950.
/
10040, 3, "unable to get list of network interfaces"
// *Cause:  An attempt to get the list of network interfaces failed.
// *Action: Look at the accompanying messages for more information.
/
10041, 3, "subnet '%s' is not configured on the node"
// *Cause:  The subnet specified did not match subnet of any network interface 
// on this node.
// *Action: Specify a subnet that matches at least one network interface's subnet
// on this node.
/
10042, 3, "DNS daemon is listening on port %d at address %s"
// *Document: NO
// *Cause:
// *Action:
/
10043, 3, "DNS daemon is not listening on port %d at address %s"
// *Cause: An attempt to check if the DNS daemon is listening on port and address specified failed.
// *Action: Make sure that the address specified is reachable. Make sure that 
//          there is no firewall between the node on which this command was run
//          and the address specified. Also look at the accompanying
//          messages for more information.
/
///////////////////////////////////////////////////////////////////////////////
/
//   10051-10060 - CVU resource specific error messages
/
///////////////////////////////////////////////////////////////////////////////
10051, 3, "CVU found following errors with Clusterware setup : %s"
// *Cause: A resource-specific error was detected by the Clusterware
//   Verification Utility (CVU).  This message is accompanied by others
//   providing details of the error condition.
// *Action: Respond based on the accompanying messages.
/

//////////////////////////////////////////////////////////////
/
/   10100-10130: crswrapexece.pl specific messages
/
//////////////////////////////////////////////////////////////
10100, 0, "Execution of crswrapexece.pl script with arguments '%s' fails."
// *Cause: crswrapexece.pl script failed when executed with the specific
//         arguments.
// *Action: Check system log and crswrapexece.log for more details. Contact
//          Oracle Support Services.
/
10101, 0, "Internal Error"
// *Cause: Execution of crswrapexece.pl script failed due to missing argument.
// *Action: Contact Oracle Support Services.
/
10102, 0, "Failure to open environment file %s."
// *Cause: The crswrapexece.pl script failed to open the environment file,
//         which might be caused by hostname change or user edits. 
// *Action: Check for the existence and permission of the environment file.
/
10103, 0, "Found %s syntax errors in environment file %s."
// *Cause:  crswrapexece.pl found syntax errors in the provided environment
//          file.
// *Action: Check and fix syntax error in the indicated environment file.  If
//          the problem persists, contact Oracle Support Services. 
/

//////////////////////////////////////////////////////////////
/
/   10131-10160: ohasd init scripts specific messages
/
//////////////////////////////////////////////////////////////
10131, 0, "Failure to create named pipe %s. Details [%s]."
// *Cause: The specified named pipe could not be created.  Oracle High
//         Availability Service would not be able to restart if crashes.
// *Action: Check for the existence and permission of the parent directory,
//          where the named pipe was created.
/
10132, 0, "Oracle High Availability Service was restarted at least %s times within the last %s seconds. Stop auto-restarting Oracle High Availability Service."
// *Cause: Oracle High Availability Service was restarted too rapidly within a
//         short period of time.
// *Action: Check the Oracle High Availability Service log file to determine
//          the cause.  If the problem persists, contact Oracle Support
//          Services. 
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
/
/ 10250 - 10300: crsctl <action> wallet related messages
/
///////////////////////////////////////////////////////////////////////////////
10250, 0, "Database name is required to access database wallets. Use -name option to supply a database name."
// *Cause: The option -name was missing on the command line.
// *Action: For APPQOSDB wallet types -name is a mandatory parameter. Retry the command with -name option.
/
