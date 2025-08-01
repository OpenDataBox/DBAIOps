/* Copyright (c) 2001, 2017, Oracle and/or its affiliates. All rights reserved.*/
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
/    apfwkr     10/11/17 - Backport
/                          sbezawad_blr_backport_26581118_12.2.0.1.170718ocwru
/                          from st_has_12.2.0.1.0ocwpsu
/    sbezawad   08/27/17 - Backport sbezawad_bug-26581118 from main
/    csivanan   11/30/16 - XbranchMerge csivanan_fix_app_cluster from main
/    shullur    11/01/16 - Backport shullur_bug-24567625 from main
/    samjo      08/03/16 - Bug 24372551
/    shullur    09/12/16 - Bug 24567625
/    sbezawad   08/09/17 - Bug 26581118: Allow clustername to begin with
/                          numeric character
/    sbezawad   04/11/17 - Bug 24799186: Add msg 2129
/    csivanan   09/13/16 - bug/24423011
/    csivanan   09/13/16 - bug/24437619
/    bofwang    07/29/16 - Bug 24373659
/    jgrout     06/07/16 - Bug 23294655
/    agorla     05/24/16 - bug#23303856 - clscrs error
/    csivanan   05/13/16 - bug/23272108
/    ekucukog   04/26/16 - Added message 42007
/    dbagaria   04/20/16 - Added message 42003
/    mkallana   04/19/16 - 23000106 Add voting file majority messages for
/                          extended cluster
/    csivanan   04/14/16 - bug/22814969
/    xesquive   04/08/16 - Fix bug23044032 improve message 10048
/    tthathac   04/01/16 - Bug : 22540887
/    csivanan   03/31/16 - bug/23006855
/    agorla     03/31/16 - bug#23028237 - fix CRS-5046 to print params
/    bofwang    03/22/16 - Add modify site -s message
/    csivanan   03/18/16 - bug/22862929
/    yiwatan    03/15/16 - Fix CHM help message
/    tthathac   03/12/16 - Bug : 22826398
/    ajkundu    03/11/16 - Bug 22822769
/    sraos      03/10/16 - Bug22878899
/    csivanan   02/29/16 - bug/22819036
/    shiyer     02/23/16 - #34948
/    bofwang    02/19/16 - Bug 22765410
/    csivanan   02/18/16 - bug/20743211
/    dbagaria   02/16/16 - Bug 22734872: Cluster rename support
/    shiyer     02/11/16 - #33632/#33504
/    bofwang    02/09/16 - Bug 22550842
/    bofwang    01/13/16 - Bug 21946446
/    agorla     01/29/16 - error for start RF service of pdb
/    bofwang    01/13/16 - Bug 21946446
/    shiyer     01/29/16 - RG messages
/    dbagaria   01/24/16 - Bug 22366810: Added alert message CRS-1031
/    dbagaria   01/20/16 - Cluster rename support
/    nbraak     01/19/16 - bug 21900311
/    tthathac   01/15/16 - Bug : 22480005
/    agorla     01/15/16 - RF service messages
/    csivanan   01/15/16 - bug/21891352
/    nmallego   01/11/16 - bug-21959667
/    ajkundu    01/06/16 - Bug 22141284: CTSS to write mode changes to calog
/    jwarnes    12/24/15 - Bug 22293770: Improve message CRS-6770
/    shiyer     12/24/15 - #22311636
/    shiyer     12/22/15 - modify #4158 & #4159
/    tthathac   12/16/15 - Bug : 17735562
/    bofwang    12/15/15 - Bug 21482414
/    csivanan   12/10/15 - bug/22303927
/    tankumar   12/07/15 - Adding 9128, 9129 (Bug-22178565)
/    csivanan   12/01/15 - bug/22081085
/    bofwang    12/01/15 - Bug 22148628
/    nbraak     11/20/15 - bug 21565301
/    bofwang    11/17/15 - Storage Split
/    shiyer     11/12/15 - #22186236
/    sbezawad   11/10/15 - Bug 21919798: Adding msg for crsctl query cluster
/                          class command
/   jwarnes     10/29/15 = LRG 18693967: Add new message to test clsecho's
/                          call to clsd_malertprintftLSF
/   nkorehis    10/19/15 - DI bug-21107618
/   bofwang     10/09/15 - Bug 21847483
/   jwarnes     09/30/15 - Bug 21873441 - remove messages related to crsctl 
/                          get/set/unset log file size
/   jwarnes     09/29/15 - Bug 21870399: remove references to 'trace' for
/                          crsctl set/get commands. crsctl set/get trace is
/                          no longer supoorted
/   jwarnes     09/20/15 - Bug 19491598: add new messages for regression
/                          testing
/   sbezawad    09/07/15 - Bug 21275228: Add msg for crsctl command to get last
/                          active timestamp
/   lmortime    08/31/15 - Bug 21663151 - Fix clscal timestamp format
/   yiwatan     08/28/15 - Bug 21696068 - Add -format to oclumon help message.
/   yiwatan     08/27/15 - Edit oclumon message on loglvl
/   bmanry      08/25/15 - bug 21494960 - change 8503 format item
/   hmbui       08/20/15 - Bug 21647456 - Inconsistent crsctl help message.
/   kiraj       08/12/15 - Fix bug : 20963954
/   jwarnes     08/12/15 - bug 21616390: disable crsctl set trace 
/   shiyer      08/12/15 - #21430565
/   shiyer      07/31/15 - add 33805
/   hmbui       07/27/15 - Bug 21503928 - Adding space between -w and <filter>
/   takiba      06/15/15 - bug21195237: correct misleading messages
/   shiyer      07/23/15 - crsctl export messages
/   bofwang     07/16/15 - Extended Cluster 2
/   rakebhat    07/15/15 - fix bug 21362191
/   sraos       07/05/15 - Bug20056117
/   jwarnes     07/02/15 - bug 21289799 - disable crsctl set css logfilesize
/                          and crsctl get css logfilesize
/   nkorehis    07/01/15 - bug-21295235: remove "analyze" from usage of oclumon
/   shiyer      06/25/15 - #21302002:2969,33969
/   bofwang     06/17/15 - Extended Cluster
/   takiba      06/15/15 - bug21195237: correct misleading messages
/   shiyer      06/25/15 - #21302002:2969,33969
/   samjo       06/15/15 - Add site related error messages
/   takiba      06/15/15 - bug21195237: correct misleading messages
/   nmallego    06/16/15 - bug20991879 - change CRS-1603 msg
/   samjo       06/15/15 - Add site related error messages
/   shiyer      06/12/15 - crsctl messages
/   dbagaria    06/11/15 - Bug 21210646: Added messages for calog ret time
/   tthathac    06/11/15 - Bug 20742586
/   ksrangal    06/09/15 - Bug 20617461 - Added #6573
/   shiyer      06/03/15 - Bug #21133210 : RG messages
/   csivanan    05/27/15 - bug/21136596
/   bofwang     05/26/15 - Add ACL extension
/   nkorehis    05/26/15 - DI bug-20568884
/   dbagaria    05/26/15 - Modified message 40016
/   csivanan    05/22/15 - bug/21086914
/   shiyer      05/22/15 - #21133029
/   shiyer      05/21/15 - #21087569
/   jwarnes     05/14/15 - Bug 20925634: typo in CRS-0007
/   kiraj       05/13/15 - Fix bug : 21070499
/   shiyer      05/13/15 - 20913669
/   hmbui       05/07/15 - Generate and propagate CALOG activity for cluster
/                          starting/stopping
/   jrevuelt    05/06/15 - Bug 20822591
/   arpshukl    05/06/15 - Split CHM messages
/   csivanan    05/05/15 - bug/21036821
/   tthathac    05/01/15 - Bug : 20995151
/   yiwatan     04/22/15 - Add msg 9127
/   shiyer      04/21/15 - #20912504
/   ggomezb     04/20/15 - Modified message 2409
/   shiyer      04/18/15 - #20841179
/   shiyer      04/15/15 - #20803610
/   kiraj       04/14/15 - Fix bug : 20083913
/   bmanry      04/13/15 - Bug 19935056 - add alert message 716
/   shiyer      04/13/15 - #20841483
/   dbagaria    04/10/15 - BUG 20862812: Added message 2129, 2130
/   hmbui       04/08/15 - Fixed typos and made placeholders conform to new
/                          format.
/   dbagaria    04/06/15 - Added message 40016
/   agusev      03/31/15 - fix for 19403970
/   shiyer      03/30/15 - RG membership messages
/   yiwatan     03/30/15 - Bug 9842364 - change message 9201 and 9241
/   bofwang     03/26/15 - Bug 18489390
/   shiyer      03/26/15 - 20717835
/   csivanan    03/18/15 - add -explain
/   tthathac    03/18/15 - Bug : 20723784
/   shiyer      03/17/15 - 20713178:use positional params
/   lmortime    03/16/15 - Bug 20675487 - Fix timestamp/interval format errors
/   dbagaria    03/16/15 - Added messages 6764
/   shiyer      03/09/15 - RG What-if messages
/   hmbui       03/08/15 - Bug 20440856 - Obtain user name and group for
/                          security attribs before setting the cluster type.
/   dbagaria    03/02/15 - Modified message 6755
/   jolascua    02/27/15 - Bug 19642801: adding a comment about communication
/                          to sysmond.
/   jrevuelt    02/25/15 - Bug 17653408: detailed message for invalid node
/   csivanan    02/23/15 - bug/20526941
/   hmbui       02/20/15 - Implemented cluster starting/stopping with filter.
/   csivanan    02/16/15 - fix policy -whyif
/   xesquive    02/11/15 - Fix bug20476447 split message 4815, append to 4829
/   dbagaria    02/10/15 - BUG 19708639: Added message 1029, 1030
/   sraos       02/02/15 - Bug12345215
/   nmallego    01/30/15 - Bug-19382066 - handle priority failure status
/   nmallego    01/23/15 - Bug20408163 - Message for CSSD base priority
/   hmbui       01/14/15 - Bug fix - 19676090.
/   nbraak      01/12/15 - online relocate
/   jwarnes     01/07/15 - Bug 20319572: Added  messages CRS-6775/6776 in 
/                          support of command:
/                          crsctl get/set tracefileopts init
/   shiyer      01/06/15 - RG dependency messages
/   pckamath    12/22/14 - Bug14236777
/   shiyer      12/17/14 - More RG messages
/   csivanan    12/15/14 - whyif - phase 3
/   shiyer      12/09/14 - More Resource Group messages
/   hmbui       11/19/14 - Implemented Application Load Awareness.
/   ysharoni    11/16/14 - bug 19829992 start cssd service msg
/   bmanry      11/13/14 - Bug 20026879 - tweak message 8505
/   xesquive    11/11/14 - include querytype in dns
/   tthathac    11/06/14 - Bug : 19708451
/   shiyer      11/03/14 - More Resource Group messages
/   rakebhat    10/29/14 - fix bug 19778281
/   dbagaria    10/27/14 - Added messages for "crsctl get calog" and
/                          "crsctl set calog"
/   hmbui       10/22/14 - Bug 19783690 - Allowing env override in resource
/                          modifications.
/   sbezawad    10/20/14 - Bug 16195774: Modify alert during OCR auto repair
/   tthathac    10/14/14 - Adding message number 2935
/   tthathac    10/01/14 - Bug 16675963: add messages for  new command:
/                           crsctl set tracefileopts <daemon> 
/                            -filesize <int> -numsegments <int> 
/   hmbui       09/29/14 - Bug 19624640 - Added Cluster Type get and set
/                          commands.
/   shiyer      09/25/14 - More ResourceGroup messages
/   minzhu      09/17/14 - new message for "HAIP"
/   dbagaria    09/14/14 - Added messages for "crsctl query calog"
/   atellaku    08/25/14 - Bug 18893463 - Cannot access GPnP wallets
/   shiyer      08/14/14 - More ResourceGroup messages
/   csivanan    07/18/14 - proj/47163
/   csivanan    07/18/14 - proj/47163
/   rwessman    07/11/14 - Bug 19164135 - added 10104 and 10105.
/   hmbui       06/29/14 - Bug fix - 18781949.
/   shiyer      05/28/14 - ResourceGroup messages
/   hmbui       05/19/14 - Bug 19388232 - Added option to disable CSS auto
/                          restart.
/   tthathac    05/15/14 - Add node weight messages
/   pckamath    05/05/14 - Bug18260170 -Add 4646 mesg when non existant VF
/                          replace is done
/   samjo       04/22/14 - Bug 18639465. Improve ACTION for CRS-1119
/   hmbui       04/18/14 - Bug 18007540 - Do not restart CRS if CSS crashes due
/                          to an interconnect problem.
/   pckamath    03/17/14 - Remove changes for 4905 message
/   jolascua    03/11/14 - Bug:17201508 message for retention space
/   pckamath    03/02/14 - Bug18321282
/   bmanry      02/17/14 - Bug 17663831 - misspelling in #4270
/   tthathac    02/10/14 - Bug : 18221290
/   sltam       02/05/14 - Bug 9892886: Add 5033 to 5036
/   hmbui       02/03/14 - Bug 18085593 - Implemented handling for start/stop
/                          dependencies on server category.
/   jolascua    01/31/14 - Bug 18126999: delete -csvlog option
/   minzhu      01/15/14 - 16240326, HAIP global set
/   hmbui       01/15/14 - Bug fixes - 18075044 and 18080122
/   pckamath    01/14/14 - Bug17531342 -Remove manual from CRS-1625 message
/   tthathac    01/13/14 - Bug 18053196
/   hmbui       12/30/13 - Bug fix - 14243661, implementing the displays of
/                          specific attributes and user-defined attributes.
/   minykim     12/26/13 - add 5031 and 5032
/   dbagaria    12/05/13 - BUG 17908553: Added message 1028
/   csivanan    11/27/13 - bug/17866576
/   csivanan    11/25/13 - bug/17778536
/   agusev      11/21/13 - fix for 16020794
/   mpradeep    11/19/13 - XbranchMerge mpradeep_bug-17776099 from main
/   nkorehis    11/12/13 - bug-16959589: more precise msg for crsctl replace
/                          discoverystring
/   jrevuelt    11/04/13 - Bug 14736007 - Fixing oclumon debug options syntax.
/   hmbui       11/04/13 - Bug fix - 17635513
/   tthathac    11/04/13 - Bug : 14137828
/   samjo       10/30/13 - Bug 17658111. Removing unsupported options from
/                          example
/   hmbui       10/23/13 - Bug fix - 17600410
/   vsamudra    10/21/13 - Add CHM messages for 12.1.0.2
/   samjo       10/17/13 - Bug 17623039. Improve message if database or local
/                          inst is not active
/   lmortime    10/16/13 - Adding VmAgent messages
/   papatel     10/10/13 - Bug 17583101 - CRS-4666
/   tthathac    10/07/13 - Bug : 17556818
/   csivanan    10/03/13 - bug/16275858
/   csivanan    10/03/13 - bug/16542825
/   samjo       09/20/13 - Bug 17338168. Remove '-d' from usage in 'oclumon
/                          calibrate'
/   pckamath    09/15/13 - Bug14188657
/   arpshukl    08/26/13 - Add CSV log help messages
/   tthathac    09/07/13 - Bug : 16853313
/   tthathac    09/01/13 - Bug : 17385854
/   hmbui       08/29/13 - Bug fix - 14707086 - Timeout status for Custom
/                          Actions.
/   pckamath    08/28/13 - Bug16206997
/   spavan      08/20/13 - fix bug16922949 - add messages for invalid
/                          characters
/   csivanan    08/20/13 - bug/17155827
/   csivanan    08/20/13 - bug/16735013
/   csivanan    08/20/13 - bug/16906396
/   nbraak      08/19/13 - reserving message for ranked startup
/   arpshukl    08/19/13 - Fix for bug 14213699
/   samjo       08/15/13 - Add 9089
/   csivanan    08/13/13 - bug/15942668
/   shiyer      08/07/13 - update #4933
/   csivanan    08/02/13 - bug/14825612
/   csivanan    08/01/13 - bug/14825476
/   csivanan    08/01/13 - bug/14549682
/   samjo       08/01/13 - Add server pool and model option for 'oclumon
/                          calibrate'
/   csivanan    07/22/13 - filter support for delete
/   minykim     07/17/13 - fix bug#17028080 - add 5030
/   hmbui       07/11/13 - Dependency Modifications Syntax - Bug 17006555
/   tthathac    07/03/13 - Bug : 17006539
/   samjo       07/02/13 - Bug 17028127. Add message for length of node name
/   mchimang    06/20/13 - b16865282: client cluster messages
/   mchimang    06/14/13 - 14690942:add new error messages for client cluster
/   arpshukl    06/07/13 - Add -i option to oclumon dumpnodeview
/   pckamath    06/06/13 - Bug16846090
/   hmbui       06/03/13 - Bug fix: 16675918
/   minzhu      05/29/13 - XbranchMerge minzhu_bug-16443575 from
/                          st_has_12.1.0.1
/   tthathac    05/22/13 - Bug : 14624244
/   tthathac    05/02/13 - Bug : 16602987
/   nbraak      04/29/13 - bug 16558193
/   tthathac    04/16/13 - Fix for bug 16617936
/   jwarnes     04/10/13 - bug 16631475: Add message CRS-0036
/   hmbui       03/27/13 - bug/16508450: Message 0714 -  Removing copyright
/                          notice, adding cause/action notes, and changing
/                          message type from 1 (error) to 3 (info).
/   csivanan    03/19/13 - bug/16221316
/   sejlim      03/18/13 - Message # 2828 is an error
/   csivanan    03/18/13 - bug/16319673
/   csivanan    03/18/13 - bug/16371690
/   csivanan    03/12/13 - bug/16273849
/   jwarnes     03/05/13 - bug 14525998
/   jwarnes     03/06/13 - bug 16448379: modify text for alert log message
/                          CRS-0003
/   csivanan    03/05/13 - bug/16264775
/   csivanan    03/05/13 - bug/16221316
/   csivanan    03/05/13 - bug/16206690
/   csivanan    02/25/13 - bug/16188227
/   hkanchar    02/14/13 - Message # 5027 is an error
/   nbraak      02/12/13 - bug 15987361
/   csivanan    02/11/13 - bug/16181395
/   jwarnes     02/11/13 - bug/13936066
/   samjo       01/09/13 - Add usage for 'oclumon calibrate'
/   shiyer      01/16/13 - #16134091
/   csivanan    01/07/13 - bug/15962849
/   csivanan    01/07/13 - bug/15956692
/   csivanan    01/07/13 - bug/15926460
/   csivanan    01/07/13 - bug/14729679
/   csivanan    01/04/13 - bug/14725920
/   csivanan    11/06/12 - bug/14735589
/   csivanan    11/05/12 - bug/14829782
/   minzhu      04/05/13 - 16443575, INTUITIVE ERROR MESSAGE
/   csivanan    09/25/12 - bug/14339536
/   csivanan    09/18/12 - bug/14590078
/   csivanan    09/13/12 - bug/14624956
/   csivanan    09/13/12 - bug/14591473
/   csivanan    09/12/12 - bug/14609331
/   csivanan    09/11/12 - bug/14585651
/   nbraak      09/11/12 - bug 14551834
/   diguma      09/04/12 - unset bc parameters
/   csivanan    09/04/12 - bug/14582914
/   csivanan    08/31/12 - bug/14572452
/   csivanan    08/31/12 - bug/14572494
/   shiyer      08/29/12 - Add 4409
/   diguma      08/31/12 - add \n in msg 1671
/   shiyer      08/29/12 - Add 4409
/   csivanan    08/30/12 - bug/13696326
/   csivanan    08/29/12 - bug/14551895
/   sbezawad    08/28/12 - Add alert 1027
/   vsamudra    08/23/12 - 12c new naming convention for chm
/   samjo       08/10/12 - Bug 14480614. Patch level for SIHA
/   shiyer      08/16/12 - #14253107
/   samjo       08/20/12 - Bug 14458787. Add 1159 and 1142.
/   shiyer      08/07/12 - #14216639
/   csivanan    08/02/12 - bug/14115152
/   wlohwass    07/30/12 - Bug 14386700. Fix lgwr incomplete ckpt causal chain
/   csivanan    07/23/12 - bug/14202698
/   samjo       07/16/12 - Change details for Top Process Memory Usage
/   anutripa    07/13/12 - Add message for retention failure for mdb
/   csivanan    07/11/12 - bug/14284847,14165376
/   mkallana    07/09/12 - change 4663
/   mkallana    07/04/12 - modify 4663
/   wegu        07/02/12 - Change %u to %d for System CPU Usage details. Bug
/                          14252279
/   samjo       06/25/12 - Move CHA messages
/   agusev      06/27/12 - added create ps
/   vsamudra    06/25/12 - fix bug 14223504
/   vsamudra    06/25/12 - Add messages for oclumon for wallet and listener
/                          failures
/   samjo       06/14/12 - Bug 7606868. Fix message 1182
/   anutripa    06/13/12 - Remove REPLICA from oclumon manage help
/   csivanan    05/29/12 - bug/14098958
/   csivanan    05/22/12 - bug/8770619
/   jleys       05/22/12 - errors_us requirements
/   jleys       05/21/12 - Add a period to the end of an Action statement
/   jleys       05/15/12 - Add msg for failure of CSS caused by other
/                          components
/   anutripa    05/15/12 - Corrections in help for oclumon
/   mrmehta     05/07/12 - Adding autostart related messages
/   priagraw    05/10/12 - alert when rim cannot connect
/   wlohwass    01/30/12 - Added CHMDB Messages.
/   samjo       01/24/12 - CHA: Adding corrective action for OS, CW, ASM model
/   vsamudra    05/03/12 - Add some CHM alert messages related to mgmtdb
/   arpshukl    05/03/12 - Add message number 9080
/   wegu        05/02/12 - Add message for CHMOS repository storage (filesystem
/                          or disk group) close to full. Bug 10418841
/   nbraak      05/01/12 - adding SERVER_LABEL attribute messages
/   anutripa    05/01/12 - Update oclumon help messages
/   gdbhat      04/19/12 - Bug 13970079
/   nbraak      04/16/12 - clarifying 2873
/   samjo       03/28/12 - Bug 13836319. Add support for start rollingupgrade
/   mrmehta     03/29/12 - Bug 13789711
/   mrmehta     03/26/12 - bug 13838972 and 13680982
/   samjo       03/26/12 - Add mesg for no component, no sev
/   shiyer      03/19/12 - #13797116:remove -shutdown_cluster_now for now
/   samjo       03/21/12 - Change %d to %u for msg 1169
/   shiyer      03/19/12 - #13797116:remove -shutdown_cluster_now for now
/   nbraak      03/16/12 - fixing typo in 2912
/   gdbhat      03/13/12 - Bug 13573192
/   bmanry      03/05/12 - Add CRS-8505 for non-signal fatal errors; tweak 8501
/   arpshukl    03/05/12 - update #9508
/   spavan      02/29/12 - fix bug12808031
/   sltam       02/28/12 - Bug 13626519
/   nbraak      02/28/12 - adding message to abort category modification
/                          lacking force if required
/   nbraak      02/27/12 - Bug 13589034
/   ggomezb     02/23/12 - Bug 13775664
/   mrmehta     02/15/12 - Bug 12990525
/   hkanchar    02/15/12 - Add error message 5027 for racagents
/   mrmehta     02/08/12 - Bug 13367930
/   samjo       01/26/12 - Project 33056. CRSCTL commands for rolling patch
/   mrmehta     02/10/12 - BUG 13430040
/   csivanan    02/09/12 - bug/13548546
/   anjiwaji    02/09/12 - Add message 5023-5026.
/   mrmehta     02/08/12 - Bug 13367930
/   ggomezb     02/06/12 - Update #4957
/   gdbhat      01/31/12 - Add Generic appagent msg
/   shiyer      01/31/12 - Add msgs for crsctl resource dependency view
/   csivanan    01/26/12 - bug/13559437
/   lmortime    01/19/12 - crsctl add credentials help
/   ksrangal    01/14/12 - Removed alert 1023
/   samjo       01/13/12 - Bug 11730613. Check if AV has progressed
/   samjo       01/11/12 - Project 33056. Rolling patch
/   yafan       01/12/12 - bug 13408765: add CHA error message 9077
/   samjo       01/11/12 - Project 33056. Rolling patch
/   cwang       01/10/12 - bug 13114873 add 5022
/   mrmehta     01/04/12 - Changing the syntax of 'crsctl eval add res'
/   samjo       12/15/11 - Fix oclumon analyze help
/   shiyer      12/27/11 - Update #5809
/   wegu        12/08/11 - Add messages for CHA problem details
/   bmanry      12/08/11 - add CRS-8504 (process exit)
/   nbraak      12/08/11 - bug 13409017
/   agorla      12/07/11 - CVUDB support
/   csivanan    12/02/11 - bug/13052369
/   nbraak      12/02/11 - bug 13459525
/   shiyer      11/30/11 - #13405084:new messages
/   ysharoni    11/24/11 - Bug 13342671 add gns advert fail msg 2337,2339
/   mrmehta     11/15/11 - Bug 13349350
/   mrmehta     11/15/11 - Bug 13362292
/   shiyer      11/14/11 - #12945978:update 4119
/   gdbhat      11/11/11 - Bug 13349282
/   nbraak      11/08/11 - bug 12737296
/   akhaladk    11/08/11 - New msgs for credential permissions
/   samjo       11/08/11 - Add CHA message 9076
/   samjo       11/07/11 - Reserve range for CHA model messages
/   mrmehta     11/03/11 - Bug 13331629
/   samjo       09/20/11 - Add analyze error messages
/   bmanry      10/14/11 - update 85xx messages pre review comments
/   nbraak      10/03/11 - alert log template
/   samjo       09/01/11 - Add message for no problems found
/   mrmehta     09/20/11 - Bug 12856152
/   shiyer      09/12/11 - add more 'crsctl css' command msgs
/   samjo       09/01/11 - Add message for no problems found
/   jchandar    09/13/11 - add MGMTDB wallet type for crsctl
/   shiyer      09/12/11 - add more 'crsctl css' command msgs
/   lmortime    09/08/11 - Adding credentials commands
/   samjo       09/01/11 - Add message for no problems found
/   shiyer      09/02/11 - add 5835:agent versioning
/   minykim     09/01/11 - Add 5021
/   csivanan    08/30/11 - modifying 2846
/   samjo       08/30/11 - XbranchMerge samjo_bug-12729496 from st_has_11.2.0
/   vmanivel    08/28/11 - Bug 12758971
/   vmanivel    08/28/11 - Bug 12910641
/   gdbhat      08/26/11 - Add msg 2900-2903
/   shiyer      08/23/11 - update #4946
/   spavan      08/15/11 - add subnet for dhcp commands
/   nbraak      07/23/11 - suppress ohasd driver restart
/   shiyer      07/20/11 - Messages for BC/crsctl
/   bmanry      07/21/11 - New process infrastructure messages
/   sbezawad    07/18/11 - Add new alert 1023
/   samjo       04/07/11 - Project 33087. Add msg for OCLUMON output
/   shiyer      07/20/11 - Messages for BC/crsctl
/   ksrangal    07/14/11 - Modified message 1004 and added new message 1023.
/   shiyer      07/12/11 - #12749094:alert msg for resource disable
/   vsamudra    07/07/11 - Modify error message 9031
/   csivanan    07/05/11 - resource restart op
/   vmanivel    06/20/11 - Blocking Stack Start
/   sbezawad    06/01/11 - Modify msg 1022, 1121
/   vmanivel    05/24/11 - WhatIf for Cluster Admins
/   csivanan    05/02/11 - Server pool:resource start/stop
/   akhaladk    04/28/11 - Add more credential messages
/   vsamudra    04/18/11 - CHM alert messages for clusterware log(Bug 12370546)
/   sbezawad    04/12/11 - Add msg for force upgrade
/   vmanivel    04/11/11 - WhatIf activate policy
/   anutripa    04/11/11 - Change oclumon dumpnodeview usage
/   lmortime    04/07/11 - Adding crsctl credential messages
/   nbraak      04/06/11 - action entrypoint
/   jchandar    03/31/11 - add priority and nice value in process
/   jgobbur     03/30/11 - to fix bug#11937312
/   csivanan    03/15/11 - bug/10638125
/   samjo       03/14/11 - Adding CHA specific messages 3501-3999
/   papatel     03/09/11 - Bug 11848398
/   arpshukl    03/06/11 - Correct bdb location change message for CRF
/   vmanivel    03/03/11 - WhatIf for add/modify/fail
/   wegu        03/02/11 - Bug-10413273. Add metric explanation and units for
/                          oclumon dumpnodeview -h 
/   anutripa    03/01/11 - Fix message 9015 for oclumon
/   csivanan    02/17/11 - bug/10239164
/   dtrejoh     02/16/11 - Bug 9754300. Add msg for clusterized commands.
/   cwang       02/14/11 - fix 5019
/   rbvarshn    02/09/11 - update start testdns msg
/   vmanivel    02/07/11 - WhatIf for Servers
/   vsamudra    01/26/11 - Add error message for dumpnodeview -allnodes -n
/                          combined usage
/   jgrout      01/18/11 - Fix bugs 6849323, 8313948 and 10039715
/   priagraw    01/14/11 - add alert 1662, 1663
/   nbraak      01/12/11 - adding cardinality hotmod failure message
/   ysharoni    01/10/11 - messages for initial gpnp  rim/hub implementation
/   ssaggar     01/10/11 - Bug: 9750124
/   spavan      01/06/11 - fix bug10081734
/   sbezawad    12/21/10 - Add alert if OCR backup in ASM DG is not accessible
/   vmanivel    12/21/10 - WhatIf for ServerPools
/   spavan      12/16/10 - messages for osuser wallets
/   sltam       12/08/10 - Add 5020
/   gdbhat      12/01/10 - Policy mgmt msgs
/   samjo       11/29/10 - Add 1119 mesg to reject AV change
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
/   sukumar     07/06/10 - Change BDB to repos and add more CHM messages.
/   anutripa    06/24/10 - Change BDB to repos
/   cwang       06/23/10 - add 5019
/   lmortime    06/17/10 - clsce messages
/   anutripa    06/16/10 - Remove -m option from oclumon commands
/   anutripa    06/14/10 - CHM/IPD: Add CRFM component to debug help for
/                          oclumon
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
/   1101-1200: Oracle Clusterware upgrade and patch specific messages
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
/   2500-3500: CRS Policy Engine error messages
/   3501-3999: Cluster Health Analysis (CHA) specific messages
/   4000-4999: CRSCTL specific messages
/   5000-5099: HAA specific messages
/   5100-5150: CLSCRS-API status messages
/   5151-5199: CLSCRS-API return code messages
/   5200-5500: HAA specific messages (Continued after 5099)
/   5501-5600: Reporter specific messages
/   5601-5700: MDNS specific messages
/   5701-5800: Placement Policy specific messages
/   5801-5999: AGFW specific messages
/   6001-6999: CRSD specific messages
/   7000-7999: GPNP messages (see also 2301-2400)
/   8000-8199: Last Gasp messages
/   8200-8499: Eval messages (continued)
/   8500-8999: Process infrastructure (CLSB) messages
/   9000-9999: CHM/IPD specific message
/   10000-10001: Other component specific messages
/   10100-10130: crswrapexece.pl specific messages
/   10201-10300: CLSCE specific messages
/   10301-10400: CCL specific messages
/   10401-10500: Credentials specific messages
/   10501-10700: CLSU specific messages
/   10701-11000: CLSM specific messages
/   20000-39999: CHA model messages
/   40000-41000: CLSCAL specific messages
/   41001-42000: CRSCTL specific messages
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
// *Cause: The messsage for the given message id is not found in any language.
// *Action: Make sure the product is setup correctly on the system.
/
002, 1, "%s:Internal list corruption. trace file: \"%s\""
// *Cause: An internal error was detected during trace file flush processing.
// *Action: Contact Oracle Support Services.
/
003,  1, "An error occurred while attempting to open file \"%s\". Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to open the specified
//         file.
// *Action: Examine the additional diagnostics, if available, and attempt
//          to correct any file system environmental problems if indicated.
//          Otherwise, contact Oracle Support Services.
/
004,  1, "logging terminated for the process. log file: \"%s\""
// *Cause: One or more file system errors were encountered which caused
//         logging to be terminated for this process.
// *Action: Examine preceding Alert log messages for details on the error or
//          errors that occurred. Restart the process to reenable logging.
/
005,  1, "file \"%s\" deleted after close failure"
// *Cause: This message is informational. An attempt to close the specified
//         file failed. The contents of the file after a close
//         error are undefined. The file has been successfully deleted.
//         Log data are lost.
// *Action: None. 
/
006,  3, "file rotation processing continues for file: \"%s\""
// *Cause: This message is informational and indicates only that a preceding
//         error was not sufficiently severe to terminate file rotation which
//         might otherwise be the case.
// *Action: None.
/
007,  1, "failed to open new log file \"%s\""
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
009,  1, "file \"%s\" reopened"
// *Cause: An error was encountered during rotation processing so that
//         file rotation could not proceed. The original file, which
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
011,  1, "An error occurred while attempting to close file \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered when attempting to close the specified
//         file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
012,  1, "An error occurred while attempting to rename file \"%s\" to \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered when attempting to rename the source
//         file to the destination file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
013,  1, "An error occurred while attempting to check for the existence of file \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to determine if the
//         specified file existed.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
014,  1, "An error occurred while attempting to delete file \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to delete the specified
//         file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
015,  1, "An error occurred while attempting to flush file \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while an attempting to flush the
//         specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
016,  1, "An error occurred while attempting to free the file name object for file \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to free the file name
//         object for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
017,  1, "An error occurred while attempting to create a file name object for file \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to create a file name
//         object for the specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct
//          any file system environmental problems if indicated. Otherwise,
//          contact Oracle Support Services.
/
018,  1, "An error occurred while attempting to reopen file \"%s\" during file rotation. Additional diagnostics: %s"
// *Cause: An error was encountered while attempting to reopen the 
//         specified file.
// *Action: Examine the additional diagnostics, if any, and attempt to correct 
//          any file system environmental problems if indicated. Otherwise, 
//          contact Oracle Support Services.
/
019,  1, "Log file rotation terminated. log file: \"%s\""
// *Cause: One or more file system errors were encountered which caused log
//         file rotation to be terminated for the process. Although log file
//         rotation has been terminated, logging continues.
// *Action:  Review Alert log messages that precede this alert log message
//           that identify the file system error or errors encountered. If the
//           additional diagnostic data in a preceding alert log message
//           indicate a file system environmental problem, attempt
//           to correct it. Otherwise contact Oracle Support Services.
//
//           To reenable file rotation the process must be restarted.
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
036,  1, "An error occurred while attempting to open file \"%s\". Additional diagnostics: Path: %s. Filename: %s. rc: %d"
// *Cause: An error was encountered while attempting to open the specified 
//         file.
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
039,  1, "An error occurred while attempting to open trace file \"%s\". Additional diagnostics: Path: %s. Filename: %s. rc: %d"
// *Cause: An error was encountered while attempting to open the specified 
//         file. Tracing was disabled for the process.
// *Action: Review the preceding alert log messages and attempt to
//          resolve any file system environmental problems indicated.
//          Otherwise, contact Oracle Support Services.
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
/ Messages 42 - 46 for regression testing
/
/ WPTG: Do not translate the following message. It is used only for testing.
042, 1, "alert log: lsfpd test1: %(4)s\n %(3)s\n %(2)s\n %(1)s"
// *Document: NO
/ WPTG: Do not translate the following message. It is used only for testing.
043, 1, "alert log: lsfpd test2: %s %s %s %s"
// *Document: NO
/ WPTG: Do not translate the following message. It is used only for testing.
044, 1, "alert log: lsfpd test3: %s %s %s %s %s"
// *Document: NO
/ WPTG: Do not translate the following message. It is used only for testing.
045, 1, "alert log: lsfpd test4: %s %s %s %s %s %s"
// *Document: NO
/ WPTG: Do not translate the following message. It is used only for testing.
046, 1, "Test call to clsd_malertprintftLSF from clsecho: %s %s %s %s"
// *Document: NO
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
186,    1, "There is a switch conflict in the type definition files used by crs_profile\nwhen creating your '%s' type resource. Make sure each attribute\nswitch is defined only once.\n"
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
// *Cause: Based on the placement policy for the resource, there was no 
// available host to which the resourse could failover or start.
// *Action: Check the target host for the resource and restart the resource
//          using the 'crsctl start resource' command.    

/
/ added for 10i
224,    2, "Warning: failed to redirect I/O"
225,    1, "Resource name not specified"
226,    2, "Warning: memory allocation"
227,    1, "Invalid resource name"
228,    1, "Invalid host"
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
239,  1,  " Invalid command"
240,  1,  " Piped channel output error"
241,  1,  " Invalid directory path."
242,  1,  " ACL information is not available"
243,  1,  " default setting unavailable"
244,  1,  " registration allow/deny information is not available"
245,  1,  " User doesn't have enough privilege to perform the operation"
246,  1,  " User id is invalid"
247,  1,  " User name or group name is invalid"

248,  1,  " ACL operation failed"
249,  1,  " Authentication failure. "
250,  1,  " Configuration unsuccessful. Try again or restart CRSD."
251,  1,  " CRS configuration file missing."
252,  1,  " CRS configuration file syntax error."
/
253,  1,  " CRS configuration error, the CRS default directory is not set in Oracle Cluster Registry. "
// *Cause:   The Oracle Cluster Registry key which contains the user default CRS key is not 
//           initialised.
// *Action:  Check the CRS configuration. If necessary reinstall CRS.
/
254,  1,  " authorization failure"
// *Cause:  The user permissions were insufficient to operate on the
//          resource.
// *Action: Check the permissions associated with the resource using 
//          'crsctl getperm resource' and set the appropriate user permissions
//          using 'crsctl setperm resource'.
255,  1,  " CRSD is not running in privileged mode. Insufficient permissions to run this command. "
// *Cause:  The CRS daemon was not running as the privileged user.
// *Action: Check if the CRS daemon is running as root (UNIX) or Administrator 
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
// *Action: For all new use cases, use the replacement.
273,    3,  "This command is deprecated and has been replaced by '%s'"
// *Cause: A deprecated command was issued.
// *Action: For all new use cases, use the replacement.
274,    3,  "This command is deprecated and its functionality incorporated into '%s'"
// *Cause: A deprecated command was issued.
// *Action: For all new use cases, use the replacement.
275,    0,  "This command is not supported in Oracle Restart environment."
// *Cause: One of the "crs_" commands was issued  in an Oracle Restart environment.
// *Action: Use the corresponding  crsctl command. 
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
325,     1, "Unable to process the command; CRS upgrade is in progress."
// *Cause:  A command that cannot be executed when CRS upgrade is in progress was issued. 
// *Action: Retry the command after the CRS upgrade is complete.
/
/
/
401,     1, "Directory '%s' not found."
402,     1, "Could not make safe directory('%s')"
// *Cause: Unable to create safe directory.
// *Action: Check if you have proper permissions and sufficient space on the disk to create the directory.
403,     1, "Could not change working directory to safe directory('%s')"
// *Cause: Unable to change directory to safe directory.
// *Action: Check if safe directory exists and if you have proper permissions. 
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
451,  0,  " CRS configuration error, unable to initialize Oracle Cluster Registry. "
// *Cause:   The Oracle Cluster Registry that contains information about the CRS configuration
//           is unavailable.
// *Action:  Check the OCR configuration using the ocrcheck utility and resolve any issues it reports. 
//           If the problem persists, contact Oracle Support Services.
/
452,  0,  " CRS configuration error, unable to find CRSD Connection Information in Oracle Cluster Registry. "
// *Cause:   The Oracle Cluster Registry key which contains the user default CRSD connection is not
//           initialized.
// *Action:  Check the OCR configuration using the ocrcheck utility and resolve any issues it reports.
//           If the problem persists, contact Oracle Support Services.
/
453,  0,  " CRS configuration error, unable to find Instance Information in Oracle Cluster Registry. "
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

/ Alert
0602, 3, "Encountered operating system error '%s' while authenticating user '%s'. Details at %s in %s."
// *Cause:   The operating system experienced an error when Clusterware authenticated the specified user.
// *Action:  Verify that the authentication service in your environment is functioning correctly. If the problem persists, contact Oracle Support Services.

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
0714, 3, "Oracle Clusterware Release %d.%d.%d.%d.%d."
// *Cause: The Oracle High Availability Services Daemon (OHASD) was started as part of a general start of the Oracle Clusterware stack on this node.
// *Action: None.
0715, 1, "Oracle High Availability Service has timed out waiting for init.ohasd to be started."
// *Cause: The Oracle High Availability Service requires that initd start init.ohasd to successfully initialize.
// *Action: 1. Check the run level to ensure that you are in the correct runlevel using cluvfy ("cluvfy stage -pre crsinst -n <nodelist>"); 2. If the run level is correct, diagnose the reason for init.d not starting init.ohasd.
/ Alert
0716, 1, "Oracle High Availability Service failed to initialize ADR automatic purge. Details at %s in %s."
// *Cause:  An attempt to initialize automatic purge processing for the
//          Automatic Diagnostic Repository (ADR) failed.  This error is
//          not fatal, but automated periodic removal of ADR trace and
//          related data will not occur.
// *Action: ADR data can be purged manually using the ADRCI command line
//          tool.  However, repeated occurrences of this message should be
//          reported to Oracle Support Services.

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
/   1001-1100: OCR specific messages. From clsdus.msg.
/
/   NOTE TO DEVELOPER:
/              When an OCR message is added or deleted, a corresponding
/              OLR message must be added or deleted if applicable.
/              Do not fill holes in the message numbers because
/              the unused message numbers might be used by OLR messages.
/   NOTE TO TRANSLATOR:
/              These OCR messages should be translated almost identical
/              to the corresponding OLR messages (2101 - 2300).
/
//////////////////////////////////////////////////////////////////////////

/ Alert 1001 - 1030
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
// *Cause: Successfully imported the OCR contents from a file.
// *Action: None
1005, 0, "Oracle Clusterware upgrade was completed. Version has changed from [%d, %s] to [%d, %s]. Details in %s."
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
// *Action: Contact Oracle Support Services.
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
//          problem, then contact Oracle Support Services.
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
1018, 3, "Automatically repaired invalid Oracle Cluster Registry configuration on this node.  Details at %s in %s."
// *Cause: The OCR configuration on this node did not match with the OCR
//         configuration on the other nodes in the cluster; therefore, it was
//         automatically repaired.
// *Action: If this occurs repeatedly, contact Oracle Support Services.
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
// *Cause: Oracle Cluster Registry backup location did not exists, wasn't
//         mounted correctly, or did not have the required permissions.
// *Action: Ensure that the backup location exists, that it is mounted correctly
//          and visible to all nodes in the cluster, and that its permissions
//          are correct. Check the ASM entries in the alert log file for more
//          details.
1022, 0, "Oracle Clusterware was forcibly upgraded without upgrading nodes %s. Version has changed from [%u, %s] to [%u, %s]. Details in %s."
// *Cause: Oracle Clusterware was forcibly upgraded when the above listed
//         nodes were not upgraded.
// *Action: Delete the above listed nodes using the procedure documented in
//          the Oracle Clusterware documentation. If the nodes later become
//          accessible, they can be added back into the cluster.
1024, 3, "The Cluster Ready Service on this node terminated because the ASM instance was not active on this node. Details at %s in %s."
// *Cause: The Cluster Ready Service on the node terminated because the
//         ASM instance was no longer active.
// *Action: The Cluster Ready Services on this node will be automatically
//          restarted. If the problem persists, contact Oracle Support Services.
1025, 0, "Oracle Clusterware was upgraded to version [%s] on all nodes, but the cluster active version is still [%s]. Details in [%s]."
// *Cause: The cluster upgrade did not complete because the root upgrade script
//         failed on the last node, the root upgrade script was interrupted by
//         the user, or the cluster upgrade is ongoing.
// *Action: Check the Oracle Clusterware alert log on all nodes for any
//          problems. Rerun the root upgrade script on the last node to 
//          completion, and ensure that the cluster active version has 
//          changed using the 'crsctl query crs activeversion' command. If the 
//          problem persists, run diagcollection.pl and contact Oracle Support 
//          Services.
1026, 0, "Oracle Clusterware patch has completed. The patch level has changed from [%u] to [%u]. Details in %s."
// *Cause: The Oracle Clusterware was successfully patched.
// *Action: None.
1027, 1, "The Oracle Cluster Registry (OCR) location in an ASM disk group [%s] does not have sufficient space. Details at %s in %s."
// *Cause: Unable to increase the size of OCR file in the above listed disk
//         group as the disk group was out of space.
// *Action: Delete unused files from the disk group or add additional disks to
//          the disk group. Refer to Oracle Clusterware administration
//          documentation to know about the space requirements for OCR in ASM
//          disk group.
1028, 0, "The Oracle Cluster Registry backup location %s is inaccessible from node %s. Details in %s." 
// *Cause: The backup location provided did not exist, was not 
//         mounted correctly, or did not have the required permissions. 
// *Action: Ensure that the backup location exists, that it is mounted 
//          correctly and visible to all nodes in the cluster, and that the
//          permissions are correct. If the backup location is an 
//          ASM disk group, check the ASM entries in the alert log file for 
//          more details.
1029, 0, "The Oracle Cluster Registry backup file %s is corrupt. Details at %s in %s." 
// *Cause: The backup file created by the periodic backup of the Oracle Cluster
//         Registry (OCR) failed to pass the post-backup sanity check.  
//         Either the OCR was corrupted or the backup was faulty. 
// *Action: If the fault was introduced during the backup generation, then it
//          will be corrected during the next backup generation, and no action
//          is required. If the subsequent backup is also faulty, then the 
//          Oracle Cluster Registry might be corrupt. Contact Oracle 
//          Support Services.
1030, 0, "The Oracle Cluster Registry backup file %s could not be validated. Details at %s in %s." 
// *Cause: The indicated Oracle Cluster Registry (OCR) backup file 
//         could not be validated due to validation process not starting or 
//         failing to run the validation check.
// *Action: If the backup was attempted as part of an automatic periodic backup, 
//          then no action is needed. If the backup was attempted as part of a 
//          manual backup, then try the backup again.
//          If the problem persists, contact Oracle Support Services.
1031, 0, "The Oracle Cluster Registry operation encountered ASM error. Details at %s in %s." 
// *Cause: The Oracle Cluster Registry (OCR) operation could not be completed
//         due to the referenced ASM errors.
// *Action: Check the referenced log file for more detailed failure 
//          information. 
/


///////////////////////////////////////////////////////////////////////////
/
/ 1101-1149 Clusterware upgrade specific messages
/ 1150-1200 Clusterware patching specific messages
/
//////////////////////////////////////////////////////////////////////////

/ SET CRS ACTIVEVERSION 1101 - 1130

1101, 0, "Started to upgrade the OCR.\n"
// *Document: NO
1102, 0, "The OCR was successfully upgraded.\n"
// *Document: NO
1103, 0, "Started to upgrade CRS.\n"
// *Document: NO
1104, 0, "CRS was successfully upgraded.\n"
// *Document: NO
1105, 0, "Started to upgrade CSS.\n"
// *Document: NO
1106, 0, "CSS was successfully upgraded.\n"
// *Document: NO
1107, 0, "Started to upgrade EVM.\n"
// *Document: NO
1108, 0, "EVM was successfully upgraded.\n"
// *Document: NO
1109, 0, "Successfully upgraded the active version of Oracle Clusterware.\n"
// *Document: NO

1110, 0, "Oracle Clusterware upgrade is in unknown state [%d].\n"
// *Cause: There was an internal error upgrading the Oracle Clusterware.
// *Action: Retry the 'crsctl set crs activeversion' command. If the problem
//          persists, contact Oracle Support Services.

1111, 0, "Error upgrading the active version of Oracle Clusterware:\n%s.\n"
// *Cause: There was an internal error upgrading the active version of
//         Oracle Clusterware.
// *Action: Verify using the 'crsctl check crs' command that the CRS Service 
//          is running. Retry the 'crsctl set crs activeversion' command.
//          If the problem persists, contact Oracle Support Services.

1112, 0, "failed to set Oracle Clusterware active version %s"
// *Cause: There was an internal error upgrading the Oracle Clusterware.
// *Action: Retry the 'crsctl set crs activeversion' command. If the problem
//          persists, contact Oracle Support Services.

1113, 0, "Oracle Clusterware active version was successfully set to %s.\n"
// *Document: NO

1114, 0, "Invalid active version [%s] passed"
// *Cause: An invalid active version was passed.
// *Action: Use the 'crsctl query crs softwareversion' command to retrieve a 
//          valid active version. 

1115, 0, "Oracle Clusterware has already been upgraded.\n"
// *Cause: Oracle Clusterware is already running in highest possible operating
//         version.
// *Action: None

1116, 0, "Upgrade of the active version of Oracle Clusterware has been aborted.\n"
// *Cause: One of the Oracle Clusterware components have failed to upgrade
//         within the expected time.
// *Action: Check the Oracle Clusterware alert log and the CRS daemon log for
//          additional information.

1117, 0, "Error upgrading the active version of Oracle Clusterware.\n"
// *Cause: An attempt was made to change the Oracle Clusterware active
//         version before all nodes were upgraded.
// *Action: Run root.sh script on all nodes in the cluster. If the problem 
//          persists, contact Oracle Support Services.

1118, 0, "Started to upgrade the active version of Oracle Clusterware. This operation may take a few minutes.\n"
// *Document: NO

1119, 0, "Unable to complete Oracle Clusterware upgrade while nodes %s have not yet upgraded.\n"
// *Cause: An attempt was made to change the Oracle Clusterware active
//         version before all known nodes had been upgraded. Note that some of
//         the nodes listed in the message may no longer be current or recent
//         cluster members.
// *Action: Issue the 'olsnodes' command to list current and recent cluster
//          members.  Any nodes listed in the error message, but not listed by
//          'olsnodes' have not been active recently, and should be deleted
//          using the procedure documented in the Oracle Clusterware 
//          documentation.
//          The currently or recently active cluster members listed by
//          'olsnodes' should be upgraded, or, if no longer needed, deleted:
//              1) Run the rootupgrade.sh script on each node to be retained.
//              2) Delete nodes no longer desired using the procedure
//                 documented in the Oracle Clusterware documentation.
//          Once all of the nodes listed in the message have been upgraded or
//          deleted, run the rootupgrade.sh script on an upgraded node to 
//          complete the upgrade.
//          If one or more nodes could not upgraded or deleted, forcibly
//          upgrade the cluster using the procedure documented in the 
//          Oracle Clusterware documentation.

1120, 2, "Attempting to forcibly upgrade the active version of Oracle Clusterware using only the nodes %s.\n"
// *Document: NO

1121, 2, "Oracle Clusterware was forcibly upgraded without upgrading nodes %s.\n"
// *Cause: Oracle Clusterware was forcibly upgraded when the above listed
//         nodes were not upgraded.
// *Action: Delete the above listed nodes using the procedure documented in
//          the Oracle Clusterware documentation. If the nodes later become
//          accessible, they can be added back into the cluster.

1122, 0, "Forcibly upgraded the active version of Oracle Clusterware.\n"
// *Document: NO

1123, 0, "Oracle Clusterware active version was forcibly set to %s.\n"
// *Document: NO

1124, 0, "Invalid active version [%s] retrieved."
// *Cause: An invalid active version was retrieved from the configuration.
// *Action: Contact Oracle Support Services.

/ Status messages continued from 1109
1125, 0, "Started to upgrade Oracle ASM.\n"
// *Document: NO
1126, 0, "Oracle ASM was successfully upgraded.\n"
// *Document: NO
1127, 0, "Started to upgrade Oracle IOServer.\n"
// *Document: NO
1128, 0, "Oracle IOServer was successfully upgraded.\n"
// *Document: NO

1129, 0, "Rejecting rolling upgrade mode change because Oracle ASM is in an unexpected state."
// *Cause:  A request to reset rolling upgrade mode was rejected because 
//          Oracle ASM was in an unexpected state.
// *Action: Retry the 'crsctl set crs activeversion' command. If the problem
//          persists, contact Oracle Support Services.

1130, 0, "Rejecting rolling upgrade mode change because Oracle IOServer is in an unexpected state."
// *Cause:  A request to reset rolling patch mode was rejected because
//          Oracle IOServer was in an unexpected state.
// *Action: Retry the 'crsctl set crs activeversion' command. If the problem
//          persists, contact Oracle Support Services.

/ START ROLLINGUPGRADE 1131 - 1150

1131, 0, "The cluster was successfully set to rolling upgrade mode.\n"
// *Cause: A 'crsctl start rollingupgrade' command completed successfully.
// *Action: None.  

1132, 0, "The cluster is in rolling upgrade mode."
// *Cause: The cluster was already running in rolling upgrade mode.
// *Action: None.

1133, 0, "There was an error setting Oracle Clusterware to rolling upgrade mode."
// *Cause: There was an error setting Oracle Clusterware to rolling upgrade 
//         mode.
// *Action: Verify using the 'crsctl check crs' command that the Cluster Ready
//          Services (CRS) is active, and inspect the accompanying 
//          Clusterware-specific error messages to see if there is a 
//          correctable problem. If so, correct the problem and retry the 
//          'crsctl start rollingupgrade' command. If the problem persists, 
//          contact Oracle Support Services.

1134, 0, "There was an error setting Oracle ASM to rolling upgrade mode."
// *Cause: There was an error setting Oracle ASM to rolling upgrade mode.
// *Action: Verify using the 'srvctl status asm' command that the Oracle ASM
//          instance is active, and inspect the accompanying ASM-specific error
//          messages to see if there is a correctable problem. If so, correct
//          the problem and retry the 'crsctl start rollingupgrade' command. 
//          If the problem persists, contact Oracle Support Services.

1135, 0, "There was an error setting Oracle IOServer to rolling upgrade mode."
// *Cause: There was an error setting Oracle IOServer to rolling upgrade mode.
// *Action: Verify using the 'srvctl status ioserver' command that the 
//          Oracle IOServer instance is active, and inspect the 
//          accompanying IOServer-specific error messages to see if there is a 
//          correctable problem. If so, correct the problem and retry the 
//          'crsctl start rollingupgrade' command. If the problem persists, 
//          contact Oracle Support Services.

1136, 0, "Rejecting the rolling upgrade mode change because the cluster is being patched."
// *Cause:  The rolling upgrade mode change was rejected because the cluster
//          was being patched.
// *Action: Complete applying the patch on all nodes in the cluster before
//          retrying the 'crsctl start rollingupgrade' command.

1137, 0, "Rejecting the rolling upgrade mode change because the cluster was forcibly upgraded."
// *Cause: The rolling upgrade mode change was rejected because the cluster was
//         forcibly upgraded.
// *Action: Delete the nodes that were not upgraded using the procedure 
//          documented in the Oracle Clusterware documentation. Retry the 
//          'crsctl start rollingupgrade' command after completing the above 
//          steps.

1138, 0, "There was an error setting the cluster to rolling upgrade mode."
// *Cause: There was an internal error setting the cluster to rolling 
//         upgrade mode.
// *Action: Retry the 'crsctl start rollingupgrade' command. If the problem
//          persists, contact Oracle Support Services.

1139, 0, "Invalid version [%s] passed"
// *Cause: An invalid version was passed.
// *Action: Use the version returned by the 'crsctl query crs releaseversion'
//          command issued from the Oracle Grid Infrastructure home to which 
//          you are upgrading.

1140, 0, "The passed version [%s] cannot be less than or equal to the release version [%s]."
// *Cause: A version was passed that was less than or equal to the  
//         release version.
// *Action: Verify that the version of the Oracle Grid Infrastructure home to
//          be upgraded to is greater than the current Oracle Grid 
//          Infrastructure home.

1141, 0, "The passed version [%s] cannot be less than or equal to the cluster active version [%s]."
// *Cause: A version was passed that was less than or equal to the cluster 
//         active version.
// *Action: Verify that the version of the Oracle Grid Infrastructure home to
//          be upgraded to is greater than the cluster active version.

1142, 0, "The cluster cannot be set to rolling upgrade mode because Oracle Clusterware is not active on at least one remote node."
// *Cause: The cluster could not be set to rolling upgrade mode because 
//         Oracle Clusterware was not active on any of the remote nodes.
// *Action: Start Oracle Clusterware on at least one remote node and retry the
//          'crsctl start rollingupgrade' command, or retry upgrade using the
//          non-rolling option.

/ PATCHING 

1151, 0, "The cluster was successfully set to rolling patch mode.\n"
// *Cause: A 'crsctl start rollingpatch' command completed successfully.
// *Action: None.  

1152, 0, "The cluster is in rolling patch mode."
// *Cause: The cluster was already running in rolling patch mode.
// *Action: None.

1153, 0, "There was an error setting Oracle Clusterware to rolling patch mode."
// *Cause: There was an error setting Oracle Clusterware to rolling patch mode.
// *Action: Verify using the 'crsctl check crs' command that the Cluster Ready
//          Services (CRS) is active, and inspect the accompanying 
//          Clusterware-specific error messages to see if there is a 
//          correctable problem. If so, correct the problem and retry the 
//          'crsctl start rollingpatch' command. If the problem persists, 
//          contact Oracle Support Services.

1154, 0, "There was an error setting Oracle ASM to rolling patch mode."
// *Cause: There was an error setting Oracle ASM to rolling patch mode.
// *Action: Verify using the 'srvctl status asm' command that the Oracle ASM
//          instance is active, and inspect the accompanying ASM-specific error
//          messages to see if there is a correctable problem. If so, correct
//          the problem and retry the 'crsctl start rollingpatch' command. 
//          If the problem persists, contact Oracle Support Services.

1155, 0, "There was an error setting Oracle IOServer to rolling patch mode."
// *Cause: There was an error setting Oracle IOServer to rolling patch mode.
// *Action: Verify using the 'srvctl status ioserver' command that the 
//          Oracle IOServer instance is active, and inspect the 
//          accompanying IOServer-specific error messages to see if there is a 
//          correctable problem. If so, correct the problem and retry the 
//          'crsctl start rollingpatch' command. If the problem persists, 
//          contact Oracle Support Services.

1156, 0, "Rejecting the rolling patch mode change because the cluster is in the middle of an upgrade."
// *Cause:  The rolling patch mode change was rejected because the cluster
//          was undergoing an upgrade.
// *Action: None.

1157, 0, "Rejecting the rolling patch mode change because the cluster was forcibly upgraded."
// *Cause: The rolling patch mode change was rejected because the cluster was
//         forcibly upgraded.
// *Action: Delete the nodes that were not upgraded using the procedure
//          documented in the Oracle Clusterware documentation. Retry the 
//          'crsctl start rollingpatch' or 'crsctl stop rollingpatch'
//          command after completing the above steps.

1158, 0, "There was an error setting the cluster to rolling patch mode."
// *Cause: There was an internal error setting the cluster to rolling 
//         patch mode.
// *Action: Retry the 'crsctl start rolling patch' command. If the problem
//          persists, contact Oracle Support Services.

1159, 0, "The cluster cannot be set to rolling patch mode because Oracle Clusterware is not active on at least one remote node."
// *Cause: The cluster could not be set to rolling patch mode because 
//         Oracle Clusterware was not active on any of the remote nodes.
// *Action: Start Oracle Clusterware on at least one remote node and retry the
//          'crsctl start rollingpatch' command, or retry patching using the
//          non-rolling option.

1161, 0, "The cluster was successfully patched to patch level [%u].\n"
// *Cause: A 'crsctl stop rollingpatch' command completed successfully.
// *Action: None.  

1162, 0, "Rejecting rolling patch mode change because the patch level is not consistent across all nodes in the cluster. The patch level on nodes %s is not the same as the expected patch level [%u] found on nodes %s."
// *Cause:  The 'crsctl stop rollingpatch' command was rejected because all
//          the nodes in the cluster were not patched to the same patch level.
// *Action: Make sure all the nodes in the cluster have been patched to the 
//          same patch level using the 'crsctl query crs softwarepatch <host>'
//          command. Retry the 'crsctl stop rollingpatch' command after 
//          patching the required nodes. 

1163, 0, "There was an error resetting Oracle Clusterware rolling patch mode."
// *Cause: There was an error resetting Oracle Clusterware rolling patch mode.
// *Action: Verify using the 'crsctl check crs' command that the Cluster Ready
//          Services (CRS) is active, and inspect the accompanying 
//          Clusterware-specific error messages to see if there is a 
//          correctable problem. If so, correct the problem and retry the 
//          'crsctl stop rollingpatch' command. If the problem persists, 
//          contact Oracle Support Services.

1164, 0, "There was an error resetting Oracle ASM rolling patch mode."
// *Cause: There was an error resetting Oracle ASM rolling patch mode.
// *Action: Verify using the 'srvctl status asm' command that the Oracle ASM
//          instance is active, and inspect the accompanying ASM-specific error
//          messages to see if there is a correctable problem. If so, correct
//          the problem and retry the 'crsctl stop rollingpatch' command. 
//          If the problem persists, contact Oracle Support Services.

1165, 0, "There was an error resetting Oracle IOServer rolling patch mode."
// *Cause: There was an error resetting Oracle IOServer rolling patch mode.
// *Action: Verify using the 'srvctl status ioserver' command that the 
//          Oracle IOServer instance is active, and inspect the 
//          accompanying IOServer-specific error messages to see if there is a 
//          correctable problem. If so, correct the problem and retry the 
//          'crsctl stop rollingpatch' command. If the problem persists, 
//          contact Oracle Support Services.

1166, 0, "Rejecting rolling patch mode change because Oracle ASM is in [%s] state."
// *Cause:  A request to reset rolling patch mode was rejected because 
//          Oracle ASM was in an unexpected state.
// *Action: Retry the 'crsctl stop rollingpatch' command. If the problem
//          persists, contact Oracle Support Services.

1167, 0, "Rejecting rolling patch mode change because Oracle IOServer is in [%s] state."
// *Cause:  A request to reset rolling patch mode was rejected because
//          Oracle IOServer was in an unexpected state.
// *Action: Retry the 'crsctl stop rollingpatch' command. If the problem
//          persists, contact Oracle Support Services.

1168, 0, "There was an error resetting the cluster rolling patch mode."
// *Cause: There was an internal error resetting the cluster rolling 
//         patch mode.
// *Action: Retry the 'crsctl stop rolling patch' command. If the problem
//          persists, contact Oracle Support Services.

1169, 0, "The cluster is consistent and the cluster active patch level is [%u]."
// *Cause: The cluster has already completed the rolling patch procedure.
// *Action: None.

1170, 0, "Rejecting rolling patch mode change because the patch has not been applied yet. The software patch level [%u] on this node is not the same as the expected patch level [%u]."
// *Cause:  The 'crsctl stop rollingpatch' command was rejected because the
//          patch level did not match with the configured software patch level.
// *Action: Complete applying the patch on this node, and verify the patch 
//          level using the 'crsctl query crs softwarepatch <host>'
//          command. Retry the 'crsctl stop rollingpatch' command.

1171, 0, "Rejecting rolling patch mode change because the patch level is not consistent across all nodes in the cluster. The patch level on nodes %s is not the same as the patch level [%u] found on nodes %s."
// *Cause:  The 'crsctl stop rollingpatch' command was rejected because all
//          the nodes in the cluster were not patched to the same patch level.
// *Action: Verify the list of patches applied on a node by issuing the 
//          the 'crsctl query crs releasepatch' command. Apply the requisite
//          patches. Make sure all the nodes in the cluster have been patched
//          to the same patch level using the 'crsctl query crs softwarepatch' 
//          command. Retry the 'crsctl stop rollingpatch' command after 
//          patching the required nodes. 

1181, 0, "There was an error retrieving Oracle Clusterware release patch level."
// *Cause: There was an internal error retrieving the Oracle Clusterware 
//         release patch level.
// *Action: Contact Oracle Support Services.

1182, 0, "Oracle Clusterware release patch level is [%u] and the complete list of patches [%s] have been applied on the local node.\n"
// *Cause: None, this is an informational message.
// *Action: None.

1183, 0, "Oracle Clusterware release patch level is [%u] and an incomplete list of patches [%s] have been applied on the local node.\n"
// *Cause: There was an error retrieving the complete list of patches.
// *Action: Contact Oracle Support Services.

1184, 0, "Oracle Clusterware release patch level is [%u] and no patches have been applied on the local node.\n"
// *Cause: None, this is an informational message.
// *Action: None.

1191, 0, "There was an error retrieving Oracle Clusterware software patch level."
// *Cause: There was an internal error retrieving the Oracle Clusterware 
//         software patch level.
// *Action: Contact Oracle Support Services.

1192, 0, "Oracle Clusterware patch level on node %s is [%u].\n"
// *Cause: None, this is an informational message.
// *Action: None.


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   1201-1300: CRSD specific messages. From clsdus.msg.
/
/   NOTE TO DEVELOPER:
/              When a CRS message is added or deleted, a corresponding
/              OHAS message must be added or deleted if applicable.
/              Do not fill holes in the message numbers because
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
/              Do not fill holes in the message numbers because
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
1340, 1, "Node '%s' has a pending role change; Oracle High Availability Services needs to be restarted."
// *Cause: A 'crsctl stop cluster' command was run after a node's role has changed.
// *Action: Run 'crsctl stop crs' and 'crsctl start crs' on the node for the node role change to take effect.

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
1603, 0, "CSSD on node %s has been shut down."
// *Cause:  The CSS daemon on the listed node was terminated.
// *Action: None.
1604, 0, "CSSD voting file is offline: %s; details at %s in %s."
// *Cause:  The indicated voting file became unusable on the local node either
//          because it was being replaced or because it was not accessible. 
// *Action: 1. No action necessary if the voting file was replaced. 
//          2. If the voting file was not replaced then verify that the 
//             filesystem containing the indicated voting file is
//             available on the local node.
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

1649, 0, "An I/O error occurred for voting file: %s; details at %s in %s."
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
/ Alert
1664, 0, "No voting files found; switching node role to 'leaf'."
// *Cause: A node attempting to start as a Hub node was not able to find a voting file.
// *Action: No action is required.
/ Alert
1665, 0, "maximum number of cluster Hub nodes reached; the CSS daemon is terminating"
// *Cause: A node attempting to start as a Hub node found the maximum number
//         of Hub nodes already active.
// *Action: If the configured node role is 'auto', no action is required
//          for the node to restart as a Leaf node.  If the configured
//          node role is 'hub', then the configured role must be changed
//          to a Leaf node using 'crsctl set node role leaf' or the Hub size
//          must be increased using 'crsctl set cluster hubsize'.
/ Alert
1666, 0, "no Hub nodes found; switching node role to 'hub'"
// *Cause: A node attempting to start as a Leaf node was unable to locate any Hub nodes.
// *Action: No action is required.
/ Alert
1667, 0, "node %s not allowed to join because the maximum number of Hub nodes has been reached"
// *Cause: A node attempting to start as a Hub node found the maximum number
//         of Hub nodes already active.
// *Action: No action is required.
1668, 0, "operation is not allowed on a Leaf node\n"
// *Cause: An unsupported operation was requested on a Leaf node.
// *Action: Retry this operation on a Hub node.
/
1669, 0, "The number of voting files available %d is less than the minimum number of voting files required %d."
// *Cause:  The number of voting files has decreased to a number of files
//          that is insufficient.
// *Action: Look in the alert log for related messages such as 1714,
//          1604, 1613, 1614 and 1615 and act accordingly.
/ Alert
1670, 0, "Leaf node could not find any Hub nodes to connect to; details at %s in %s"
// *Cause:  A Leaf node attempted to join the cluster but could not find a 
//          Hub node to which to connect.
// *Action: Verify that the clusterware stack is up and running on at least 
//          one Hub node and, if not, start the stack on one or more Hub nodes.
//          Verify that the Grid Naming Service (GNS) resource is active on a Hub node.
//          If not, start it on at least one node. Check if the network connectivity 
//          is viable to all Hub nodes that have the clusterware stack running. 
//          If the Leaf node startup has exhausted its retry attempts, it may be 
//          necessary to start the clusterware stack manually on the Leaf node.
//          Contact Oracle Support Services if all of the above is verified 
//          and the Leaf node is not able to find any Hub nodes to which to
//          to connect.

1671, 3, "The value for parameter %s is outside the allowed range of %d to %d\n"
// *Cause:  An attempt was made to set a parameter with invalid value.
// *Action: Set the parameter with a value in the indicated range.

1672, 0, "The number of voting files currently available %d has fallen to the minimum number of voting files required %d."
// *Cause:  The Cluster Synchronization Service daemon (CSSD) has detected that
//          the number of voting files currently available is equal to the
//          minimum number of voting files required on the node. There is risk
//          of node eviction in the case of another voting disk failure. 
// *Action: Restore access to voting files or configure additional voting disks 
//          so that the number of voting files currently available is 
//          more than the minimum number of voting files required.

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
//           'crsctl replace votedisk'

  

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
/
1718,0,"The CSS daemon is unable to continue due to a failure in required component %s."
// *Cause:  A component required by the Cluster Synchronization Service
//          (CSS) daemon has failed.  The CSS daemon is unable to
//          continue and is failing.
// *Action: See the alert log for more detailed messages indicating the
//          nature of the problem and the location of additional
//          information regarding this error.
/
1719,0,"Cluster Synchronization Service daemon (CSSD) %s not scheduled for %d msecs."
// *Cause:  Excessive system load has prevented threads in the Cluster
//          Synchronization Service daemon (CSSD) from being scheduled for
//          execution for the time indicated in the message. This indicates
//          the system is overloaded. 
// *Action: Take steps to reduce the system load or increase system 
//          resources to handle the load.  
/
1720,0,"Cluster Synchronization Services daemon (CSSD) is ready for operation."
// *Cause:  Cluster Synchronization Services daemon (CSSD) is fully initialized
//          and functional. CSSD group membership services has started.
//          Services dependent on CSSD can start using cluster synchronization
//          services.
// *Action: None.
1721,0,"Cluster Synchronization Service daemon (CSSD) was unable to complete initialization for fence type %s."
// *Cause:  The Cluster Synchronization Service daemon (CSSD) failed to complete
//          initialization for the indicated fence type, most likely because of
//          a failure in the associated support entity. The entities CSSD 
//          depends on are ASM, DISKMON. Messages in the alert log from DISKMON 
//          or ASM may supply additional details.
// *Action: Contact Oracle Support Services.
/          
1722,0,"Cluster Synchronization Service daemon encountered an internal error."
// *Cause:  CSSD failed due to an internal error.
// *Action: Contact Oracle Support Services. 
/
1723,0,"Cluster Synchronization Services daemon (CSSD) exited because it failed to spawn thread %s."
// *Cause:  Cluster Synchronization Services failed to spawn the indicated 
//          critical thread due to an operating system error. 
//          The accompanying message provides additional details on 
//          failed system call.
// *Action: Contact Oracle Support Services. 
/
1724,0,"CSSD agent failed to spawn CSSD process"
// *Cause:  The Cluster Synchronization Services daemon could not be started 
//          because the operating system failed to spawn the process. 
// *Action: Contact Oracle Support Services. 
/
1725,0,"Encountered operating system error '%s' while performing operation '%s'."
// *Cause:  The operating system encountered an error for the indicated operation.
// *Action: Contact Oracle Support Services. 
1726,0,"Process failed to run in real-time priority. Details at %s in %s."
// *Cause : CSSD, CSSDMONITOR or CSSDAGENT failed to set real-time priority.
// *Action: Contact Oracle Support Services.
/
1727,0,"Network communication between this node '%s' (%d) and node '%s' (%d) re-established. Node removal no longer imminent."
// *Cause : None.
// *Action: None.
/
/ translation note - both occurrences of %d are inserting numeric values

1728, 0, "The majority of voting files are accessible on %d sites, however %d sites are required, terminating to ensure data integrity; details at %s in %s"

// *Cause:  A check on voting file accessibility prompted by a voting file 
//          management operation, periodic voting file access or lease 
//          acquisition determined that a majority of voting files on a 
//          majority of sites were not accessible by the local node.

// *Action: Delete the voting files that are no longer available, as 
//          indicated by message CRS-01637, using the appropriate 'crsctl'
//          commands. Run the crsctl command either on another node where the
//          clusterware stack is active, or by starting the clusterware 
//          stack in exclusive mode.
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   1801-1900: CLSCFG specific messages. From clsdus.msg. Alerts
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
1810, 0, "Node-specific configuration for node %s in Oracle Local Registry was patched to patch level %u."
// *Cause:  None.
// *Action: None.
1811, 0, "Node %s patched to patch level %u."
// *Cause:  None.
// *Action: None.


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
/ 2013 - Added because of bug 13626519
/
2013, 0, "user %s does not have the required privileges"
// *Cause: An attempt to make a diagnostic connection to a Clusterware daemon failed 
//         because the user does not have required privileges.
// *Action: Use system tools to identify the user of the specified daemon process.
//          Log on as the same user as the specified daemon process and try again.
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/   2101-2300: OLR specific messages
/    NOTE TO DEVELOPER:
/              OLR message number = OCR message number + 1100
/              When an OLR message is added or deleted, a corresponding
/              OCR message must be added or deleted if applicable.
/              Do not fill holes in the message numbers because
/              the unused message numbers might be used by OCR messages.
/    NOTE TO TRANSLATOR:
/              These OLR messages should be translated almost identical
/              to the corresponding OCR messages (1001 - 1200).
/
///////////////////////////////////////////////////////////////////////////
/
/ Alert 2101 - 2128
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
// *Cause: Successfully imported the OLR contents from a file.
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
/2121 is not applicable to OLR
/
/2122 is not applicable to OLR
/
/2124 is not applicable to OLR
/
/2125 is not applicable to OLR
/
/2128 is not applicable to OLR
/
2129, 1, "The Oracle Local Registry backup file %(1)s is corrupt. Details at %(2)s in %(3)s."
// *Cause: The backup file created by the periodic backup of the Oracle Local
//         Registry (OLR) failed to pass the post-backup sanity check.
//         Either the OLR was corrupted or the backup was faulty.
// *Action: If the fault was introduced during the backup generation, then it
//          will be corrected during the next backup generation, and no action
//          is required. If the subsequent backup is also faulty, then the
//          Oracle Local Registry might be corrupt. Contact Oracle
//          Support Services.
/
2130, 0, "The Oracle Local Registry backup file %s could not be validated. Details at %s in %s." 
// *Cause: The indicated Oracle Local Registry (OLR) backup file 
//         could not be validated due to validation process not starting or
//         failing to run the validation check.
// *Action: Re-attempt to backup the Oracle Local Registry (OLR). 
//          If the problem persists, contact Oracle Support Services.
/

//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
/
/   2301-2400: GPNP specific messages 
/   Added in Trail Blazer 
/  
/   NOTE: If a message is added or removed, update
/         the enum clsgpnpmsg in has/include/clsgpnp0.h
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
// *Action: If error persists, contact Oracle Support Services. 
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

2308, 1, "GPnP wallets either missing or access denied. Wallet home: %s."
// *Cause: GPnP failed to open wallets for read. Either GPnP wallets are missing or the user does not have permissions to access them.
// *Action: Ensure that the GPnP wallets exist and that the user has read access permission on them. If the problem persists, contact Oracle Support Services.
/

// 2309, UNUSED
// *Cause: 
// *Action:
// This msg id is not used.
/

2310, 1, "Failed to initialize security facility. "
// *Cause: Error occurred while initializing GPnP security component.
// *Action: If the problem persists, contact Oracle Support Services.
/

2311, 1, "Failed to initialize Resource Discovery. RD error: %s. Make sure RD providers installed properly. "
// *Cause: Error occurred while initializing GPnP Resource Discovery (RD).
// *Action: If the problem persists, contact Oracle Support Services.
/

2312, 1, "Failed to initialize XML Developer's Kit (XDK). XDK error %s. "
// *Cause: Error occurred while initializing XML Developer's Kit component (XDK).
// *Action: If the problem persists, contact Oracle Support Services.
/

2313, 1, "Failed to initialize GIPC communication layer. GIPC error: %s. "
// *Cause: Error occurred while initializing GIPC communication layer.
// *Action: If the problem persists, contact Oracle Support Services.
/

2314, 1, "Cannot initialize locking subsystem. "
// *Cause: Error occurred while initializing locking subsystem.
// *Action: If the problem persists, contact Oracle Support Services.
/

2315, 1, "Failed to initialize GPnP certkey providers. "
// *Cause: GPnP certkey provider(s) data was not found or corrupt.
// *Action: If the problem persists, contact Oracle Support Services.
/

2316, 1, "Cannot initialize GPnP, %s (%s). " 
// *Cause: General GPnP initialization failure.
// *Action: If the problem persists, contact Oracle Support Services.
/

2317, 1, "Cannot get local GPnP security keys (wallet). "
// *Cause: GPnP wallet(s) directory or files were not found or corrupt.
// *Action: If the problem persists, contact Oracle Support Services.
/

2318, 1, "GPNPD is not found. "
// *Cause: Local GPnP service is not found.
// *Action: Make sure GPNPD is running.
/

2319, 1, "No cluster name found in GPnP profile. "
// *Cause: Profile is invalid - it must specify a mandatory clustername 
// parameter.
// *Action: Contact Oracle Support Services.
/

2320, 1, "No sequence number found in GPnP profile. "
// *Cause: Profile is invalid - it must specify a mandatory profile sequence 
// parameter.
// *Action: Contact Oracle Support Services.
/

2321, 1, "Flex Cluster mode configuration not found in Grid Plug and Play (GPnP) profile. "
// *Cause: The Profile did not have Flex Cluster mode configuration and could not be used
// to bring up the stack in Flex Cluster mode.
// *Action: Contact Oracle Support Services.
/

2322, 1, "Cannot get local GPnP profile. Error initializing GPnP profile cache providers. "
// *Cause: Local GPnP setup was invalid. 
// *Action: Contact Oracle Support Services.
/

2323, 1, "Error initializing one of the GPnP profile cache providers. "
// *Cause: Local GPnP setup was invalid. 
// *Action: Contact Oracle Support Services.
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
// *Cause: GPnP profile was different across cluster nodes.
// *Action: Try to repeat the update.  If the problem persists, contact Oracle Support Services. 
/

2327, 3, "GPNPD already running on node %s. Terminating. "
// *Cause: GPnP service instance was already running on node.
// *Action: Bring down existing GPNPD instance first.
/

2328, 3, "GPNPD started on node %s. "
// *Cause: GPnP service started on node.
// *Action: None.
/

2329, 3, "GPNPD on node %s shut down. "
// *Cause: GPnP service was shut down by request.
// *Action: None.
/

2330, 1, "GPNPD failed to start listening for GPnP peers. " 
// *Cause: GPnP service failed to open server endpoint.
// *Action: Check GPNPD logs for the cause. If the problem persists, contact Oracle Support Services. 
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

/Alert
2336, 1, "GPNPD failed get local GPnP profile and cannot continue. Check gpnpd/gpnp client logs. "
// *Cause: GPnP service cannot find a profile in local cache, and cannot continue.
// *Action: Contact Oracle Support Services.
/

/Alert
2337, 1, "GPNPD advertisement with %s succeeded. "
// *Cause: Grid Plug and Play Daemon (GPNPD) successfully advertised with 
//         a specified service (for example, Multicast Domain Name Service 
//         Daemon (MDNSD) or Oracle Grid Naming Service (GNS)) previously 
//         failed with CRS-2339.
// *Action: None.
/

//2338, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

/Alert
2339, 1, "GPNPD advertisement with %s failed. This may block some cluster configuration changes. Advertisement attempts will continue."
// *Cause:  Grid Plug and Play Daemon (GPNPD) failed to advertise itself 
//          with a specified service (for example, Multicast Domain Name 
//          Service Daemon (MDNSD) or Oracle Grid Naming Service (GNS)).
//          Advertisement attempts will continue at regular intervals,
//          and alerts will periodically be issued. 
// *Action: Make sure the specified service is running and wait for the success
//          message CRS-2337 before changing the cluster configuration.
/

2340, 1, "Errors occurred while processing received gpnp message. " 
// *Cause: Invalid GPnP message received.
// *Action: Check gpnp client and GPNPD logs for details. If the problem persists, contact Oracle Support Services. 
/

2341, 3, "GPNPD on node %s shutting down on signal %d. "
// *Cause: GPnP service shutting down due to received signal.
// *Action: Contact your cluster administrator.
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
2409, 0, "The clock on host %s differs from mean cluster time by %d microseconds. No action has been taken because the Cluster Time Synchronization Service is running in observer mode."
// *Cause: The system clock on the indicated host differed from the mean 
//         cluster time by more than 1000 microseconds. No action was taken 
//         because the Cluster Time Synchronization Service was running in 
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
2415, 1, "Resource '%s' cannot be registered because its owner '%s' is not the same as the Oracle Restart user '%s'."
// *Cause:  The resource indicated in the message could not be registered because it was owned by a user other than the Oracle Restart user.
// *Action: Resubmit as the Oracle Restart user.
/
2416, 0, "The Cluster Time Synchronization Service is in observer mode."
// *Cause: The Cluster Time Synchronization Service detected an active vendor
//         time synchronization service on at least one node in the cluster.
// *Action: Oracle Clusterware requires a time synchronization service in active
//          mode. Oracle Clusterware will work with a vendor service or the
//          Cluster Time Synchronization Service. If you want to change the
//          Cluster Time Synchronization Service to active mode, stop and
//          deconfigure the vendor time synchronization service on all nodes.
/
2417, 0, "The Cluster Time Synchronization Service is in active mode."
// *Cause: The Cluster Time Synchronization Service did not detect an active
//         vendor time synchronization service on any node in the cluster.
// *Action: None. If a vendor time synchronization service is preferred to the
//          Cluster Time Synchronization Service, then configure and start the
//          vendor time synchronization service on all nodes to change the
//          Cluster Time Synchronization Service to observer mode.
/

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ CRS Policy Engine error messages, added in Trail Blazer 2500-3500
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
2505, 1, "Another operation is being performed on '%s'. Retry later"
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
2509, 1, "Resource type '%s' used in dependency '%s' does not exist or is not registered."
// *Cause:  The resource type referenced by the dependency specification is not
//          found.
// *Action: Check the specification of the dependency, fix the problem indicated,
//     and resubmit the request.
2510, 1, "Resource '%s' used in dependency '%s' does not exist or is not registered."
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
// *Action: Circular dependencies are disallowed. Change the profile
//          and re-submit.
2516, 1, "Server pool is not specified for resource '%s'"
// *Cause:  The resource profile does not have server pool specified.
// *Action: Either specify a an existing server pool or
//          HOSTING_MEMBERS in the profile and re-submit the request.
2517, 1, "Required attribute '%s' is not specified for resource '%s'"
// *Cause:  A required attribute is missing from the resource profile.
// *Action: Add the attribute to the profile and re-submit the request.
2519, 1, "Either '%s' or '%s' must be specified when '%s' is '%s'"
// *Cause:  Neither or both of the parameters was specified.
// *Action: Specify exactly one of the two and re-submit.
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
//          the nature of the problem with the other resource. Follow up
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
//          the nature of the problem with the other resource. Follow up
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
// *Action: Re-evaluate the request.
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
// *Action: Specify a correct type.
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
2605, 1, "Server '%s' cannot be relocated from server pool '%s' because the pool disallows transfers"
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
// *Action: Double check the attributes that are supplied.
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
2618, 2, "Cannot change data type %s of existing attribute %s to type %s."
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
// *Action: Specify either of the two and re-submit.
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
2648, 1, "Configuration of resource '%s' prevents it from starting on any online servers."
// *Cause: An attempt was made to start a resource, but the resource configuration prevented it from starting.
// *Action: Check resource configuration.
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
// *Action: Specify a server for the resource using -k or -n.
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
// the nature of the problem with the other resource. Follow up
// on the action recommended for that message.
2671, 1, "Error processing attribute '%s': %s"
// *Cause:  The value specified for the attribute was inappropriate or invalid.
// *Action: Refer to the documentation and retry the request specifying a valid value for the indicated attribute.
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
2715, 1, "Update to attribute AGENT_FILENAME is not currently supported. Recreate the resource type with new value."
// *Cause: Attempt was made to update AGENT_FILENAME attribute.
// *Action: Delete existing resource type and add it back with the new value.
2716, 1, "Failure threshold exhausted for resource '%s'"
// *Cause: The resource instance has failed more times than allowed in
// the specified time interval. It will not be restarted automatically.
// *Action: Identify and fix the problem. Restart the resource
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
// *Action: Update the resource which this alias refers to
// instead.
2721, 1, "'%s' is a resource alias for '%s' and cannot be unregistered"
// *Cause: An attempt was made to unregister a resource alias as if it
// were a resource.
// *Action: Either unregister the resource which this alias refers to
// or modify its ALIAS_NAME attribute to not have a resource alias.
2722, 1, "The instance of resource '%s' may only run on '%s'; check on '%s' is unnecessary"
// *Cause: A check was issued on a server for a resource instance that may only
// run on a particular server.
// *Action: Issue a check on the server where the resource instance is
// supposed to be run.
2723, 1, "No instance of resource '%s' found on '%s'"
// *Cause: A check was issued on a server for a resource which does not have any
// offline instances and no running instances on that server.
// *Action: Issue a check on a server where a resource instance 
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
2738, 1, "Unable to modify server pool '%s' as this will affect running resources and resource groups, but the force option was not specified"
// *Cause: One or more running resources and/or resource groups would be 
//         affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
//          resources and resource groups mentioned right before this error, or 
//          use the force option for the same command.
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
2790, 3, "Starting shutdown of Cluster Ready Services-managed resources on server '%(1)s'"
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
2808, 0, "Update Configuration Policy Set"
// *Document: NO
2809, 1, "Failed to update cluster configuration policy set. Details at %s in %s."
// *Cause: Could not update repository with new configuration data.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2810, 1, "Cluster configuration policy set is corrupted. Details at %s in %s."
// *Cause: Could not read the configuration data from the repository.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2811, 0, "Unregister Server Category"
// *Document: NO
2812, 0, "Register Server Category"
// *Document: NO
2813, 0, "Modify Server Category"
// *Document: NO
2814, 1, "Server category '%s' does not exist."
// *Cause: A request was received that referenced a non-existing server category.
// *Action: Make sure a registered server category is used.
2815, 1, "Server category '%s' is already registered."
// *Cause: A request to register a server category with a duplicate name was received.
// *Action: Use a unique name.
2816, 1, "Server category '%s' cannot be unregistered as it is referenced by resource '%s'."
// *Cause:  The server category you are trying to remove has references to it.
// *Action: Make sure the server category you are trying to remove is not referenced by other entities.
2817, 1, "Server category '%s' cannot be unregistered as it is referenced by server pool '%s'."
// *Cause:  The server category you are trying to remove has references to it.
// *Action: Make sure the server category you are trying to remove is not referenced by other entities.
2818, 1, "Failed to delete server category '%s' from repository. Details at %s in %s."
// *Cause:  Could not update repository with server category details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2819, 1, "Failed to save server category '%s'. Details at %s in %s."
// *Cause: Could not update repository with server pool details.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2820, 1, "Required attribute '%s' is missing for configuration policy '%s'."
// *Cause: A required attribute was not specified.
// *Action: Make sure the attribute is specified.
2821, 1, "Fatal error while validating configuration policy '%s'."
// *Cause: There's a problem with the configuration data in the specified policy.
// *Action: This message always follows the actual error description.
2822, 1, "Server pool '%s' is not declared in the policy set."
// *Cause: Each configuration policy may only define server pool.
// configuration for the pools declared to be a part of the policy set.
// *Action: Either remove the server pool from the policy, change its
// name, or extend the policy set to include the pool's name.
2823, 1, "The new active policy name '%s' was not found."
// *Cause: An attempt to activate non-existent policy was made.
// *Action: Use a registered policy's name instead.
2824, 1, "'%s' is reserved for a built-in configuration policy and cannot be used."
// *Cause: This name is reserved for a built-in object.
// *Action: Use a different name.
2825, 1, "Configuration policy '%s' already exists."
// *Cause: A configuration policy name specified was defined multiple times.
// *Action: Make sure each policy is only defined once.
2826, 1, "Server pools cannot be removed from the configuration policy set without activating a new policy at the same time."
// *Cause: Server pools can be removed from the configuration policy set only if the command also activates a policy.
// *Action: To remove the server pools from the system, activate a new policy with the update. To remove the server pools from the policy control only, resubmit with the -ksp option.
2827, 0, "This policy is built-in and managed automatically to reflect current configuration"
// *Document: NO
2828, 1, "Failed to stop resource while attempting CARDINALITY modification"
// *Cause: An attempt to stop a resource during CARDINALITY modification failed.
// *Action: Use 'crsctl stop resource' to stop the resource manually and then retry the update operation.
2829, 0, "Update operation cannot proceed because it would need to stop resources."
// *Cause: An update to CARDINALITY would require the operation to stop resources.
// *Action: Either manually stop enough resources using 'crsctl stop resource' or specify the force option to have them selected for you.
2830, 1, "A server category name may not be empty or contain spaces."
// *Cause: A name must not be empty or contain space character(s).
// *Action: Specify a valid name.
2831, 1, "Either '%s' or '%s' may be specified, but never both."
// *Cause: Two mutually exclusive attributes were used at the same time, which is not allowed.
// *Action: Use either one or the other.
2832, 1, "Server '%s' does not belong to server category '%s' of pool '%s'."
// *Case: The server cannot be assigned to the pool as it does not belong to the category of servers that may
// be in the pool.
// *Action: Use a different server, a different pool, or change the configuration of either the pool or the 
// category or both. 
2833, 1, "Either '%s' or '%s' must be specified, or both."
// *Cause: At least one of the two attributes must have a value.
// *Action: Specify a value for either or both.
2834, 1, "One of '%s', '%s' or '%s' must be specified when '%s' is '%s'."
// *Cause: One attribute of the three is required for this configuration.
// *Action: Specify a value for one attribute of the three.
2835, 1, "Resource '%s' cannot start on server '%s' as the server does not belong to the resource's server category."
// *Cause: This resource may only run on the servers that belong to
// the server category of the resource.
// *Action: Pick a server that belongs to the category.
2836, 1, "When using a server category, the resource must have '%s' attribute set to '%s'."
// *Cause: An attempt was made to register a resorce that uses a server
// category and yet is not configured to utlize any available server.
// *Action: Set the attribute to the required value.
2837, 1, "There are no servers that belong to the server category '%s' of resource '%s'."
// *Cause: The resource cannot be started as there are no available servers that belong to its category.
// *Action: Add servers to the cluster or change the category to be more inclusive.
2838, 1, "'%s' is not a valid attribute of server categories."
// *Cause: An attempt was made to set a value for an attribute which does not belong to server categories.
// *Action: Use a valid attribute.
2839, 1, "Cluster Ready Services' active version is below required level of '%s'."
// *Cause: An attempt was made to use functionality that is only available starting from the specified active version.
// *Action: Upgrade to the minimum required version.
2840, 1, "Resource instance '%s' does not exist."
// *Cause: A request was received that referenced a nonexistent resource instance.
// *Action: Make sure a registered resource instance is used.
2841, 1, "'%s' must be a resource instance."
// *Cause: This command may only be issued on a resource instance but the supplied reference was to an
// object of a different type.
// *Action: Use a registered resource instance.
2842, 2, "Action '%s' on resource '%s' timed out."
// *Cause: The action did complete within the allotted time.
// *Action: None.
2843, 1, "Unable to complete processing of the '%s' action for resource '%s' on server '%s' as Cluster Ready Services is not reachable."
// *Cause: The processing of the specified action was aborted because
// Cluster Ready Services was no longer reachable.
// *Action: Unless the clusterware stack was stopped or the server was
// rebooted, Cluster Ready Services will restart momentarily. The
// action can be retried thereafter.
2844, 3, "Waiting for resource '%s' to start on server '%s'."
// *Cause: The resource is now expected to start on the server.
// *Action: None.
2845, 3, "Waiting for resource '%s' to stop on server '%s'."
// *Cause: The resource is now expected to stop on the server.
// *Action: None.
2846, 3, "There is no active action on resource instance '%s'"
// *Cause: An attempt was made to finish an action on the resource instance while no 
// corresponding attempt to start the action was found or an attempt to start the action was
// timed out before a request to finish the action arrived.
// *Action: Check the state of the resource and re-do the complete
// cycle if needed.
2847, 1, "Authorization failure: OS User '%s' does not exist on server '%s' "
// *Cause: The specified operating system user does not exist on the specified server. Cluster Ready Services requires that all users used by the resource it manages exist on each server of the cluster.
// *Action: Add the specified operating user on the specified server.
2848, 1, "Error while reading resources: Resource: %s . Error: %s  Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2849, 2, "Authorization failure:  Resource [ %s ]   "
// *Cause: A resource operation could not be performed because authorization checking failed.
// *Action: Check the ownership, group, and permissions associated with the resource and ensure that the associated operating system user and group definitions are consistent on all cluster nodes.
2850, 3, "Start of '%s' on '%s' has been delayed to maintain concurrency limit of %d."
// *Cause: The configured concurrent start action limit was reached.
// *Action: The start action will automatically resume as soon as possible.
2851, 3, "Stop of '%s' on '%s' has been delayed to maintain concurrency limit of %d."
// *Cause: The configured concurrent stop action limit was reached.
// *Action: The stop action will automatically resume as soon as possible.
2852,3, "Conflicting specification of server pool and server."
// *Cause: Server pool name and server name were specified in a start command.
// *Action: Specify either server pool name or servername, not both.
2853,3, "Unknown server pool name: '%s' ."
// *Cause: The server pool name given to start/stop command did not exist.
// *Action: Specify a valid server pool name.
2854,3, "Resource '%s' cannot be started in a server pool because it is a local resource."
// *Cause: A local resource name was given to start/stop command.
// *Action: Specify a cluster resource name.
2855,3, "Resource '%s' is not configured to run in server pool '%s'."
// *Cause: An attempt was made to start or stop the resource in a server pool where resource was not configured to run.
// *Action: Modify resource's attribute to have this server pool or specify a different resource.
2856,3, "Unknown names for server pools or for filters. "
// *Cause:  An invalid value was  supplied for the '-s' or '-w' argument in a start/stop command or to the API calls. 
// *Action: Provide valid server pool names or filter attributes.
2857, 1, "Cannot stop resource '%s' because it is not running in server pool '%s'."
// *Cause: A resource stop request specified a server pool on which the resource is not running. 
// *Action: Check the current state of the resource; it should no
//          longer be running in that server pool.
2858, 1, "User '%s' does not have permission to run action '%s' on resource '%s'."
// *Cause: A username and/or group was specified for the action permissions, but the current user is not included in the specification.
// *Action: Use 'crsctl modify' to update the ACTIONS attribute for this resource to add the current user to the permission list for this action, or remove all user and group specifications to enable universal access.
2859, 1, "Cannot run action '%s' on resource '%s' because the resource is not online."
// *Cause: A resource action operation could not be performed because the resource was not online.
// *Action: Ensure the resource is online before attempting to run an action.
2860, 0, "Resource Action"
// *Document: NO
2861, 0, "Found no resources to run action on."
2862, 1, "Cannot update the ACTIONS attribute, because the input is not valid"
// *Cause: A resource update operation could not be performed, because the input value is not vvalid.
// *Action: Ensure the ACTIONS name attribute is specified in 32 or less US7ASCII characters. Ensure users and groups are prefixed with the appropriate identifier, either "user:" or "group:" 
2863, 1, "Cannot restart resource '%s' because it is not running."
// *Cause: A resource restart action was not performed because the resource is not running.
// *Action: Ensure that the resource which needs to be restarted is up and running. 
2864, 0, "Restart Resource"
// *Document: NO
2865, 1, "Resource '%s' cannot be started on server '%s' because it has an exclusion dependency with resources of type '%s'."
// *Cause: An exclusion dependency was configured without the right to preempt a running resource.
// *Action: Pick a different server or stop the other resource(s) on this server.
2866, 1, "Resource '%s' cannot be started on server '%s' because it has an exclusion dependency with resources of type '%s' and the force option was not specified."
// *Cause: An exclusion dependency was configured but the force option was not used to stop the running resource(s).
// *Action: Either pick a different server or use the force option.
2867, 1, "Server pool '%s' cannot be added to the policy set."
// *Cause: The Generic server pool as well as its sub-pools cannot be
// added to the policy set.
// *Action: Remove the pool from SERVER_POOL_NAMES attribute.
2868, 1, "'%s' is not a valid attribute of configuration policies."
// *Cause: An attempt was made to set a value for an attribute which does not belong to configuration policies.
// *Action: Use a valid attribute.
2869, 1, "'%s' is not a valid attribute of the policy set."
// *Cause: An attempt was made to set a value for an attribute which does not belong to the policy set.
// *Action: Use a valid attribute.
2870, 1, "An OCR write operation has failed during upgrade of the object schema."
// *Cause: While performing CRS upgrade as part of the clusterware upgrade, an OCR write operation has failed.
// *Action: Examine the clusterware alert log for more information about OCR failures.
2871, 1, "Resource '%s' cannot be started on server '%s' because it has an exclusion dependency with resource '%s'."
// *Cause: An exclusion dependency was configured between the two resources without the right to preempt a running resource.
// *Action: Pick a different server or stop the other resource on this server.
2872, 1, "Resource '%s' cannot be started on server '%s' because it has an exclusion dependency with resource '%s' and the force option is not used."
// *Cause: An exclusion dependency was configured between the two resources but the force option was not used to stop the running resource.
// *Action: Either pick a different server or use the force option.
2873, 0, "Cluster Ready Services Autostart"
// *Document: NO
2874, 1, "Could not restart resource '%s' on server '%s'."
// *Cause: A required part of restart operation has failed.
// *Action: Check the preceding errors to see the cause and take appropriate action.
2875, 1, "Failed to record shutdown information in OLR."
// *Cause: An attempt to record information during a normal shutdown failed. This will cause the shutdown to be regarded as unplanned on the next startup, and may lead to some driver resources being disabled.
// *Action: Use the ocrconfig and ocrcheck utilities to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2876, 1, "Disabled resource '%s' due to OHASD crashes"
// *Cause: OHASD crashes have exceeded the autostart thresholds set for this resource, and the resource has been disabled as a result.
// *Action: Use crsctl config to look up whether a resource has been disabled, and crsctl enable/disable to manually change the status.
2877, 1, "Owner '%s' of the entity '%s' does not belong to the '%s' group."
// *Cause:  The owner of an entity being configured was not a member of the required group.
// *Action: The user, issuing the command, needs to be configured to be in the group. 
2878, 1, "Failed to restart resource '%s'"
// *Cause: An attempt to start the resource has failed.
// *Action: If failover is not enabled, try manually starting the resource on a different server. If failover is enabled, the resource has been failed over, and any problems are reported in subsequent messages.
2879, 1, "Cannot update the ALERT_TEMPLATE attribute, because the input is not valid"
// *Cause: A resource update operation could not be performed, because the input value is not valid.
// *Action: Ensure that valid attributes are specified in a space separated list.
2880, 1, "Incorrect specification of dependency '%s', only one modifier may be specified."
// *Cause: During resource update, an exclusion dependency specified more than the maximum of one modifier.
// *Action: Check the specification of the dependency, fix the problem indicated,
//     and resubmit the request.
2881, 1, "Additional exclusion dependency discovered on resource '%s' within the same dependency tree."
// *Cause: During resource update, a dependency specified more than the maximum of one exclusion per hard dependency tree.
// *Action: Check the specification of the dependency, fix the problem indicated,
//     and resubmit the request.
2882, 1, "Unable to place an instance of resource '%s' due to an exclusion dependency on '%s'."
// *Cause:  The resource cannot be placed because of the constraints imposed 
//          by its start dependencies.
// *Action: Either change the resource start dependencies or re-evaluate the request.
2883, 1, "Resource '%s' failed during Clusterware stack start."
// *Cause: During Clusterware startup, automatic startup of the indicated resource 
//         succeeded but the resource failed before Clusterware startup completed.
// *Action: Retry starting Clusterware.
2884, 1, "Server '%s' cannot be used for resource placement currently."
// *Cause: The server is currently configured such that it cannot be
// used for resource placement.
// *Action: Use a different server.
2885, 0, "cannot stop the last server in Domain Service Cluster with active member cluster named '%s'"
// *Cause: An attempt to stop the last server in the Domain Service Cluster
//         was rejected because this cluster was still serving the indicated 
//         client cluster and perhaps other member clusters."
// *Action: Stop the active member clusters that use this Domain Service Cluster
//          first, or specify the '-f' option." 
2890, 1, "An administrator-managed database cannot be configured on a non-Hub server '%s'."
// *Cause: An attempt was made to register a database on a
// server whose role is not 'hub' or the node is currently down.
// *Action: Use only online servers configured as Hub servers.
2891, 1, "Policy-managed databases can only be configured in server pools that use '%s' category."
// *Cause: An attempt was made to configure a database using a server
// pool that does not currently use a category that includes only nodes with the specified role.
// *Action: Either use an existing server pool that uses such a category
// or create and use a server pool with such category.
2892, 1, "In order to use '%s' in resources of '%s' type, '%s' must be set to '%s' and '%s' must be set to '%s'."
// *Cause: An attempt was made to use an attribute such that other attributes must be set to specific values.
// *Action: Resubmit with the mentioned attributes set to the mentioned values.
2893, 1, "Cannot stop ASM instance on server '%s' because it is the only instance running."
// *Cause: An attempt was made to stop the last ASM instance in the cluster, which would lead to a complete cluster outage.
// *Action: Reissue the request when there are at least two ASM instances running in the cluster.
2894, 1, "Cannot stop the ASM resource because it will lead to a complete cluster outage."
// *Cause: An attempt was made to stop all ASM instances in the cluster, which would lead to a complete cluster outage.
// *Action: Reissue the request by specifying a concrete node name.
2895, 1, "DEGREE attribute is desupported."
// *Cause: An attempt was made to add a resource with DEGREE attribute.
// *Action: Remove the DEGREE attribute from the add command.
2900, 3, "User '%s' does not exist on node '%s'."
// *Cause : An attempt was made to add an unknown username to the CRS Administrator list. 
// *Action: Reissue the command with a known username. Or create the user on
//          the node(s) specified, and reissue the command.
2901, 1, "Not authorized to modify the CRS Administrator list."
// *Cause : An attempt was made to modify the CRS Administrator list by a user not
//          belonging to the CRS Administrator list.
// *Action: Either acquire the role of cluster administrator or have one modify
//          the CRS Administrator list for you.
2902, 0, "Add CRS Administrator"
// *Document: NO
2903, 0, "Delete CRS Administrator"
// *Document: NO
2904, 1, "Parameter '%s' for 'relocate' is not a singleton resource."
// *Cause:  A relocate request  specified a resource that is not singleton. 
// *Action: Specify a singleton resource or a filter that resolves to an
//          instance of  the resource. 
2905, 1, "Server pools in a policy do not have ACL attribute"
// *Cause:  A 'crsctl modify serverpool' command specified an ACL attribute with -policy or -all_policies.
// *Action: Omit ACL from the attributes.
2906, 1, "Server category '%s' cannot be unregistered as it is referenced by server pool '%s' in policy '%s'."
// *Cause:  The server category you are trying to remove has references to it in a policy.
// *Action: Make sure the server category you are trying to remove is not referenced by other entities in the policy.
2907, 1, "Resource '%s' is not completely configured, and hence cannot be operated upon."
// *Cause:  A request was made without specifying the PID_FILES or EXECUTABLE_NAMES.
// *Action: Specify a value for PID_FILES and/or EXECUTABLE_NAMES attribute, or specify
//          values for STOP_PROGRAM, CHECK_PROGRAM and CLEAN_PROGRAMS attributes.
// 2908 no longer used
2909, 1, "Server '%s' cannot be assigned to server pool '%s' because its current role is not '%s'."
// *Cause:  An attempt was made to assign a server to the server pool that did not have the specified role. 
//          Only servers with the specified role can be assigned to this server pool.
// *Action: Retry using a different server.
2910, 1, "Unable to register server category '%s' as this will affect running resources, but the force option was not specified."
// *Cause: One or more running resources were affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
// resources mentioned right before this error, or use the force option for the same command.
2911, 1, "Unable to modify server category '%s' as this will affect running resources, but the force option was not specified."
// *Cause: One or more running resources were affected by the operation.
// *Action: Add more servers to the cluster, stop or relocate the
// resources mentioned right before this error, or use the force option for the same command.
2912, 1, "Unable to start resource '%s' on server '%s' because resource dependencies require stopping it on a different server."
// *Cause:  A start request failed because resource dependencies would require stopping the
//          resource in order to start it somewhere else.  
// *Action: Manually stop the resource before starting it elsewhere.
2913, 1, "'autostart delay' value '%s' is invalid."
// *Cause:  The command specified an 'autostart delay' time that was non-numeric or negative.
// *Action: Specify a non-negative numeric value for the 'autostart delay' argument.
2914, 1, "'autostart servercount' value '%s' is invalid." 
// *Cause:  The command specified an 'autostart servercount' value that was non-numeric or negative.
// *Action: Specify a positive numeric value for the 'autostart servercount' argument.
2915, 2, "Failed to update 'autostart delay' (%s) or 'autostart servercount' (%s). Details at %s in %s."
// *Cause:  A request to update the automatic start details failed because of incorrect input values.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
2916, 0, "Set 'CRS Autostart'"
// *Document: NO
2917, 1, "The '%s' server pool cannot be removed from the system."
// *Cause:  The command to remove the server pool from the policy set
// would have caused it to be removed from the system completely.
// *Action: Reissue the 'crsctl modify policyset' command with the -ksp option.
2918, 1, "Authorization failure: operating system group '%s' does not exist on server '%s' "
// *Cause: The specified operating system group does not exist on the specified server. Cluster Ready Services requires that all groups used by the resources it manages exist on each server of the cluster.
// *Action: Add the specified operating system group on the specified server.
2919, 1, "Resource '%s' has no instances to act upon."
// *Cause: An attempt was made to act on a resource that has no
// resource instances because it is configured to run on servers that
// have never existed in the cluster.
// *Action: Retry the command when the resource has instances.
2920, 1, "Unable to activate policy '%s' because this will affect running resources, but the force option was not specified."
// *Cause: An attempt to activate a new policy would have affected one or more running resources but the force option was not specified.
// *Action: Reevaluate the request and if it makes sense, set the force option and
//          resubmit.
2921, 1, "Unable to register policy because attribute '%s' for resource '%s' does not have the POLICY_CONFIG flag."
// *Cause: An attempt was made to specify resource attributes in the policy that do not have the POLICY_CONFIG flag.
// *Action: Only attributes that can be policy managed and have the POLICY_CONFIG flag can be specified in a policy definition.
2922,    1, "The attribute '%s' is not supported for resource type '%s'." 
// *Cause: An attempt to update a CRS resource specified an attribute that is not associated with the resource type.
// *Action: Specify only attributes that are associated with the type of resource being updated.
2923, 1, "The EXPRESSION attribute cannot accept '%s' as a server configuration attribute."
// *Cause: An attempt was made to set a server configuration attribute that cannot be used with the EXPRESSION attribute.
// *Action: Use a valid attribute.
2924, 1, "The EXPRESSION attribute contains invalid value '%s' for server configuration attribute '%s'."
// *Cause: An attempt was made to set a value which cannot be assigned to a server configuration attribute.
// *Action: Use a valid value.
2925, 1, "The dependency modification '%s' for the targets '%s' has an unknown dependency or incorrect syntax."
// *Cause: An attempt was made to modify an existing dependency without providing a known dependency or the correct modification syntax.
// *Action: Refer to the Oracle Clusterware documentation for an explanation of supported dependencies and the resource dependency modification syntax.
2926, 1, "Cannot find a match for target '%s' in the modification list for dependency '%s'."
// *Cause: There was no existing dependency that had the same target to be modified.
// *Action: Supply the correct target for the dependency modification.
2927, 1, "The requested action for the resource '%s' was aborted due to a timeout."
// *Cause: The timeout specified for a custom action was reached before the action could complete.
// *Action: Revise the timeout setting and retry the action.
2928, 1, "The dependency on type '%s' cannot be accepted because it is specified multiple times."
// *Cause:  A duplicate type was assigned as a dependency to a resource.
// *Action: Revise the dependency list to ensure that no duplicate types exist.
2929, 1, "The dependency on resource '%s' cannot be accepted because it is specified multiple times."
// *Cause:  A duplicate resource was assigned as a dependency to a resource.
// *Action: Revise the dependency list to ensure that no duplicate resources exist.
2930, 1, "The server category '%s' cannot be deleted because it is still a dependency for one or more resources."
// *Cause: An attempt was made to delete a server category that was still a dependency for one or more resources.
// *Action: Either modify the dependency attributes of the associated resources or delete those resources and try again.
2931, 1, "Server category '%s' used in dependency '%s' does not exist or is not registered."
// *Cause: An attempt was made for the current resource to have a dependency on a server category that does not exist.
// *Action: Check the specification of the dependency, fix the problem indicated, and resubmit the request.
2932, 1, "The dependency on server category '%s' is not supported for a resource type."
// *Cause: An attempt to specify a server category dependency for a resource type failed because server category dependency is only supported for a resource.
// *Action: Omit the server category dependency.
2933, 1, "The server category name for the relation '%s' is missing."
// *Cause: The server category name was expected for the resource dependency, but it was not supplied.
// *Action: Provide the server category name when resubmitting the request.
2934, 1, "Value '%s' is neither '%s' nor '%s'"
2935, 1, "The value can be either '%s' or '%s'."
// *Document: NO
2936, 1, "The user manually disabled HAIP."
// *Document: NO
2937, 3, "Resource group '%s' has been registered."
// *Document: NO
2938, 3, "Resource '%s' has been modified."
// *Document: NO
2939, 3, "Resource group '%s' has been modified."
// *Document: NO
2940, 3, "Resource '%s' has been unregistered."
// *Document: NO
2941, 3, "Resource group '%s' has been unregistered."
// *Document: NO
2942, 3, "Resource '%s' has been registered."
// *Document: NO
2943, 3, "Server pool '%s' has been registered."
// *Document: NO
2944, 3, "Server pool '%s' has been modified."
// *Document: NO
2945, 3, "Server pool '%s' has been unregistered."
// *Document: NO
2946, 3, "beginning to auto-start resources on server '%s'"
// *Document: NO
2947, 3, "Configuration policy set has been modified."
// *Document: NO
2948, 3, "detected unplanned state change of resource '%s' from state '%s' to '%s'"
// *Document: NO
2949, 1, "The dispersion dependency '%s' is specified with mutliple modifiers."
// *Cause: An attempt to specify the dispersion dependency failed because multiple modifiers were specified where at most one is supported.
// *Action: Check the specification of the dependency, fix the problem indicated, and resubmit the request.

2961, 1, "Consistency problem in registry while processing category '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2962, 1, "Consistency problem in registry while processing server pool '%s'. Details at %s in %s."
// *Cause: This is an internal error.
// *Action: Contact Oracle Support Services.
2963, 3, "Consistency check for all entities managed by the Cluster Ready Services has completed successfully."
// *Cause: None.
// *Action: None.
/
2964, 1, "cannot run resource '%(1)s' on server '%(2)s' because the server needs an additional %(3)d MB of memory"
// *Cause: An attempt to start a resource on a server failed because the server
//         needed the indicated additional memory to satisfy the memory
//         requirements of the resource.
// *Action: Change the placement policy of the resource to expand the server
//          selections, change the memory requirement of the resource, or add
//          more memory to the server to which the resource is directly
//          assigned.
/
2965, 1, "cannot run resource '%(1)s' on server '%(2)s' because the server needs %(3)d additional CPUs"
// *Cause: An attempt to start a resource on a server failed because the server
//         needed additional CPUs to satisfy the CPU requirement of the
//         resource.
// *Action: Change the placement policy of the resource to expand the server
//          selections, change the CPU requirement of the resource, or add more
//          CPUs to the server to which the resource is directly assigned.
/
2966, 1, "There are no servers satisfying the placement policy for resource '%s'."
// *Cause: An attempt to start a resource on servers that were available
//         according to the placement policy failed because none of those
//         servers could satisfy the requirements of the resource.
// *Action: Change the placement policy of the resource to expand the server
//          selections, change the requirements of the resource, or upgrade the
//          configurations of the eliminated servers.
/
2967, 1, "Resource instance '%s' is unable to start because it is scheduled for deletion."
// *Cause: An online relocate attempt on this resource failed to stop the specified 
//         resource instance. The resource instance is scheduled for deletion when
//         it stops.
// *Action: Use 'crsctl stop resource' to stop the resource instance manually.
/
2968, 3,  "authorization failure updating attribute '%s'"
// *Cause: Write access permission was not granted to this user to modify the attribute.
// *Action: Either omit the attribute, or issue the command from an operating system 
//          user who has the required permission.
2969, 1, "cannot add resource '%s' because a resource group exists with the same name"
// *Cause: An attempt to add a resource failed because a resource group with
//         the same name was already registered.
// *Action: Reissue the command specifying a different name for the new resource.
/
2970, 1, "Value '%s' is invalid, must be one of: '%s', '%s', '%s', or '%s'."
// *Cause: An attempt to change an attribute value of a resource was rejected because the indicated value was specified, when it must have been one of the other values indicated in the message.
// *Action: Retry modifying the resource attribute value specifying one of the allowed values as shown in the error message.
/
2971, 1, "cannot run resource ora.asm on server '%s' on quarantined site '%s'"
// *Cause: An attempt to run resource ora.asm on the indicated server was
//         rejected because that server was in the indicated site, which was 
//         quarantined so that no ASM client or instance could be run there.
// *Action: Unquarantine the site before attempting to run the resource.
/
2972, 1, "There are no servers satisfying the CPU and memory requirements for resource '%s'."
// *Cause: An attempt to start the indicated resource failed because there were
//         no servers available that meet the CPU-count and memory
//         requirements of that resource.
// *Action: If possible, change the CPU or memory requirements of the resource
//          or add more CPUs or memory to the servers in the cluster.
/
2973, 1, "The CPU count '%d' exceeds the maximum value of '%d'."
// *Cause: An attempt to modify a resource failed because the specified
//         CPU count exceeded the maximum value indicated in the message.
// *Action: Retry modifying the resource attribute value specifying a value
//          less than the maximum value as shown in the message.
/
2974, 1, "unable to act on resource '%(1)s' on server '%(2)s' because that would require stopping or relocating resource '%(3)s' but the -force option was not specified"
// *Cause:  The attempted operation on the indicated resource and server 
//          was rejected because it would have required stopping or relocating 
//          the additional resource as shown. The -force option would 
//          have been required to allow the additional effects.
// *Action: Reevaluate the request and, if appropriate, specify the -force 
//          option and resubmit.
2975, 1, "duplicate attempt to complete Transparent HA for resource '%s' rejected" 
// *Cause:  An attempt to end the transparent High Availability (HA) 
//          action on the indicated resource instance was rejected because 
//          the same action was already pending on that resource instance."
// *Action: None
2976, 1, "The workload maximum memory '%(1)d' MB exceeds the available memory size of '%(2)d' MB."
// *Cause: An attempt to modify a resource failed because the specified
//         workload maximum memory exceeded the available value indicated in
//         the message.
// *Action: Retry modifying the resource attribute value specifying a value
//          less than or equal to the available value as shown in the message.
2977, 1, "The specified value '%(1)d' exceeds the available CPU capacity on node '%(2)s"
// *Cause:  An attempt to modify the attribute WORKLOAD_CPU_CAP was rejected  
//          because the new value would have caused the total CPU utilization 
//          to exceed 100% on the node given in the message.
// *Action: Check the CPU utilization on the mentioned node and re-issue the
//          modify command with an appropriate value.




//////////////////////////////////////////////////////////////
/
/
/   3501-3999: Cluster Health Analysis Service specific messages.
/
//////////////////////////////////////////////////////////////

3501, 0, "The Cluster Health Analysis service started on host %s."
// *Cause: The Cluster Health Analysis service was successfully started on the
//         listed node.
// *Action: None.
/
3502, 0, "The Cluster Health Analysis service aborted on host %s. Details at %s in %s."
// *Cause:  The Cluster Health Analysis service aborted due to an internal
//          error.
// *Action: Determine whether the Cluster Health Analysis service has
//          automatically restarted by checking the Oracle Clusterware alert 
//          log. If the problem persists, contact Oracle Support Services.
/
3503, 0, "The Cluster Health Analysis service on host %s is shutting down."
// *Cause: The Cluster Health Analysis service on the listed node was
//         terminated.
// *Action: None.
/

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
4040, 1, "The value of attribute '%s' contains the following invalid characters: '%s'"
// *Cause: An attribute value with invalid characters was specified.
// *Action: Reissue the command and provide valid characters for the attribute value.
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
/ Status or Stat Usage - 4048 - 4049, 4061 - 4069, 4819 - 4821
/
4048, 3, "  crsctl status serverpool [<spName>[...]|-w <filter>] [-p|-v|-f]\n     Check status of designated server pools\n\n  crsctl status serverpool {<spName>[...]} -g\n     Check status of designated server pools"
4049, 3, "\nwhere \n     spName [...]      One or more blank-separated server pool names\n     -w                Server pool filter (e.g., \"MIN_SIZE > 3\")\n     -g                Check if server pools are registered\n     -p                Print static configuration\n     -v                Print runtime configuration\n     -f                Print full configuration"


/////////////////////////////////////////////////
/ Used by any crsctl command
/////////////////////////////////////////////////
4050, 2, "Rejecting the command because the cluster active version [%s] is less than the required cluster active version [%s]"
// *Cause:  The command was rejected because the cluster active version was 
//          less than the required cluster active version.
// *Action: Reissue the command with a valid cluster active version.

/
/ Modify 4051 - 4056, 4070, 4818
/
// Msg 4051 consists of msg 4051 and msg 4818.
4051, 3, "  crsctl modify {resource|type|resourcegroup|resourcegrouptype|serverpool|policy|policyset} <name> <options> \nwhere \n    name         Name of the CRS entity \n    options      Options to be passed to the modify command\n\n    See individual CRS entity help for more details"
4052, 3, "  crsctl modify {resource|type|resourcegroup|resourcegrouptype|serverpool|policy|policyset} <name> <options>\n  crsctl modify wallet <options>\n  crsctl modify cluster site <options>"
4053, 3, "  crsctl modify resource <resName> -attr \"<specification>[,...]\" [-f] [-delete] [-i] [-group <resourceGroupName>] [-env \"env1=val1,env2=val2,...\"]\n     <specification>:   {<attrName>=<value> | <attrName>@<scope>=<value>}\n        <scope>:   {@SERVERNAME(<server>)[@DEGREEID(<did>)] |\n                       @CARDINALITYID(<cid>)[@DEGREEID(<did>)] }\nwhere"
// Msg 4054 continued in msg 6540
4054, 3, "     resName            Modify named resource\n     attrName           Attribute name\n     value              Attribute value\n     server             Server name\n     cid                Resource cardinality ID\n     did                Resource degree ID\n     -f                 Force option\n     -delete            Delete named attribute\n"
// Msg 4055 consists of msgs 4055, 4835 and 4836
4055, 3, "  crsctl modify type <typeName> -attr \"ATTRIBUTE=<attrName>[,TYPE={string|int}][,DEFAULT_VALUE=<defaultValue>][,FLAGS=typeFlags][,...]\" [-f] [-i]\nwhere"
4056, 3, "  crsctl modify serverpool <spName> -attr \"<attrName>=<value>[,...]\" [-policy <policyName> | -all_policies] [-f] [-i]"

/
/ Relocate 4057 - 4060
/
4057, 3, "  crsctl relocate {resource|server} <name> <options>"
4058, 3, "  crsctl relocate resource {<resName> [-k <cid>]| -all|-w <filter>} -s <server> [-n <server>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]\n     Relocate designated resources"
// Msg 4059 continued in msg 6541
4059, 3, "\nwhere\n     resName        Resource named resource\n     -all           Relocate all resources\n     -s             Source server\n     -w             Resource filter (e.g., \"TYPE = ora.database.type\")\n     -n             Destination server\n     -k             Cardinality ID\n     -env           Attribute overrides for this command\n"
4060, 3, "  crsctl relocate server <server> [...] -c <spName> [-f] [-i]\n     Relocate designated servers\nwhere \n     server [...]   One or more blank-separated server names\n     -c             Destination server pool name\n     -f             Force option\n     -i             Fail if request cannot be processed immediately"

/
/ Status or Stat Usage - 4048 - 4050, 4061 - 4069, 4819 - 4821
/
4061, 3, "  crsctl status {resource|resourcegroup|type|resourcegrouptype|serverpool|server} [<name>|-w <filter>] [-g] \nwhere \n    name   CRS entity name\n    -w     CRS entity filter\n    -g     Check if CRS entities are registered"
// Msg 4062 consists of msg 4062 and msg 4819.
4062, 3, "  crsctl status type [<typeName>[...]]|-w <filter>] [-p|-f|-g|-r]\n     Check status of designated resource types\nwhere \n     typeName [...]    One or more blank-separated resource type names"

// Msg 4063 consists of msgs 4063, 4064, 4065 and 4820.
4063, 3, "  crsctl status resource [<resName>[...]|-w <filter>] [-p [-attr <attribName>[,...] [-noname]] |-v [-attr <attribName>[,...] [-noname]]] | [-f|-l|-g] | [[-k <cid>|-n <server>] [-e [-p|-v]] [-d <did>]] | [-s -k <cid> [-d <did>]]\n     Check status of designated resources\n\n  crsctl status resource [<resName>[...]|-w <filter>] -t"

// Msg 4064 continued in msg 6542
4064, 3, "     Print status of resources in tabular format\n\n  crsctl status resource [<resName>[...]] -dependency [-stop | -pullup]\n    Print resource dependencies\nwhere \n     resName [...]     One or more blank-separated resource names\n     -w                Resource filter (e.g., \"TYPE = ora.database.type\")\n"

4065, 3, "     -attr             Print specific attributes\n     -noname           Bypass the default printing of the resource name\n     -e                Evaluate a resource instance's special values\n     -f                Print full configuration\n     -l                Print all cardinal and degree members"


// Msg 4066 consists of msgs 4066 and 4821.
4066, 3, "  crsctl status server {[<server>[...] [-g] ] | [-category <categoryName>] | [-w <filter>]} [-p|-v|-f] \n     Check status of designated servers\nwhere \n     server [...]      One or more blank-separated server names\n     categoryName      Category name to match servers for"

4067, 3, "  crsctl status <resource|type|serverpool|server> [<name>] [options]\n  crsctl status <ip|testdns> <options>"
4068, 3, "  crsctl status ip -A {<IP_name>|<IP_address>}\n     Check if the IP is alive\nWhere\n     IP_name        Name which resolves to an IP. If name is not fully qualified domain name then standard name search will be used.\n     IP_address     IP address\n" 
4069, 3, "  crsctl status testdns [-address <IP_address>] [-port <port>] [-v]\n     Check status of DNS server for specified domain\nWhere\n     IP_address          DNS server address (defaults to hostname)\n     port                The port on which the DNS server is listening. Default value for the port is 53.\n     -v                  Verbose output"

/
/ Modify 4051 - 4056, 4070, 4818
/
// Msg 4070 continued in msg 6543
4070, 3, "  crsctl modify wallet -type <wallet_type> [-name <name>] -user <user_name> -passwd\n     Modify the password for the designated user\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER, APPQOSDB, MGMTDB, OSUSER or CVUDB.\n     name            Name is required for APPQOSDB and CVUDB wallets.\n"

/
/ Add 4071 - 4080, 4822 - 4826
/
// Msg 4071 continued in msg 6544
4071, 3, "  crsctl add {resource|type|resourcegroup|resourcegrouptype|serverpool|policy} <name> <options> \nwhere \n   name          Name of the CRS entity \n   options       Options to be passed to the add command\n\n   See individual CRS entity help for more details\n\n  crsctl add crs administrator -u <user_name> [-f] \nwhere  "
// Msg 4072 continued in msg 6545
4072, 3, "  crsctl add wallet -type <wallet_type> <options>\nwhere \n   wallet_type   Type of wallet i.e. APPQOS, APPQOSUSER, APPQOSDB, MGMTDB, OSUSER or CVUDB.\n   options       Options to be passed to the add command\n\n "
4073, 3, "  crsctl add {resource|type|resourcegroup|resourcegrouptype|serverpool|policy} <name> <options> \n  crsctl add crs administrator -u <user_name> [-f]\n  crsctl add wallet -type <type_name> <options>\n crsctl add credentials -target <target> <options>\n  crsctl add cluster site <site_name> <options>"
// Msg 4074 consists of msgs 4074, 4075, 4822 and 4823
4074, 3, "  crsctl add resource <resName> -type <typeName> [[-file <filePath>] | [-attr \"<specification>[,...]\"]] [-f] [-i] [-group <resourceGroupName>]\n     <specification>:   {<attrName>=<value> | <attrName>@<scope>=<value>}"
4075, 3, "        <scope>:   {@SERVERNAME(<server>)[@DEGREEID(<did>)] |\n                       @CARDINALITYID(<cid>)[@DEGREEID(<did>)] }\nwhere"
// Msg 4076 consists of msgs 4076, 4824 and 4834
4076, 3, "  crsctl add type <typeName> -basetype <baseTypeName> {-file <filePath> | -attr \"ATTRIBUTE=<attrName>,TYPE={string|int}[,DEFAULT_VALUE=<defaultValue>][,FLAGS=typeFlags][,...]\" } [-i]\nwhere"
// Msg 4077 consists of msgs 4077 and 4825
4077, 3, "  crsctl add serverpool <spName> [[-file <filePath>] | [-attr \"<attrName>=<value>[,...]\"]] [-i] [-f]\nwhere \n     spName          Add named server pool\n     filePath        Attribute file"
4078, 3, "  crsctl add crs administrator -u <user_name> [-f]\nwhere \n    user_name    User name to be added to the admin list or \"*\"\n    -f           Override user name validity check"
4079, 3, "  crsctl add css votedisk <vdisk>[...] [-purge]\nwhere\n    vdisk [...]     One or more blank-separated voting file paths\n   -purge           Purge option"
// Msg 4080 consists of msgs 4080 and 4826
4080, 3, "  crsctl add wallet -type <wallet_type> [-name <name>] [-user <user_name> -passwd]\n     Create the designated wallet and add user to it\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER, APPQOSDB, MGMTDB, OSUSER or CVUDB."

/
/ Check 4081 - 4085, 4180 - 4184
/
4081, 3, "  crsctl check has\n     Check status of OHAS"
4082, 3, "  crsctl check crs\n     Check status of OHAS and CRS stack" 
4083, 3, "  crsctl check cluster [[-all]|[-n <server>[...]]]\n     Check status of CRS stack"
4084, 3, "  crsctl check cluster [-all|-n <server>[...]]\n    Check status of CRS stack\nwhere \n    Default          Check local server\n    -all             Check all servers\n    -n               Check named servers\n    server [...]    One or more blank-separated server names"
4085, 3, "  crsctl check resource {<resName> [...]|-w <filter>} [-n <server>] [-k <cid>] [-d <did>]\n     Check status of resources"

/
/ Delete 4086 - 4095
/
4086, 3, "  crsctl delete {resource|type|resourcegroup|resourcegrouptype|serverpool|node|policy} <name> [...] [<options>] \n  crsctl delete crs administrator -u <user_name> [-f]\n  crsctl delete wallet -type <wallet_type> <options>\n  crsctl delete css votedisk <options>\n  crsctl delete credentials <options>\n  crsctl delete cluster site <site_name>"
4087, 3, "  crsctl delete resource {<resName> [...]|-w <filter>} [-f] [-i]\nwhere \n    resName [...]  One or more resource names to be deleted\n    -w             Resource filter (e.g., \"TYPE = ora.database.type\")\n    -f             Force option\n    -i             Fail if request cannot be processed immediately"
4088, 3, "  crsctl delete type {<typeName> [...]|-w <filter>} [-i]\nwhere \n    typeName [...]  One or more blank-separated resource type names\n    -w              Type filter (e.g., \"TYPE_NAME = test_type\")\n    -i              Fail if request cannot be processed immediately"
4089, 3, "  crsctl delete serverpool {<spName> [...]|-w <filter>} [-i]\nwhere \n    spName [...]    One or more server pool names to be deleted\n    -w              Serverpool filter (e.g., \"NAME = pool1\")\n    -i              Fail if request cannot be processed immediately"
4090, 3, "  crsctl delete crs administrator -u <user_name> [-f]\nwhere \n    user_name       User name to be deleted from the admin list or \"*\"\n    -f              Override user name validity check"
4091, 3, "  crsctl delete wallet -type <wallet_type> [-name <name>] [-user <user_name>]\n     Delete the designated wallet or user from wallet\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER, APPQOSDB, MGMTDB, OSUSER or CVUDB.\n     name            Name is required for APPQOSDB and CVUDB wallets.\n     user_name       User to be deleted from wallet."
4092, 3, "  crsctl delete css votedisk +<diskgroup>\nwhere\n diskgroup           The name of a diskgroup containing voting files;\n                     allowed only when clusterware is in exclusive mode"
4093, 3, "  crsctl delete node -n <nodename>\nwhere\n    nodename     Node to be deleted"
4094, 3, "  crsctl delete credentials -target <target> [-path <path>] [-id <ID>] [-local]\nwhere \n    target    Target listed by 'crsctl query credentials targetlist'\n    path      Path, relative to the target, of a credentials domain\n    ID        Credential member ID to delete\n    -local    Delete credential information from OLR rather than OCR"

/
/ Getperm 4096 - 4105
/
4096, 3, "  crsctl getperm {resource|type|serverpool|category|policyset} <name> [-u <user_name>|-g <group_name>]"
4097, 3, "  crsctl getperm resource <resName> [-u <user_name>|-g <group_name>]\nwhere \n    resName    Get permissions for named resource\n    -u         Get permissions for user name\n    -g         Get permissions for group name"
4098, 3, "  crsctl getperm type <typeName> [-u <user_name>|-g <group_name>]\nwhere \n    typeName   Get permissions for named resource type\n    -u         Get permissions for user name\n    -g         Get permissions for group name"
4099, 3, "  crsctl getperm serverpool <spName> [-u <user_name>|-g <group_name>]\nwhere \n    spName     Get permissions for named server pool\n    -u         Get permissions for user name\n    -g         Get permissions for group name"
4100, 0, "No permission found for user '%s'"
4101, 0, "No permission found for group '%s'"
4102, 3, "  crsctl getperm category <categoryName> [-u <user_name>|-g <group_name>]\nwhere \n    categoryName     Get permissions for named server category\n    -u               Get permissions for user name\n    -g               Get permissions for group name"

4103, 3, "  crsctl getperm policyset [-u <user_name>|-g <group_name>]\n    -u         Get permissions for user name\n    -g         Get permissions for group name"
/
/ Setperm 4106 - 4115
/

4106, 3, "  crsctl setperm {resource|type|serverpool|category|policyset} <name> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere \n     -u           Update entity ACL\n     -x           Delete entity ACL\n     -o           Change entity owner\n     -g           Change entity primary group"
4107, 3, "  crsctl setperm {resource|type|serverpool|category|policyset} <name> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}"
4108, 3, "  crsctl setperm resource <resName> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update resource ACL\n     -x           Delete resource ACL\n     -o           Change resource owner\n     -g           Change resource primary group"
4109, 3, "  crsctl setperm type <typeName> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update resource type ACL\n     -x           Delete resource type ACL\n     -o           Change resource type owner\n     -g           Change resource type primary group"
4110, 3, "  crsctl setperm serverpool <spName> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update server pool ACL\n     -x           Delete server pool ACL\n     -o           Change server pool owner\n     -g           Change server pool primary group"
// Msg 4111 consists of msgs 4111 and 4112
4111, 3, "\n\n   ACL (Access Control List) string:\n\n   { user:<user_name>[:<readPerm><writePerm><execPerm>]   |\n     group:<group_name>[:<readPerm><writePerm><execPerm>] |\n     other[::<readPerm><writePerm><execPerm>] }\nwhere\n   user         User ACL\n   group        Group ACL\n   other        Other ACL"
4112, 3, "   readPerm     Read permission (\"r\" grants, \"-\" forbids)\n   writePerm    Write permission (\"w\" grants, \"-\" forbids)\n   execPerm     Execute permission (\"x\" grants, \"-\" forbids)"
4113, 3, "  crsctl setperm category  <categoryName> {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update server category ACL\n     -x           Delete server category ACL\n     -o           Change server category owner\n     -g           Change server category primary group"
4114, 3, "  crsctl setperm policyset {-u <aclstring>|-x <aclstring>|-o <user_name>|-g <group_name>}\nwhere\n     -u           Update policyset ACL\n     -x           Delete policyset ACL\n     -o           Change policyset owner\n     -g           Change policyset primary group"
/
/ Start 4116 - 4125, 4827, 6701 - 6720
/
// Msg 4116 consists of msgs 4116, 4117, 4827, 4120, 4125,6507 and 4811 OR
//                      msgs 4116, 4117, 4827, 4119, 4122, 4125, 4811 and 6701
4116, 3, "  crsctl start resource {<resName> [...]|-w <filter>]|-all} [-n <server> | -s <server_pools>] [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-begin|-end] [-f] [-i] [-l] \n     Start designated resources\nwhere"
4117, 3, "     resName [...]    One or more blank-separated resource names\n     -w               Resource filter (e.g., \"TYPE = ora.database.type\")\n     -all             All resources\n     -n               Server name\n     -k               Resource cardinality ID"
// Msg 4118 consists of msgs 4118, 4120, 4125 and 4811 OR
//                      msgs 4118, 4119, 4121, 4125 and 4811
4118, 3, "  crsctl start resource {<resName> [...]|-w <filter>]|-all} [-n <server>| -s <server_pools>] [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-begin|-end] [-f] [-i] [-l]"
//4119 is 4119 plus 4952
// Msg 4119 continued in msg 6546
4119, 3, "  crsctl start crs [-excl [-nocrs | -cssonly]] | [-wait | -waithas | -nowait] | [-noautostart]\n     Start OHAS on this server\nwhere\n     -excl        Start Oracle Clusterware in exclusive mode\n     -nocrs       Start Oracle Clusterware in exclusive mode without starting CRS\n     -nowait      Do not wait for OHAS to start\n"
4120, 3, "  crsctl start has [-nowait] [-noautostart]\n     Start Oracle High Availability Services on this server\nwhere\n     -nowait      Do not wait for Oracle High Availability Services to start.\n     -noautostart Start only Oracle High Availability Services."
4121, 3, "  crsctl start cluster [[-all] | [-n <server>[...]] | -hub | -leaf | -w <filter>]"
// Msg 4122 continued in msg 6547
4122, 3, "  crsctl start cluster [[-all] | [-n <server>[...]] | -hub | -leaf | -w <filter>]\n    Start CRS stack\nwhere\n    Default         Start local server\n    -all            Start all servers\n    -n              Start named servers\n    server [...]    One or more blank-separated server names\n    -hub            Start hub nodes\n"
4123, 0, "Oracle High Availability Services has been started."
4124, 0, "Oracle High Availability Services startup failed."
4125, 3, "  crsctl start ip -A {<IP_name>|<IP_address>}/<net_mask>/<interface_name>\n    Start an IP on the given interface with specified net mask\nWhere\n    IP_name              Name which resolves to an IP. If it is not a fully qualified domain name then standard name search will be used.\n    IP_address           IP address\n" 

/
/ Stop 4126 - 4135, 6721 - 6740
/
4126, 3, "  crsctl stop resource {<resName>[...]|-w <filter>|-all} [-n <server> | -s <server_pools>] [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-begin|-end] [-f] [-i] [-l] \n     Stop designated resources\nwhere"
// Msg 4127 continued in msg 6548
4127, 3, "     resName [...]    One or more blank-separated resource names\n     -w               Resource filter (e.g., \"TYPE = ora.database.type\")\n     -all             All resources\n     -n               Server name\n     -k               Resource cardinality ID\n     -d               Resource degree ID\n"
4128, 3, "  crsctl stop resource {<resName>[...]|-w <filter>|-all} [-k <cid>] [-d <did>] [-n <server>] [-env \"ENV1=val1,ENV2=val2,...\"] [-begin|-end] [-f] [-i] [-l]"
4129, 3, "  crsctl stop crs [-f]\n    Stop OHAS on this server\nwhere\n    -f              Force option"
4130, 3, "  crsctl stop has [-f]\n    Stop OHAS on this server\nwhere\n    -f              Force option"
4131, 3, "  crsctl stop cluster [[-all] | [-n <server>[...]] | -hub | -leaf | -w <filter>] [-f]"
// Msg 4132 continued in msg 6549
4132, 3, "  crsctl stop cluster [[-all] | [-n <server>[...]] | -hub | -leaf | -w <filter>] [-f]\n    Stop CRS stack\nwhere\n    Default         Stop local server\n    -all            Stop all servers\n    -n              Stop named servers\n    server [...]    One or more blank-separated server names\n    -hub            Stop hub nodes\n"
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
/ Debug 4151 - 4157
/
4151, 3, "DEPRECATED: use crsctl set log {css|crs|evm}"
4152, 3, "DEPRECATED: use crsctl set trace {css|crs|evm}"
4153, 3, "DEPRECATED: use crsctl set log res"
4157, 3, "  crsctl debug statedump {crs|css|evm}\n where\n   crs           Cluster Ready Services\n   css           Cluster Synchronization Services\n   evm           Event Manager"
/
/ Export 4158 - 4164
/
4158, 3, "  crsctl export resourcegroup <rgName> -file <importScript>\nwhere\n     rgName        Resource group to export\n     importScript  Perl import script file name"
4159, 3, "  crsctl export resourcegroup <rgName> -file <importScript>"
4165, 0, "%s Error: %s"
    

/
/ Config 4166 - 4169
/
4166, 3, "This message reserved for crsctl config cluster online help"
4167, 3, "This message reserved for crsctl config cluster online help"
4168, 3, "  crsctl config has\n     Display OHAS autostart config on this server"
4169, 3, "  crsctl config crs\n     Display OHAS autostart config on this server"

/
/ Query 4170 - 4178. Continued 6741 - 6760, 41001 - 42000
/
4170, 3, "  crsctl query crs softwareversion [<nodename>| -all]\n     Lists the version of Oracle Clusterware software installed\nwhere\n     Default         List software version of the local node\n     nodename        List software version of named node\n     -all            List software version for all the nodes in the cluster"
4171, 3, "  crsctl query crs administrator\n     Display admin list"
4172, 3, "  crsctl query crs activeversion [-f]\n     Lists the Oracle Clusterware active version\nwhere\n     -f              List the cluster state and active patch level"
4173, 3, "  crsctl query crs releaseversion\n     Lists the Oracle Clusterware release version"
4174, 3, "  crsctl query crs softwareversion [<nodename>]\n     Lists the version of Oracle Clusterware software installed\nwhere\n     Default         List software version of the local node\n     nodename        List software version of named node"
4175, 3, "  crsctl query css ipmidevice\n     Checks whether the IPMI device/driver is present"
4176, 3, "  crsctl query css votedisk\n     Lists the voting files used by Cluster Synchronization Services"
// Msg 4177 continued in msg 6550
4177, 3, "  crsctl query wallet -type <wallet_type> [-name <name>] [-user <user_name> | -all]\n     Check if the designated wallet or user exists\nwhere\n     wallet_type     Type of wallet i.e. APPQOSADMIN, APPQOSUSER, APPQOSDB, MGMTDB, OSUSER or CVUDB.\n     name            Name is required for APPQOSDB and CVUDB wallets.\n"
4178, 3, "  crsctl query css ipmiconfig\n     Checks whether Oracle Clusterware has been configured for IPMI"

/
/ Help message for filters
/
/split the filter help msg (# 4179) into two to restrict it to 400 chars.
/ see msg # 4270
4179, 1, "Sample filters:\n1. TYPE = type1\n2. ((TYPE = type1) AND (CHECK_INTERVAL > 50))\n3. (TYPE = type1) AND ((CHECK_INTERVAL > 30) OR (AUTO_START co never))"

/
/ Overflow help messages
/
4180, 3, "  crsctl check install"
4181, 3, "  crsctl check css\n     Check status of Cluster Synchronization Services"
4182, 3, "  crsctl check ctss\n    Check status of Cluster Time Synchronization Services"
4183, 3, "  crsctl check evm\n     Check status of Event Manager"
// Msg 4184 continued in msg 6551
4184, 3, "  crsctl check resource {<resName> [...]|-w <filter>} [-n <server>] [-k <cid>] [-d <did>]\n     Check status of resources\nwhere \n     resName [...]    One or more blank-separated resource names\n     -w               Resource filter (e.g., \"TYPE = ora.database.type\")\n     -n               Server name\n"
4185, 3, "  crsctl get css <parameter>\n    Displays the value of a Cluster Synchronization Services parameter\n\n    clusterguid\n    diagwait\n    disktimeout\n    misscount\n    reboottime\n    noautorestart\n    priority"
4186, 3, "  crsctl get css ipmiaddr\n    Displays the IP address of the local IPMI device as set in the Oracle registry."
4187, 3, "  crsctl get hostname\n    Displays the host name"
4188, 3, "  crsctl get nodename\n    Displays the node name"
4189, 3, "  crsctl get {css <parameter>|hostname|nodename}"
4190, 3, "  crsctl set css <parameter> <value>\n    Sets the value of a Oracle Cluster Synchronization Services parameter\n\n    diagwait\n    disktimeout\n    misscount\n    reboottime\n    noautorestart\n    priority"
4191, 3, "  crsctl set css ipmiaddr <ipmi_ip_address>\n    Set the IP address of the local IPMI device in the Oracle registry."
4192, 3, "  crsctl set css ipmiadmin <ipmi_admin_name>\n    Set the administrative login for the local IPMI device in the Oracle registry."
4193, 3, "  crsctl set css votedisk asm <diskgroup>[...]\nwhere\n    diskgroup       Voting disk disk group\n"
4194, 3, "  crsctl set css {<parameter> <value>|ipmiaddr <ipmi_ip_address>|ipmiadmin <ipmi_admin_name>}"
4195, 3, "  crsctl unset css <parameter>\n    Unsets the value of a Cluster Synchronization Services parameter, restoring its default value\n\n    diagwait\n    disktimeout\n    misscount\n    reboottime\n    priority"
4196, 3, "  crsctl pin css -n <node1>[...]\n Pin the nodes (make leases non-expiring)."
4197, 3, "  crsctl unpin css -n <node1>[...]\n Unpin the nodes (allow leases to expire)." 
4198, 3, "  crsctl replace votedisk <+diskgroup>\nwhere\n    diskgroup   disk group where the voting files will be located in ASM"
4199, 3, "  crsctl set crs activeversion [<version>] [-force]\n    Sets the Oracle Clusterware active version "

/ 4200 - 4250: crsctl ipmi (node kill/fencing) 

4200, 0, "Failed to initialize a security context during wallet IPMI credentials creation.\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Support Services.
4201, 0, "Hash context initialization failure during wallet IPMI credentials creation\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Support Services.
4202, 0, "String hashing failed during wallet credentials creation\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Support Services.
4203, 0, "Hashing creation error during wallet credentials creation\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Support Services.
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
//          operation. If the retry fails call Oracle Support Services.
4209, 0, "IPMI credentials not contained in the wallet\n"
// *Cause:  The wallet has not been configured.
// *Action: Configure the wallet for the IPMI device using 'crsctl set'\n
4210, 0, "Failed to obtain the length of IPMI credentials while accessing the wallet.\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call Oracle Support Services.
4211, 0, "Failed to allocate memory\n"
// *Cause:  Insufficient system memory resources.
// *Action: Correct the system memory resources problem and retry.
4212, 0, "Failed to obtain the secret from the wallet.\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call Oracle Support Services.
4213, 0, "Secret from wallet has incorrect size\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call Oracle Support Services.
4214, 0, "crsctl %s and %s wallet versions of IPMI do not match.\n"
// *Cause:  A mismatch occurred between the IPMI versions of crsctl and the
//          Cluster Synchronization Services Daemon.
// *Action: Check proper installation and configuration of crsctl and the
//          Cluster Synchronization Services Daemon.
4215, 0, "Wallet secret encoding error\n"
// *Cause:  Internal error.
// *Action: Contact Oracle Support Services.
4216, 0, "Unexpected error configuring the wallet contents\n"
// *Cause:  Possible corruption in wallet or internal error.
// *Action: Reconfigure the IPMI wallet using "crsctl set" and then retry the
//          operation. If the retry fails call Oracle Support Services.
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
//         operation if indicated.  If this fails, contact Oracle Support Services.
4227, 0, "Configuration data stored but IPMI IP address is required to complete the change. The change cannot be validated until the information is complete.\n"
//*Cause:  Not proceeding with Client's IPMI login change request because
//         all information such as IPMI username, password and IP address
//         need to be present.
//*Action: Execute 'crsctl set css ipmiaddr' from crsctl.
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
//*Action: Execute 'crsctl set css ipmiadmin' from crsctl.
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
// *Action: Contact Oracle Support Services. 
4252, 0, "Failed to update the profile with the new discovery string\n"
//*Cause:  An internal error happened when updating the discovery string in the profile.
//*Action: Contact Oracle Support Services. 
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
4268, 0, "'-name' option is allowed only with APPQOSDB or CVUDB type wallets"
// *Cause: The '-name' option was specified in a wallet command for other than APPQOSDB or CVUDB type wallet.
// *Action: Use the '-name' option only for actions on APPQOSDB or CVUDB type wallets.
4269, 0, "Successful get priority %d %s for Cluster Synchronization Services.\n"
// *Cause: The 'get' operation was performed successfully.
// *Action: None.

/split the filter help msg (# 4179) into two to restrict it to 400 chars.
4270, 1, "Filter Operators: =, >, <, !=, co, st, en, nc, nci, coi, eqi\n\twhere\n\t\tco  --> contains\n\t\tst  --> starts with\n\t\ten  --> ends with\n\t\tnc  --> does not contain\n\t\tcoi --> contains, case-insensitive\n\t\tnci --> does not contain, case-insensitive\n\t\teqi --> equals, case-insensitive\n\nSample command: crsctl status resource  -w \"TYPE = type1\"" 
4271, 0, "Voting file creation in other than an ASM disk group prohibited in this cluster.\n"
// *Cause: An attempt was made to create voting files outside the
//         ASM disk group.
// *Action: Specify an ASM disk group for voting file creation or replacement.
4272, 0, "error while identifying voting files in use\n"
// *Cause: More than one voting file was identified for the cluster.
// *Action: Contact Oracle Support Services.
4273, 0, "Creation of voting files in an ASM disk group not allowed using the command 'crsctl add votedisk'.\n"
//*Cause: An attempt was made to create voting file in the ASM disk group with the command 'crsctl add votedisk'.
//*Action: Use 'crsctl replace votedisk' to add or replace the voting files in ASM disk group.
4274, 0, "Command not supported in this cluster.\n"
//*Cause: An attempt was made to add voting file(s) in a client cluster with the command 'crsctl add votedisk'.
//*Action: Use 'crsctl replace votedisk' to add or replace the voting file in client clusters.
4275, 0, "Command 'crsctl add css votedisk' command is invalid.\n"
//*Cause: An attempt to add a voting file using 'crsctl add css votedisk' was
//        rejected because voting files are only supported on ASM disk group.
//        Changes in configuration can be made only with 'crsctl replace votedisk'.
//*Action: Use 'crsctl replace votedisk' to add the voting files.
4276, 0, "Command 'crsctl delete css votedisk' command is invalid.\n"
//*Cause: An attempt to delete a voting file using 'crsctl delete css votedisk'
//        was rejected because voting files are present in ASM disk group.
//*Action: Use 'crsctl replace votedisk' to replace the voting files. 
/
/ CRSCTL messages
/
4301, 0, "       crsctl add       - add a resource, type or other entity"
4302, 0, "       crsctl check     - check the state or operating status of a service, resource, or other entity"
4303, 0, "       crsctl config    - display automatic startup configuration"
4304, 0, "       crsctl debug     - display or modify debug state"
4305, 0, "       crsctl delete    - delete a resource, type or other entity"
4306, 0, "       crsctl disable   - disable automatic startup"
4307, 0, "       crsctl discover  - discover DHCP server"
4308, 0, "       crsctl enable    - enable automatic startup"
4309, 0, "       crsctl eval      - evaluate operations on resource or other entity without performing them"
4310, 0, "       crsctl get       - get an entity value"
4311, 0, "       crsctl getperm   - get entity permissions"
4312, 0, "       crsctl lsmodules - list debug modules"
4313, 0, "       crsctl modify    - modify a resource, type or other entity"
4314, 0, "       crsctl query     - query service state"
4315, 0, "       crsctl pin       - make the leases of specified nodes immutable"
4316, 0, "       crsctl relocate  - relocate a resource, server or other entity"
4317, 0, "       crsctl replace   - change the location of voting files"
4318, 0, "       crsctl release   - release a DHCP lease"
4319, 0, "       crsctl request   - request a DHCP lease or an action entry point"
4320, 0, "       crsctl setperm   - set entity permissions"
4321, 0, "       crsctl set       - set an entity value"
4322, 0, "       crsctl start     - start a resource, server or other entity"
4323, 0, "       crsctl status    - get status of a resource or other entity"
4324, 0, "       crsctl stop      - stop a resource, server or other entity"
4325, 0, "       crsctl unpin     - make the leases of previously pinned nodes mutable"
4326, 0, "       crsctl unset     - unset an entity value, restoring its default"
4327, 0, "       crsctl export    - export entities"
4328, 0, "       crsctl create    - display entity creation options"
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
// Msg 4392 continued in msg 6552
4392, 0, "Usage: crsctl <command> <object> [<options>]\n    command: add|check|config|create|debug|delete|disable|discover|enable|eval|export|get|getperm|lsmodules|modify|pin|query|release|relocate|replace|request|set|setperm|start|status|stop|unpin|unset\nFor complete usage, use:\n    crsctl [-h | --help]\n"
4393, 0, "Usage:"
4394, 0, "\n     -l               Leave affected resources as-is if request fails\n     -begin           Start transparent HA action\n     -end             End transparent HA action"
4395, 0, "\n     -begin           Start transparent HA action\n     -end             End transparent HA action" 
// Msg 4396 continued in msg 6553
4396, 3, "Sample filters:\n1. TYPE = type1\n2. ((TYPE = type1) AND (CHECK_INTERVAL > 50))\n3. (TYPE = type1) AND ((CHECK_INTERVAL > 30) OR (AUTO_START co never))\n\nFilter Operators: =, >, <, !=, co, st, en, nc, nci, coi, eqi\n\twhere\n\t\tco  --> contains\n\t\tst  --> starts with\n\t\ten  --> ends with\n\t\tnc  --> does not contain\n\t\tcoi -->"
// Msg 4397 continued in msg 6554
4397, 3, "Sample filters:\n1. TYPE = type1\n2. ((TYPE = type1) AND (CHECK_INTERVAL > 50))\n3. (TYPE = type1) AND ((CHECK_INTERVAL > 30) OR (AUTO_START co never))\n\nFilter Operators: =, >, <, !=, co, st, en, nc, nci, coi, eqi\n\twhere\n\t\tco  --> contains\n\t\tst  --> starts with\n\t\ten  --> ends with\n\t\tnc  --> does not contain\n\t\tcoi -->"
4398, 3, "                crsctl status category -w \"EXPRESSION co 'cpu'\"\n                crsctl status category -w \"EXPRESSION nci 'COUNT'\""
4399, 0, "Command no longer supported. Use 'crsctl get tracefileopts css' or 'crsctl set tracefileopts css' instead.\n" 
// *Cause: The specified command is no longer supported and has been replaced.
// *Action: Use command 'crsctl get tracefileopts css' or
//         'crsctl set tracefileopts css'.
//          For the complete syntax enter 'crsctl get tracefileopts -help' or
//          'crsctl set tracefileopts -help'.

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
4406, 0, "Oracle High Availability Services synchronous start failed."
// *Cause:  A start of Oracle High Availability Services with the '-wait' or '-waithas' 
//          option did not complete successfully.  This message is preceded by others 
//          describing errors that occurred.
// *Action: Examine the error messages preceding this message and correct
//          the problems they describe.
4407, 0, "Values bigger than 10 are not allowed for parameter %s.\n"
// *Cause:  This parameter does not allow values higher than 10.
// *Action: Use a value between 0 and 10.
4408, 0, "Node '%s' configured role successfully changed; restart Oracle High Availability Services for new role to take effect."
// *Cause:  The 'crsctl set node role' command was run to change the role of a node in a Flex Cluster.
// *Action: Restart Oracle High Availability Services on the node by running 'crsctl stop crs' and 'crsctl start crs'.
4409, 0, "Node '%s' is already configured in '%s' role."
// *Cause: A 'crsctl set node role' command specified the role already configured for the node."
// *Action: Specify a different role or a different node, if appropriate.
4410, 3, "  crsctl unset cluster hubsize\n    Unsets the configuration value for the maximum number of Hub nodes in the cluster"
4411, 0, "The role of node %s cannot be converted to 'leaf'."
// *Cause: An attempt was made to modify the role of the last remaining configured 'hub' node to 'leaf' node, which is not allowed or the node is already a 'leaf' node."
// *Action: If role of this node must to be modified to 'leaf', first bring up another node as a 'hub' node to ensure that there is always at least one 'hub' node.
4412, 0, "Attribute '%s' does not exist."
// *Cause: An attempt was made to obtain the value for a nonexistent attribute.
// *Action: Verify the attribute name was specified as intended or retry with a valid attribute.
4413, 3, "The following message was received from node '%s':"
// *Cause:  The mentioned node has sent a message indicating the status of the executed command.
// *Action: See the following message for the status.
4414, 0, "The specified 'crsctl set trace' or 'crsctl get trace' command is no longer supported.\n"
// *Cause: A request was made to modify or acquire a component trace level 
//         which could not be carried out because the designated component 
//         tracing is no longer performed, making the concept of component 
//         trace level no longer applicable.
// *Action: None.
4415, 0, "cannot stop all the Hub Nodes when clusterware stack is still up and running on a Leaf Node"
// *Cause: An attempt to stop all the Hub Nodes was rejected because the 
//         clusterware stack was still running on a Leaf Node, which 
//         needs to be connected to a Hub Node."
// *Action: Stop all the stacks on the Leaf Nodes first, or keep at least one 
//          stack up and running on a Hub Node."
4416, 3, "Server attribute '%s' successfully changed. Restart Oracle High Availability Services for new value to take effect."
// *Cause:  The 'crsctl set' command was run to change the server attribute of a node in a Flex Cluster, however the new value had not taken effect.
// *Action: To have the new value take effect restart Oracle High Availability Services on the node by running 'crsctl stop crs' and 'crsctl start crs'.
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
/ Patch Management (KPFPM), CLSV Patch (clsv*patch) failures
4465, 0, "Error code %d in main Patch Management context initialization\n"
4466, 0, "Error code %d in Patch Management API\n"
4467, 0, "Error code %d in retrieving the software patch level for host %s\n"
4468, 0, "could not retrieve the software patch level because host %s is not a cluster member\n"
//  *Cause: The software patch level could not be retrieved for the indicated 
//          host because it is not a cluster member. 
//  *Action: Specify a host name that belongs to the cluster. 


/
/ Oracle Cluster Registry init failures
4471, 0, "Insufficient privileges at Oracle Cluster Registry initialization: %s\n"
4472, 0, "Oracle Cluster Registry initialization failed accessing Oracle Cluster Registry device: %s\n"
4473, 0, "Oracle Cluster Registry initialization failed with invalid format: %s\n"
4474, 0, "Unable to allocate memory in Oracle Cluster Registry initialization: %s\n"
4475, 0, "Unable to locate Oracle Home in Oracle Cluster Registry initialization: %s\n"
4476, 0, "Failure %d in main Oracle Cluster Registry context initialization: %s\n"
4477, 1, "Oracle Cluster Registry security attributes cannot be initialized.\n"
//  *Cause: An attempt to initialize the Oracle Cluster Registry (OCR) security attributes failed
//          because CRS could not obtain either the user name or the user group name.
//  *Action: Report the error to Oracle Support Services.

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
//             or you tried to delete the last remaining voting disk;
//         19- version incompatibility between client and server.
// *Action: Respond based on the return code as follows:  
//         15 - adjust privileges or use a different userid;
//         16 - review the voting disk configuration displayed by 
//              'crsctl query css votedisk' and 
//              correct your request accordingly;
//         19 - ensure that compatible versions are installed;
//         others - report to Oracle Support Services.
4609, 0, "Error %d while trying to open voting file Oracle Cluster Registry key.\n"
4610, 0, "Failed %d to delete Oracle Cluster Registry keys for voting file.\n"
4611, 0, "Successful deletion of voting disk %s.\n"
4612, 0, "Located %d voting disk(s).\n"
4613, 0, "Failure %d in clssqlnum \n"
4614, 0, "Failure %d in clssnsqname for nodenum %d\n"
4615, 0, "Software version query failed for node %s\n"
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
4646, 0, "Disk group %s does not exist or is not mounted.\n"
// *Cause: The indicated disk group was not found or was not mounted.
// *Action: Create or mount the Disk group before use.
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
// *Action: Shut down the entire clusterware stack before deleting the node.
4659, 1, "Error while trying to unpin node %s.\n"
// *Cause: An internal error happened during this operation.
// *Action: Contact Oracle Support Services.  
4660, 1, "Could not find node %s to delete.\n"
// *Cause: The node to be deleted could not be found because it has not been a
//         member of this cluster recently.
// *Action: Check the name provided.  If the name is correct, the node has
//          been automatically deleted because it was inactive for a long time and
//          no further action is required to delete the node from the cluster.
4661, 1, "Node %s successfully deleted.\n"
//  *Cause: A request to delete a node completed.
//  *Action: None. 
4662, 1, "Error while trying to delete node %s.\n"
// *Cause: Some internal error happened during this operation.
// *Action: Contact Oracle Support Services. 
4663, 1, "could not find node %s to pin\n"
// *Cause: The indicated node was not an active Hub node in the cluster.
// *Action: Ensure that the node name is correct, is a Hub node, and that Oracle
//          Clusterware is running on the node.
4664, 3, "Node %s successfully pinned.\n"
//  *Cause: A request to pin a node completed.
//  *Action: None. 
4665, 1, "Error while trying to pin node %s.\n"
// *Cause: An internal error happened during this operation.
// *Action: Contact Oracle Support Services. 
4666, 1, "Could not find node %s to unpin.\n"
// *Cause: An unpin request specified a node that is not an active hub node in the cluster.
// *Action: Ensure that the node name is correct, that it is a hub node, and that Oracle Clusterware 
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
/ 4675 has been removed - do not reuse number
/ 4676 has been removed - do not reuse number
4677, 0, "Failed to get %s for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Contact Oracle Support Services. 
4678, 0, "Successful get %s %d for Cluster Synchronization Services.\n"
// *Cause: The 'get' operation was performed successfully.
// *Action: None.
/ 4679 has been removed - do not reuse number
/ 4680 has been removed - do not reuse number
4681, 0, "Failed to unset priority for Cluster Synchronization Services.\n"
// *Cause: An internal error happened during this operation for Cluster Synchronization Services.
// *Action: Contact Oracle Support Services. 
4682, 0, "Successful unset priority for Cluster Synchronization Services.\n"
// *Cause: The 'unset' operation was performed successfully.
// *Action: None.
4683, 0, "failed to set parameter '%s' to %d for Cluster Synchronization Services with error %d\n"
// *Cause: A 'crsctl set' command failed. The number following
//        "error" is a return code, which can be: 
//        1 - internal OCSSD server error
//        15 - insufficient privileges for this operation
// *Action: Respond based on the return code as follows: 
//        15 - Adjust privileges or use a different user ID.
//        others - Contact Oracle Support Services.
4684, 0, "Successful set of parameter %s to %d for Cluster Synchronization Services.\n" 
// *Cause: The 'set' operation was performed successfully for Cluster Synchronization Services.
// *Action: None.
/ 4685 has been removed - do not reuse number
/ 4686 has been removed - do not reuse number
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
4698, 0, "Error code %d in retrieving the patch level"
// *Cause: Internal error.
// *Action: Contact Oracle Support Services.
4699, 0, "Error code %d in retrieving the cluster configuration type"
// *Cause: Internal error.
// *Action: Contact Oracle Support Services.

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
4706, 0, "Oracle Clusterware active version on the cluster is [%s]. The cluster upgrade state is [%s]. The cluster active patch level is [%u].\n"
4707, 3, "  crsctl create policyset -file <filePath>\nwhere \n     filePath        Policy set file to create."
4708, 1, "Server name is missing"
// *Cause: The server name provided was empty or no name was provided.
// *Action: Provide a valid server name.
4709, 3, "  crsctl create member_cluster_configuration <member_cluster_name> -file <cluster_manifest_file>  -member_type <database|application>  [-version <member_cluster_version>] [-domain_services [asm_storage <local|direct|indirect>][<rhp>]]"
4710, 3, "  where \n     member_cluster_name    name of the new Member Cluster\n     -file                  path of the Cluster Manifest File (including the '.xml' extension) to be created\n     -member_type           type of member cluster to be created\n     -version               5 digit version of GI (example: 12.2.0.2.0) on the new Member Cluster, if\n                            different from the Domain Services Cluster"
4711, 3, "     asm_storage            indicates the storage access path for the database member clusters\n                            local : storage is local to the cluster\n                            direct or indirect : direct or indirect access to storage provided on the Domain Services Cluster\n     rhp                    generate credentials and configuration for an RHP client cluster."
4712, 0, "An invalid client cluster version [%s] was provided."
// *Cause: An attempt to create a configuration for a client cluster failed because an invalid cluster version was provided for the cluster.
// *Action: Retry the operation, providing a valid client cluster version in the required format(%u.%u.%u.%u.%u). 
4713, 0, "Creating member cluster credential and configuration failed."
// *Cause: An attempt to create a credential and configuration for a 
//         member cluster failed. This is an Internal error.
// *Action: Contact Oracle Support Services.
4714, 0, "invalid output file name [%s] was provided"
// *Cause: An invalid output file name was provided.
// *Action: Provide a valid file name with XML extension. 
4715, 3, "  crsctl delete member_cluster_configuration <member_cluster_name> [-f]\n  where \n        member_cluster_name    Name of the Member Cluster\n        -f                     Force option"
4716, 3, "  crsctl query member_cluster_configuration [<member_cluster_name>]\n  where \n        member_cluster_name    Name of the Member Cluster\n         If no member cluster name is provided then the details of all\n         the member clusters are displayed.\n"
4717, 3, "     -domain_services       services to be initially configured for this member\n                            cluster (asm_storage with local, direct, or indirect access paths, and rhp)\n                            --note that if \"-domain_services\" option is not specified,\n                            then only the GIMR and TFA services will be configured"
4718, 0, "deleting member cluster credential and configuration failure"
// *Cause: An attempt to delete a credential and configuration for a 
//         member cluster failed. The accompanying messages provide detailed
//         failure information. 
// *Action: See the accompanying messages, correct the issue and retry the 
//          command.
4719, 0, "querying member cluster credential and configuration failure"
// *Cause: An attempt to query a credential and configuration for a 
//         member cluster failed. The accompanying messages provide detailed
//         failure information.
// *Action: See the accompanying messages, correct the issue and retry the 
//          command.
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
//  *Cause:  An infrastructure error occurred because a required OCR key 
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
4808, 3, "  crsctl discover dhcp -clientid <clientid> [-port <port>] [-subnet <subnet>]\n     Discover DHCP server\nwhere\n      clientid         client ID for which discovery will be attempted\n      port             The port on which the discovery packets will be sent\n      subnet           The subnet on which DHCP discover packets will be sent\n"
4809, 3, "  crsctl request dhcp -clientid <clientid> [-port <port>] [-subnet <subnet>]\n     Request DHCP lease for the client ID specified\nwhere\n      clientid         client ID for which DHCP lease request will be attempted\n      port             The port on which the DHCP lease request packets will be sent\n      subnet           The subnet on which DHCP lease request packets will be sent\n"
// Msg 4810 continued in msg 6555
4810, 3, "  crsctl release dhcp -clientid <clientid> [-port <port>] [-subnet <subnet>]\n     Release DHCP lease for the client ID specified\nwhere\n      clientid         client ID for which DHCP lease release request will be attempted\n      port             The port on which the DHCP lease release packets will be sent\n"
// Msg 4811 continued in msg 6556
4811, 3, "  crsctl start testdns [-address <IP_address>] [-port <port>][-domain <GNS_domain>] [-once][-v]\n    Start a test DNS listener that listens on the given address at the given port and for specified domain\nWhere\n    IP_address          IP address to be used by the listener (defaults to hostname)\n"
4812, 3, "  crsctl stop testdns [-address <IP_address>] [-port <port>] [-v]\n    Stop the test DNS listener that listens on the given address and at the given port\nWhere\n    IP_address          IP address on which testdns was started (defaults to hostname)\n"
4813, 3, "  crsctl query dns -servers\n     Lists the system configured DNS server, search paths, attempt and timeout values\n"
4814, 3, "  crsctl query socket udp [-address <address>] [-port <port>]\n     Verifies that a daemon can listen on specified address and port\nWhere\n       address             IP address on which socket needs to be created\n       port                port on which socket needs to be created"
// Msg 4815 continued in msg 6557
4815, 3, "  crsctl query dns -name <name> [-dnsserver <DNS_server_address>] [-type <query_type>] [-port <port>] [-attempts <attempts>] [-timeout <timeout>] [-v]\n    Returns a list of addresses returned by DNS lookup of the name with the specified DNS server\nWhere\n    name                Fully qualified domain name to lookup\n"
4816, 3, "    vip_type        Type of VIP resource: HOSTVIP, SCANVIP, or APPVIP\n    VIPResName      User defined application VIP name (required for APPVIP vip_type)\n    nodename        Node for which the client ID is required (required for HOSTVIP vip_type)\n"
4817, 3, "\n    -port               The port on which the listener is listening. Default value for the port is 53. \n    -v                  Verbose output"
// Msg 4051 consists of msg 4051 and msg 4818.
4818, 3, "  crsctl modify wallet -type <wallet_type> <options> \nwhere \n    wallet_type   Type of wallet i.e. , APPQOSADMIN, APPQOSUSER, APPQOSDB, MGMTDB, OSUSER or CVUDB.\n    options       Options to be passed to the modify command"
// Msg 4062 consists of msg 4062 and msg 4819.
4819, 3, "     -w                Resource type filter (For example: \"BASE_TYPE = cluster_resource\")\n     -g                Check whether the resource types are registered\n     -p                Print static configuration\n     -f                Print full configuration\n     -r                Print all of the base types\n"
// Msg 4063 consists of msgs 4063, 4064, 4065 and 4820.
// Msg 4820 continued in msg 6558
4820, 3, "     -g                Check if resources are registered\n     -k                Cardinality ID\n     -d                Degree ID\n     -n                Server name\n     -s                Get target servers for relocation\n     -t                Tabular display"
// Msg 4066 consists of msgs 4066 and 4821.
4821, 3, "     -w                Server filter (e.g., \"STATE = ONLINE\")\n     -g                Check if servers are registered\n     -p                Print static configuration\n     -v                Print runtime configuration\n     -f                Print full configuration"
// Msg 4074 consists of msgs 4074, 4075, 4822 and 4823
4822, 3, "     resName            Add named resource\n     typeName           Resource type\n     filePath           Attribute file\n     attrName           Attribute name\n     value              Attribute value\n     server             Server name"
4823, 3, "     cid                Resource cardinality ID\n     did                Resource degree ID\n     -f                 Force option\n     -i                 Fail if request cannot be processed immediately\n     resourceGroupName  Resource group name"
// Msg 4076 consists of msgs 4076, 4824 and 4834
4824, 3, "     typeName       Add named resource type\n     baseTypeName   Base resource type\n     filePath       Attribute file\n     attrName       Attribute name\n     defaultValue   Default value"
// Msg 4077 consists of msgs 4077 and 4825
4825, 3, "     attrName        Attribute name\n     value           Attribute value\n     -i              Fail if request cannot be processed immediately\n     -f              Force option"
// Msg 4080 consists of msgs 4080 and 4826
4826, 3, "     name            Name is required for APPQOSDB and CVUDB wallets.\n     user_name       User to be added to wallet.\n     passwd          Indication that password will be specified. Password will be read from standard input."
// Msg 4116 consists of msgs 4116, 4117, 4827, 4120, 4125 and 4811 OR
//                      msgs 4116, 4117, 4827, 4119, 4122, 4125 and 4811
4827, 3, "     -d               Resource degree ID\n     -env             Attribute overrides for this command\n     -f               Force option\n     -i               Fail if request cannot be processed immediately\n     -l               Leave affected resources as-is if request fails"
4828, 3, "    net_mask             Subnet mask for the IP to start\n    interface_name       Interface on which to start the IP\n"
4829, 3, "    query_type          The query type is A or AAAA for IPv4 or IPv6 respectively. The default query_type is A.\n    port                Port on which DNS server is listening\n    attempts            Number of retry attempts\n    timeout             Timeout in seconds\n"
4830, 3, "  crsctl unset css ipmiconfig\n    Unsets the IPMI configuration and deletes the associated Oracle Registry entries."
4831, 3, "  crsctl set css <parameter> <value>\n    Sets the value of a Cluster Synchronization Services parameter\n"
4832, 3, "  crsctl set css {ipmiaddr|ipmiadmin} <value>\n    Sets IPMI configuration data in the Oracle registry\n"
4833, 3, "  crsctl set css votedisk asm <diskgroup>[...]\n    Defines the set of voting disks to be used by CRS\n"
// Msg 4076 consists of msgs 4076, 4824 and 4834
4834, 3, "     typeFlags      One or more flag values separated by '|':\n       CONFIG         Attribute may be configured\n       READONLY       Attribute is read-only\n       REQUIRED       Attribute value is required\n       HOTMOD         Attribute is hot-modifiable\n     -i             Fail if request cannot be processed immediately"
// Msg 4055 consists of msgs 4055, 4835 and 4836
4835, 3, "     typeName       Modify named resource type attributes\n     attrName       Attribute name\n     defaultValue   Default value\n     typeFlags      One or more flag values separated by '|':"
4836, 3, "       CONFIG         Attribute may be configured\n       READONLY       Attribute is read-only\n       REQUIRED       Attribute value is required\n       HOTMOD         Attribute is hot-modifiable\n     -f             Force option\n     -i             Fail if request cannot be processed immediately"
4837, 3, "  crsctl status policyset [-file <fileName>] \n     Show the current policies in the policy set\nwhere \n     fileName   Name with which to create a text file that can be used with the 'crsctl modify policyset -file' command"
4838, 3, "  crsctl modify policyset {-attr \"<attrName>=<value>[,...]\" | -file <fileName>} [-ksp] [-f]\nwhere \n    attrName   Name of the policy set attribute, e.g. SERVER_POOL_NAMES, etc.\n    value      Value of the attribute\n    fileName   Name of text file containing policy set definition\n    -ksp       Keep server pools in the system\n    -f         Force option"
4839, 1, "Required attribute '%s' is missing for '%s'."
// *Cause: A required attribute was not specified.
// *Action: Make sure the attribute is specified.
4840, 1, "Attribute '%s' cannot be specified using this command."
// *Cause: An attribute was specified that cannot be used with this command.
// *Action: Server pool configuration can be changed or created using 'crsctl
// modify policyset' and 'crsctl modify serverpool -policy' commands.
4841, 3, "  crsctl status policy [<policy_name>[...] | -w <filter> | -active] \n     Check status of designated policies\nwhere \n     policy_name [...]  One or more blank-separated policy names\n     -w                 Policy filter \n     -active            Used to display the active policy"
4842, 3, "  crsctl modify policy <policy_name> -attr \"<attrName>=<value>[,...]\" \nwhere \n     policy_name     Name of policy to be modified\n     attrName        Attribute name (SERVER_POOLS attribute is not allowed)\n     value           Attribute value\n"
4843, 1, "Policy '%s' does not exist."
// *Cause: An invalid policy name was specified.
// *Action: Verify the name.
4844, 3, "  crsctl add policy <policyName> [-attr \"<attrName>=<value>[,...]]\" \nwhere \n    policyName   Name of policy to be added\n    attrName     Attribute name (SERVER_POOLS and NAME attributes are \n                 not allowed)\n    value        Attribute value"
4845, 3, "  crsctl delete policy <policyName> [...] \nwhere \n    policyName [...]    One or more policy names to be deleted"
4846, 1, "Configuration policy set has an invalid profile."
// *Cause: An invalid policy set definition was specified. Missing elements or duplicate elements may be present in the profile.
// *Action: Verify the contents of the policy set profile and resubmit the command.
4847, 1, "File '%s' does not exist."
// *Cause: The specified for the comamnd did not exist or could not be opened.
// *Action: Verify the filename and resubmit the command.
4848, 1, "Policy '%s' appears more than once in a policy set file."
// *Cause: A policy was defined more than once in the profile.
// *Action: Verify the contents of the policy and remove the duplicate policy.
4849, 1, "Server pool '%s' appears more than once for policy '%s' in the policy set file."
// *Cause: A server pool was defined more than once in the profile for the same policy.
// *Action: Verify the contents of the policy and remove the duplicate server pool.

// ---> crsctl continues from 6500


/
/ Eval messages 4850 - 4899
/
4850, 3, "  crsctl eval start resource {<resname>|-w <filter>}[-n server] [-f]\n    Evaluate start of specified resources"
4851, 3, "  crsctl eval stop resource {<resname>|-w <filter>} [-f]\n    Evaluate stop of specified resources"
4852, 3, "  crsctl eval relocate resource {<resName> | {<resName>|-all} -s <server> | -w <filter>} {-n <server>} [-f]\n    Evaluate relocate of specified resource"
4853, 3, "  crsctl eval add serverpool <spName> [-file <filePath> | -attr  \"<attrName>=<value>[,...]\"] [-f] [-explain | -admin [-l [serverpools [-x]] | [resources | all [-a] [-x]]]]\n    Evaluate addition of specified serverpool"
4854, 3, "  crsctl eval modify serverpool <spName> {-file <filePath> | -attr  \"<attrName>=<value>[,...]\"} [-f] [-explain | -admin [-l [serverpools [-x]] | [resources | all [-a] [-x]]]]\n    Evaluate modification of specified serverpool"
4855, 3, "  crsctl eval delete serverpool <spName> [-explain | -admin [-l [serverpools [-x]] | [resources | all [-a] [-x]]]]\n    Evaluate deletion of specified server pool"
4856, 3, "Server '%s' will be moved from pool '%s' to pool '%s'."
4857, 3, "Resource '%s' (%s) will be in state '%s'."
4858, 3, "Resource '%s' (%s) will be in state '%s' on server '%s'."
4859, 3, "Create new group (Stage Group = %s)."
4860, 3, "Number of actions: %d"
4861, 3, "Sequence ID: %d"
4862, 3, "Internal error while evaluating Policy Engine actions: %s"
4863, 3, "Error code [%s] for entity [%s]. Message is [%s]."
4864, 3, "\nStage Group %d:"
4865, 3, "where\n     resname        Name of a resource\n     -w             Resource filter\n     -n             Server Name\n     -f             Evaluate as with force option"
4866, 3, "where\n     resname        Name of a resource\n     -w             Resource filter\n     -f             Evaluate as with force option"
4867, 3, "Required"
4868, 3, "Action"
4869, 3, "Stage"
4870, 3, "where\n     spName         Name of the serverpool\n     -file          File containing attributes\n     -attr          Attributes for the serverpool\n     -explain       Generate a detailed explanation plan for the command.\n     -f             Evaluate as with force option."
4871, 3, "     -admin         Cluster Administrator view\n     -l             Output display level ('serverpools' for server pools, 'resources' for resources or 'all' for all)\n     -x             Show differences only\n     -a             Show all resources (only when display level is 'resources' or 'all')"
4872, 3, "where\n     spName         Name of the serverpool\n     -f             Evaluate as with force option"
4873, 3, "At least one attribute must be specified for this command."
// *Cause: The 'crsctl eval modify' command was run without specifying any attributes.
// *Action: Rerun the command with at least one attribute specified.
4874, 3, "  crsctl eval add server <serverName> [-file <filePath> | -attr  \"<attrName>=<value>[,...]\"] [-explain | -admin [-l [serverpools [-x]] | [resources | all [-a] [-x]]]]\n    Evaluate addition of server"
4875, 3, "  crsctl eval relocate server <serverName> -to <toPool> [-f] [-admin [-l [serverpools [-x]] | [resources | all [-a] [-x]]]]\n    Evaluate relocation of specified server"
4876, 3, "  crsctl eval delete server <serverName> [-explain | -admin [-l [serverpools [-x]] | [resources | all [-a] [-x]]]]\n    Evaluate deletion of specified server"
4877, 3, "where\n     serverName     Name of the server\n     -file          File containing attributes\n     -attr          Attributes for the server\n     -explain       Generate a detailed explanation plan for the command.\n"
4878, 3, "     toPool         ServerPool to add the server to"
4879, 3, "where\n     serverName     Name of the server\n     -explain       Generate a detailed explanation plan for the command.\n"
4880, 0, "Eval command"
4881, 3, "Server '%(1)s' will be added to pools '%(2)s'."
4882, 3, "Server '%(1)s' will be removed from pools '%(2)s'."
4883, 3, "  crsctl eval add resource <resName> -type <typeName> [-file <filePath> | -attr  \"<attrName>=<value>[,...]\"] [-group <resourceGroupName>] [-f]\n    Evaluate add of specified resource"
4884, 3, "  crsctl eval modify resource <resName> -attr \"<attrName>=<value>[,...]\" [-group <resourceGroupName>] [-f] \n    Evaluate modification of specified resource"
4885, 3, "  crsctl eval fail resource {<resname> | -w <filter>} [-n <server>] [-env \"<attr>=<val>[,...]\"]\n    Evaluate failure of specified resource"
4886, 3, "where\n     resName         Name of the resource\n     attrName        Attribute name\n     value           Attribute value\n     -f              Evaluate as with force option\n     -delete         Evaluate attribute deletion\n"
4887, 3, "where\n     resName         Name of the resource\n     filter          Resource filter\n     server          Server Name\n     -env            Attribute overrides for this command\n"
4888, 3, "where\n     resName            Name of the resource\n     type               Resource type\n     attrName           Attribute name\n     value              Attribute value\n     resourceGroupName  Resource group\n     -f                 Evaluate as with force option\n"
4889, 3, "  crsctl eval activate policy <policyName> [-f] [-explain | -admin {[-l [serverpools [-x]] | [resources | all [-a] [-x]]]}]\n    Evaluate activation of specified policy"
4890, 3, "where\n     policyName     Name of policy\n     -explain       Generate a detailed explanation plan for the command.\n     -f             Evaluate as with force option.\n"
4891, 3, "Invalid value of level specified."
// *Cause: An invalid value for output level was specified. Output level can only be 1, 2 or 3.
// *Action: Rerun the command with a level of 1, 2 or 3.
4892, 3, "Started"
4893, 3, "Relocated"
4894, 3, "Stopped"
4895, 3, "All Instances Stopped!"
4896, 3, "********* Projected Result ***********"
4897, 3, "********* Projected Difference ***********"
4898, 3, "Old Active Servers = %s"
4899, 3, "New Active Servers = %s"

/ Eval messages continue from 8200

/
/ Get/Set log, other crsctl commands 4900 - 4980
/
4900, 3, "  crsctl get log {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>,...\"\n    Get the log levels for specific modules"
// Msg 4901 continued in msg 6559
4901, 3, "  crsctl get log {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>,...\"\n where \n   mdns          multicast Domain Name Server\n   gpnp          Grid Plug-n-Play Service\n   css           Cluster Synchronization Services\n   crf           Cluster Health Monitor\n   crs           Cluster Ready Services\n"
4902, 3, "  crsctl get log res <resname> \n    Get the log level for an agent"
4903, 3, "  crsctl get log res <resname> \n where\n   <resname>     Resource name"
4904, 3, "  crsctl set log {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>=<lvl1>,...\"\n    Set the log levels for specific modules within daemons"
// Msg 4905 consists of msg 4905 and msg 4924.
// Msg 4905 continued in msg 6560
4905, 3, "  crsctl set log {mdns|gpnp|css|crf|crs|ctss|evm|gipc} \"<name1>=<lvl1>,...\"\n where \n   mdns          multicast Domain Name Server\n   gpnp          Grid Plug and Play Service\n   css           Cluster Synchronization Services\n   crf           Cluster Health Monitor\n   crs           Cluster Ready Services"
4906, 3, "  crsctl set log res <resname>=<lvl>\n    Set the log levels for agents"
4907, 3, "  crsctl set log res <resname>=<lvl>\n where\n <resname>     Resource name\n   <lvl>                  Agent log levels"
4908, 0, "%s Module: %s ignored; log level not specified"
4909, 0, "%s Module: %s ignored; trace level not specified"
4910, 0, "Set %s Module: %s  Log Level: %d"
/ 4911 has been removed - do not reuse number
4912, 0, "Get %s Module: %s  Log Level: %d"
/ 4913 has been removed  - do not reuse number
4914, 0, "%s Module: %s ignored invalid component key name used"
4915, 0, "Argument '%s' has an incorrect number of parameters"
4916, 0, "Add %s Log Module: %s"
4917, 0, "Add %s Trace Module: %s"
4918, 0, "Remove %s Log Module: %s"
4919, 0, "Remove %s Trace Module: %s"
4920, 0, "Set Resource %s Log Level: %s"
4921, 0, "Get Resource %s Log Level: %s"
4922, 0, "Module %s: %s ignored; module level out of bounds (valid range %d - %d)"
// *Cause: An attempt to set a log or trace level supplied a level that is out of range for the module.
// *Action: Specify a log or trace level within the valid range.
4923, 0, "%s module: %s ignored; module level is invalid (range 0 - 65535)"
// *Cause: The module log level was invalid (range 0 - 65535).
// *Action: Specify a log level within the valid range (0 - 65535).
4924, 3, "   gipc          Grid Interprocess Communications\n   <name1>, ...    Module names (\"all\" for all names)\n   <lvl1>, ...     Module log levels"
4925, 3, "'all' module keyword was specified with other module names"
// *Cause: The module keyword 'all' already refers to all module names.
// *Action: When referring to all modules, use 'all' without duplicate references to other module names.
4926, 3, "  crsctl get cluster mode {config|status} \n    Get the cluster mode"
4927, 3, "  crsctl get cluster mode {config|status} \n where \n    config            Current cluster configured mode \n    status            Current cluster running mode"
4928, 3, "  crsctl set cluster mode flex \n    Set the cluster mode"
4929, 3, "  crsctl set cluster mode flex \n where \n      flex                   Set cluster mode to \"flex\""
4930, 0, "Cluster is configured as type \"%s\""
4932, 1, "Failed to get the current cluster mode"
// *Cause: There was an internal error while getting cluster mode.
// *Action: Contact Oracle Support Services.
4933, 3, "Cluster mode set to \"flex\"; restart Oracle High Availability Services on all nodes for cluster to run in \"flex\" mode."
// *Cause: Cluster mode was changed to \"flex\", which requires a cluster restart.
// *Action: Restart Oracle High Availability Services on all nodes for cluster to run in \"flex\" mode.
4934, 1, "Failed to set the cluster mode"
// *Cause: There was an internal error while setting cluster mode.
// *Action: Contact Oracle Support Services.
4935, 0, "Cluster is running in \"flex\" mode"
4936, 0, "Cluster is running in \"standard\" mode"
4937, 1, "Unable to set the cluster mode."
// *Cause: An attempt was made to set the cluster mode to 'flex' but Grid Naming Service(GNS) was not configured.
// *Action: Configure GNS and try again to set the cluster mode to 'flex'.
4938, 0, "Cluster is already configured in \"flex\" mode"
4939, 0, "Cluster is already configured in \"standard\" mode"
4940, 1, "Cluster must run in standard or flex mode to use this command"
// *Cause: An attempt was made to set the cluster mode but machine is not running as a cluster. 
// *Action: Cluster must be in standard or flex mode to change the cluster mode.
4941, 0, "Shutting down cluster..."
4942, 3, "Cluster mode set to \"standard\""
// *Cause: Cluster mode is changed. Cluster will shut down now.
// *Action: None.
4943, 3, "  crsctl get node role {config|status} [-node <nodename> | -all]\n    Gets the current role of nodes in the cluster"
4944, 3, "  crsctl get node role {config|status} [-node <nodename> | -all]\n    Gets the current role of nodes in the cluster\nwhere\n    nodename     Node for which node role is to be displayed\n    -all         Display roles of all nodes\n    config       Display configured  role for the node\n    status       Display current active role for the node"
4945, 3, "Node '%s' configured role is '%s'"
4946, 3, "Node '%s' active role is '%s'"
4947, 3, "  crsctl set node role {hub|leaf} [-node <nodename>]\n    Sets the configured role of the node in the cluster"
4948, 3, "  crsctl get cluster hubsize\n    Gets the current configured value for the maximum number of Hub nodes in the cluster"
4949, 3, "  crsctl set cluster hubsize <value>\n    Sets the configuration value for the maximum number of Hub nodes in the cluster"
4950, 3, "Current hubsize parameter value is %d"
4951, 3, "Cluster hubsize parameter set to %d"
4952, 3, "\n     -waithas     Wait until startup is complete and display OHASD progress and status messages\n     -cssonly     Start only CSS\n     -noautostart Start only OHAS"
4953, 3, "CSS already running in nonexclusive mode"
// *Cause: An exclusive mode CRS stack start was attempted when CSS was already running in nonexclusive mode.
// *Action: Stop the CRS stack first and then start in exclusive mode. 
4954, 3, "CRSD already running in nonexclusive mode"
// *Cause: An exclusive mode CRS stack start was attempted when CRSD was already running in nonexclusive mode.
// *Action: Stop the CRS stack first and then start in exclusive mode. 
4955, 3, "CSS failed to start in exclusive mode"
// *Cause: An exclusive mode CRS stack start was attempted but CSS failed to start in exclusive mode.
// *Action: Check the Clusterware alert log for errors. Correct the reported error(s) and retry.
4956, 3, "CRSD failed to start in exclusive mode"
// *Cause: An exclusive mode CRS stack start was attempted but CRSD failed to start in exclusive mode.
// *Action: Check the Clusterware alert log for errors. Correct the reported error(s) and retry.
// Msg 4957 continued in msg 6561
4957, 3, "  crsctl get credentials -target <target> [-id <ID>] -toxml <xmlfile> [-section <sectionName>]\nwhere\n     target        Target as is listed by 'crsctl query credentials targetlist'.\n     ID            Credentials member ID to export. If not specified, exports all \n                   members in the credentials set.\n"
4958, 3, "  crsctl set credentials <options>\n    Imports the specified credentials from an XML file"
4959, 3, "  crsctl set credentials -target <target> -fromxml <xmlfile>\nwhere\n     target        Target as is listed by 'crsctl query credentials targetlist'.\n     xmlfile       Path to XML file from which credentials will be read."
4960, 3, "  crsctl get credentials <options>\n    Exports the specified credentials to an XML file"
4961, 3, "  crsctl get cpu equivalency\n    Gets the current configured value for server attribute CPU_EQUIVALENCY"
4962, 3, "  crsctl set cpu equivalency\n    Sets the configuration value for server attribute CPU_EQUIVALENCY"
4963, 3, "Current cpu equivalency parameter value is %d"

4964, 3, "  crsctl get resource use\n    Gets the current configured value for server attribute RESOURCE_USE_ENABLED"
4965, 3, "  crsctl set resource use\n    Sets the configuration value for server attribute RESOURCE_USE_ENABLED"
4966, 3, "Current resource use parameter value is %d"
4967, 0, "Input values are out of range for parameter %s"
// *Cause: A value was provided which was out of range for this parameter. 
// *Action: Specify a value which is appropriate for this parameter. 
4968, 0, "Invalid values for parameter %s. Specify either 0 or 1."
// *Cause: A value was provided which was out of range for this parameter. 
// *Action: Specify a value which is appropriate for this parameter. 
4969, 0, "Specified server attribute %s does not exist"
// *Cause: A nonexistent attribute was specified for get/set command. 
// *Action: Specify an attribute that exists.Run 'crsctl stat res 
// <resourcename>  -p' to list all the attributes of that resource.
4970, 3, "  crsctl get server label\n    Gets the current configured value for server attribute SERVER_LABEL"
4971, 3, "  crsctl set server label\n    Sets the configuration value for server attribute SERVER_LABEL"
4972, 3, "Current SERVER_LABEL parameter value is %s"
4973, 1, "Flex ASM must be enabled before switching the cluster mode to 'flex'"
// *Cause: An attempt to change the cluster mode to 'flex' failed because Flex 
//         ASM is not enabled.
// *Action: Enable Flex ASM before changing the cluster mode. Refer to Oracle
//          Automatic Storage Management Administrator's Guide for configuring
//          Flex ASM.
4974, 3, "  crsctl query crs autostart \n    Gets the value of automatic start delay and server count\n"
4975, 3, "  crsctl set crs autostart [delay <delayTime>] [servercount <count>] \n    Sets the Oracle Clusterware automatic resource start criteria \nwhere\n     delayTime     Autostart time delay (in seconds)\n     count         Minimum servercount required for autostart\n"
4976, 3, "  crsctl set crs autostart [delay <delayTime>] [servercount <count>] \n    Sets the Oracle Clusterware automatic resource start criteria\n"
4977, 1, "Cluster cannot be converted from 'flex' mode to 'standard' mode"
// *Cause: An attempt was made to set the cluster mode to standard from flex mode. 
// *Action: If a cluster needs to be converted to standard mode, reinstall Clusterware.
4978, 3, "  crsctl unset {cluster|css} <parameter>\n" 
4979, 3, "  crsctl unset css <parameter>\n" 
/
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
4985, 1, "The value '%s' of FLAGS attribute is invalid."
// *Cause: An invalid flag value was specified.
// *Action: Flag values may be combined using the '|' character as a separator.
4986, 1, "This command is for Oracle's internal use only"
// *Cause: A command meant for internal use was specified.
// *Action: Refer to 'crsctl -h' for list of commands available for use.
4987, 0, "'Autostart delay':       %s"
// *Document: NO
4988, 0, "'Autostart servercount': %s"
// *Document: NO
4989, 0, "Module %s: %s ignored; module level out of bounds (valid range %d - %d)"
// *Cause: An attempt to set a log or trace level supplied a level that is out of range for the module.
// *Action: Specify a log or trace level within the valid range.
4990, 0, "Issued command does not support filter in this version of CRS."
// *Cause: The command was rejected because a filter (-w) was specified. Filters are not currently supported for this command.
// *Action: Reissue the command without the filter.
4991,0,  "Could not delete the resource because it does not exist."
// *Cause: An attempt to delete a resource failed because the resource specification did not identify an existing resource. Either there was no resource with the specified name, or no resource satisfied the specified filter.
// *Action: Reissue the command specifying the name of an existing resource or a filter that will select an existing resource.
4992,0,  "Could not delete the server pool because it does not exist."
// *Cause: An attempt to delete a server pool failed because the server pool specification did not identify an existing server pool. Either there was no server pool with the specified name, or no server pool satisfied the specified filter.
// *Action: Reissue the command specifying the name of an existing server pool or a filter that will select an existing server pool. 
4993,0,  "Could not delete the server category because it does not exist."
// *Cause:  An attempt to delete a server category failed because the server category specification did not identify an existing server category. Either there was no server category with the specified name, or no server category satisfied the specified filter.
// *Action:  Reissue the command specifying the name of an existing server category or a filter that will select an existing server category.
4994,0,  "Could not delete the resource type because it does not exist."
// *Cause: An attempt to delete a resource type failed because the resource type specification did not identify an existing resource type. Either there was no resource type with the specified name, or no resource type satisfied the specified filter.
// *Action: Reissue the command specifying the name of an existing resource type or a filter that will select an existing resource type.
4995, 1, " The command '%s' is invalid in crsctl. Use srvctl for this command."
// *Cause: An attempt was made to use an unsupported command in crsctl.
// *Action: Use srvctl for the mentioned command.

4996, 0, "Command ('crsctl %s policyset') is not supported in this version of CRS."
// *Cause: The command was rejected because policy-based management is not a supported feature in this release. 
// *Action: If this error occurs during rolling upgrade, wait for the upgrade to finish. Otherwise, upgrade to the required release or higher. 
4997, 0, "Command ('crsctl %s category') is not supported in this version of CRS."
// *Cause: The command was rejected because the server category is not a supported feature in this release. 
// *Action: If this error occurs during rolling upgrade, wait for the upgrade to finish. Otherwise, upgrade to the required release or higher. 
4998, 0, "Command ('crsctl eval %s' ) is not supported in this version of CRS."
// *Cause: The command was rejected because What-If is not a supported feature in this release. 
// *Action: If this error occurs during rolling upgrade, wait for the upgrade to finish. Otherwise, upgrade to the required release or higher. 
4999, 0, "Command ('crsctl %s policy') is not supported in this version of CRS."
// *Cause: The command was rejected because policy-based management is not a supported feature in this release. 
// *Action: If this error occurs during rolling upgrade, wait for the upgrade to finish. Otherwise, upgrade to the required release or higher. 
/
/ 5000 - 5099 AND 5200 - 5500  Reserved for RAC Agents
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
// *Cause:  An error occurred during the resource action.
// *Action: Examine the accompanying error messages and respond accordingly.
//
/
5018, 0, "Clusterware has disabled an IP route associated with destination \"%s\" and interface \"%s\". For details, refer to \"%s\" in \"%s\"."
// *Cause: A potentially conflicting route in the same subnet used by the
//  address for the redundant interconnect was found and removed to prevent
//   routing conflicts.
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
//  "ALTER SYSTEM SET ASM_DISKSTRING <discovery_string> ...", see
//  Setting Oracle ASM Initialization Parameters in the 
//  Automatic Storage Management Administrator's Guide
/
5020, 0, "Not all endpoints are registered for listener %s"
// *Cause: Listener agent failed to register all endpoints to listener.
// *Action: Check listener log file for that listener.
/
/Alert
5021, 0, "Check of storage failed: details at \"%s\" in \"%s\""
// *Cause: The check of ASM storage failed because the storage was not accessible.
// *Action: Check Clusterware alert log and the referenced Oracle Clusterware
// trace file for additional information.
/
/Alert
5022, 0, "Stop of resource \"%s\" failed: current state is \"%s\""
// *Cause: The named resource failed to stop.
// *Action: Ensure there are no users of the resource and reissue the stop.
// 
/
/Alert
5023, 0, "Failed to unmount file system \"%s\"; details at \"%s\" in \"%s\""
// *Cause: The named file system resource failed to unmount.
// *Action: Determine which OS processes are accessing the mount point using an
// OS command such as 'fuser' or 'lsof' for Unix based platforms or 'handle' 
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
// *Action: Determine which OS processes are accessing the mount point using an
// OS command such as 'fuser' or 'lsof' for Unix based platforms or 'handle' 
// for Windows. Close, shut down, or terminate applications and processes 
// accessing the mount point, then retry.
// 
/
5027, 1, "The ASM instance on node \"%s\" cannot be stopped because it is currently being used by Cluster Ready Services."
// *Cause: An attempt to stop the ASM instance on the indicated server failed because Cluster Ready Services was using that ASM instance.
// *Action: Use 'crsctl stop crs' or 'crsctl stop cluster' to stop the 
// Cluster Ready Services on the node.
/
/Alert
5028, 0, "Cannot start resource \"%s\" because the resource it depends on, \"%s\", failed to start on the same node"
// *Cause: The resource could not be started because the resource on which it depends failed to start on the same node.
// *Action: Manually start the dependency resource and then the resource on the same node.
/
/Alert
5029, 0, "Agent failed to initialize ARP devices required for starting the HAIP resource"
// *Cause: The resource could not be started because the ARP devices failed to start on the same node.
// *Action: Manually check the ARP devices on the same node and then start the resource.
/
5030, 0, "The resource action \"%s %s\" completed with the following error: %s"
// *Cause:  An error occurred during the resource action.
// *Action: Examine the accompanying error messages and respond accordingly.
/
5031, 0, "invalid instance open mode: '%s'"
// *Cause:  The instance open mode passed to the Agent was invalid.
// *Action: Provide a correct instance open mode and retry.
/
5032, 0, "incompatible instance open mode: '%s' with the role of the database in an Oracle Data Guard configuration: '%s'"
// *Cause:  The instance open mode passed to the Agent was invalid for the role of the database in an Oracle Data Guard configuration.
// *Action: Provide a correct instance open mode or change the role of the database in an Oracle Data Guard configuration and retry.
/
5033, 0, "Open mode '%s' is incompatible with the current instance state '%s'."
// *Cause: An attempt to change the instance to the specified open mode failed because the specified mode was incompatible with the current instance state. 
// *Action: Reissue the command with a correct instance open mode.
/
5034, 0, "failed to get instance connection"
// *Cause: Agent process failed to get an instance connection. Internal error.
// *Action: If error persists, contact Oracle Support Services.
/
5035, 3, "Instance is already in the desired state '%s'."
// "Document: NO"
/
5036, 3, "successfully changed the instance state to '%s'"
// "Document: NO"
/
5038, 0, "Oracle home '%s' was not configured correctly."
// *Cause: The 'oracle' executable was not relinked in the Oracle home or, on Windows platforms,
// the %ORACLE_HOME%\bin\oracle.key file did not exist, or the Windows registry key specified in %ORACLE_HOME%\bin\oracle.key did not exist.
// *Action: Relink the Grid Infrastructure executables as described in the Oracle Grid Infrastructure Installation Guide for your operating system.
/
5039, 0, "Oracle executable '%(1)s' was not present in Oracle home '%(2)s'."
// *Cause: The 'oracle' executable was not found in the expected location when checking if Oracle home was configured correctly.
// *Action: Relink the Grid Infrastructure executables as described in the Oracle Grid Infrastructure Installation Guide for your operating system.
/
5040, 1, "Start action for preconnect service resource '%(1)s' failed because base service name '%(2)s' is running."
// *Cause: An attempt to start a preconnect service was rejected because its associated base service was already running on the instance.
// *Action: Either issue the start request on another node or stop the base service and reissue the start on this node.
/
5041, 1, "No available network interface found for network classification %s. Confirm that network interfaces for that classification are UP and RUNNING."
// *Cause: There was a problem when initializing the network interface list for highly available IP (HAIP).
// *Action: Confirm that network interfaces for that classification are UP and RUNNING on this node. 
/
5042, 0, "failed to check whether service has any connected Java sessions"
// *Cause: An unexpected internal error occurred.
// *Action: If the error persists, contact Oracle Support Services.
/
5043, 1, "An I/O control request to determine whether Infiniband ACLs are enabled failed with error: '%s'."
// *Cause: During listener start, an OS 'ioctl' request failed.
// *Action: Examine the accompanying error message, resolve the problem reported, and restart the listener.
/
5044, 1, "Socket creation for communication failed with error: '%s'."
// *Cause: During listener start, an OS system call 'socket' failed.
// *Action: Examine the accompanying error message, resolve the problem reported, and restart the listener.
/
5045, 1, "Reader farm service '%(1)s' does not exist in the database '%(2)s'."
// *Cause: During the specified reader farm service start or check action, it was found that the service did not exist in the indicated database.
// *Action: Restart the non-reader farm service of the database so that the reader farm service is created in the database and then start a reader farm service.
/
5046, 1, "Reader farm service '%(1)s' does not exist in the PDB '%(2)s' of database '%(3)s'."
// *Cause: During the specified reader farm service start or check action, it was found that the service did not exist in the indicated PDB of the indicated database.
// *Action: Restart the non-reader farm service of the PDB so that the reader farm service is created in the PDB and then start a reader farm service.
/
5047, 0, "SCAN listener %s has endpoints registered on incorrect SCAN VIPs."
// *Cause: A periodic check by the the listener agent detected that the SCAN listener had endpoints registered on incorrect SCAN VIPs. 
// *Action: Restart the SCAN listener. If the error persists, contact Oracle Support Services.
/
5048, 0, "Failure communicating with CRS to access a resource profile or perform an action on a resource"
// *Cause: An attempt to access a resource profile or perform an action on a 
//         resource encountered an error attempting to communicate with 
//         Oracle Cluster Ready Services (CRS).
// *Action: If this error did not occur while bringing the clusterware stack 
//          up or down, please contact Oracle Support Services. Otherwise, 
//          retry the operation when the clusterware stack is up.
/
5090, 3, "  crsctl get server css_critical\n    Gets the current configured value for server attribute CSS_CRITICAL"
5091, 3, "  crsctl set server css_critical {yes|no}\n    Sets the configuration value for server attribute CSS_CRITICAL"
5092, 3, "Current value of the server attribute CSS_CRITICAL is %s."
/
// 5100 - 5150 : Reserved for CLSCRS-API status messages
/
5100,    1, "One or more attributes were not found for the entity."
// *Cause:  The operation failed because the entity lacked one or more attributes.
// *Action: Provide the required attributes and retry the operation.
5101,    1, "The specified entity was not found in the entity list."
// *Cause:  The Cluster Ready Services daemon was unable to locate the input entity in its entity list.
// *Action: Retry the operation after deleting the entity and registering it again.
5102,    1, "The entity is already registered."
// *Cause:  An attempt was made to register an entity that was already
//          registered.
// *Action: If the specification of the entity was incorrect, retry the operation with the correct entity specification.
5103,    1, "The entity is not registered."
// *Cause:  An attempt was made to operate on an entity that was not registered.
// *Action: If the specification of the entity was incorrect, retry specifying the correct entity otherwise register the entity and retry the operation.
5104,    1, "The registration of the entity failed."
// *Cause:  An attempt to register an entity failed. The preceding error messages provide additional details.
// *Action: Correct the issues described in the accompanying error messages and retry the registration.
5105,    1, "Unregistering the entity failed."
// *Cause:  An attempt to unregister an entity failed. The preceding error messages provide additional details.
// *Action: Correct the issues described in the accompanying error messages and try to unregister the entity again.
5106,    1, "The entity failed to start."
// *Cause:  An attempt to start an entity failed. The preceding error messages provide additional details.
// *Action: Correct the issues described in the accompanying error messages and try to start the entity again.
5107,    1, "The entity failed to stop."
// *Cause:  An attempt to stop an entity failed. The preceding error messages provide additional details.
// *Action: Correct the issues described in the accompanying error messages and try to stop the entity again.
5108,    1, "The entity failed to relocate."
// *Cause:  An attempt to relocate an entity failed. The preceding error messages provide additional details.
// *Action: Correct the issues described in the accompanying error messages and try to relocate the entity again.
5109,    1, "The status code is invalid."
// *Cause:  The status code was not of the type enum CLSCRS_STAT.
// *Action: Verify that the status code argument is a valid code returned from the CLSCRS API and retry.
5110,    1, "The entity failed to update."
// *Cause:  An attempt to update an entity failed. The preceding error messages provide additional details.
// *Action: Correct the issues described in the accompanying error messages and try to update the entity again.
5111,    1, "The entity has an invalid profile."  
// *Cause:  There were invalid attributes in the entity profile.
// *Action: Check the entity profile, remove any invalid attributes and retry the operation.
5112,    1, "The action script of the entity cannot be found."
// *Cause:  The action script of the entity specified by the attribute ACTION_SCRIPT could not be located.
// *Action: Ensure that the attribute ACTION_SCRIPT exists and specifies a valid script for the entity.
5113,    1, "The entity has a dependency error."
// *Cause:  An attempt to operate on an entity failed because of the resulting effect on one or more dependent entities. Preceding messages provide details on the nature of the problem.
// *Action: Take the corrective action as suggested by the preceding messages and resubmit the operation.
5114,    1, "A placement error was encountered while attempting to operate on the entity."
// *Cause: Based on the placement policy for the entity, there was no 
// available server to which the entity could failover or start.
// *Action: Check the target server for the entity and restart the entity
//          using the 'crsctl start' command.    
5115,    1, "The specified server is not in the cluster."
// *Cause: The specified server name did not designate a server in the cluster.
// *Action: Check the server names in the cluster and retry the operation specifying a server that is a member of the cluster.
5116, 2, "The operation on the entity has been cancelled."
// *Cause:  A scheduled or running operation was cancelled.
// *Action: None.
5117, 1, "An internal error occurred while operating on the entity."
// *Cause: There was an internal error. This message will be preceded by another message with a more specific problem description.
// *Action: Review the accompanying error messages and contact Oracle Support Services.
5118, 1, "The entity or all of its instances are disabled."
// *Cause: The attempted request could not be serviced because the entity was disabled.
// *Action: Enable the entity and retry the operation.
5119, 1, "The active version of Cluster Ready Services is below the required level."
// *Cause:  An attempt was made to use the functionality that has only been available beginning with the active version specified in the preceding message.
// *Action: Upgrade to the minimum required version stated in the preceding message.
5120, 1, "The requested action for the entity was aborted due to a timeout."
// *Cause:  The timeout specified for a custom action was reached before the action could complete.
// *Action: Revise the timeout setting and retry the action.
5121, 1, "The operation cannot be completed due to invalid arguments."
// *Cause:  Invalid arguments were specified to execute the CRS command.
// *Action: Check the arguments and specify only valid arguments to the command.
5122, 1, "The entity could not be registered due to a type mismatch."
// *Cause: The registration of an entity failed because the input entity type to the API did not match the type of the entity to be registered.
// *Action: Specify the correct entity type to register the entity.
5123, 1, "The resource validity check failed due to an invalid resource type."
// *Cause:  The value of the attribute TYPE for the resource was not \'application\'.
// *Action: Specify the value 'application' for the resource attribute TYPE.
5124, 1, "The entity has one or more attributes missing."
// *Cause:  The validity check failed to find one or more of the attributes NAME, TYPE or ACTION_SCRIPT for the entity.
// *Action: Update the entity to have the missing attributes.
5125, 1, "The action script does not exist for the entity."
// *Cause:  The validity check on the entity failed to find the file specified in the attribute ACTION_SCRIPT of the entity.
// *Action: Provide the full path to an existing file for the attribute ACTION_SCRIPT.
5126, 1, "The entity has invalid hosting servers for the placement policy."
// *Cause:  Either the attribute HOSTMEM_REQ was not set or was empty for the entity.
// *Action: Either set the attribute HOSTMEM_REQ or set the attribute PLACEMENT to 'balanced'.
5127, 1, "The attribute HOSTING_MEMBERS must not be specified for the entity."
// *Cause:  The attribute HOSTING_MEMBERS was specified for the entity with the balanced placement policy.
// *Action: Either unset the attribute HOSTING_MEMBERS or set the entity's placement policy to be 'favored' or 'restricted'.
5128, 1, "The value of the attribute HOSTING_MEMBERS for the entity is invalid."
// *Cause:  The value of the attribute HOSTING_MEMBERS for the entity contained one or more of the characters: ',', ';' or ':'.
// *Action: Remove the invalid characters from the value of the attribute HOSTING_MEMBERS.
5129, 1, "An invalid placement policy was specified for the entity."
// *Cause : The attribute PLACEMENT for the entity was set to an invalid value.
// *Action: Set the attribute PLACEMENT to either 'favored','restricted', or 'balanced'.
5130, 1, "An invalid value was specified for the attribute AUTO_START."
// *Cause:  The attribute AUTO_START of the entity was set to an invalid value.
// *Action: Set the attribute AUTO_START to either 'always', 'never', or 'restore'.
5131, 1, "One or more attribute of the entity are set to invalid values."
// *Cause:  An attempt was made to set the attribute to a value of different type.
// *Action: Check the attributes and set the value to the appropriate type.
5132, 1, "The entity list is not empty."
// *Cause:  The entity list passed to receive the information for the queried CRS entities was not empty.
// *Action: Create an empty list to pass as the output argument and retry.
5133, 1, "The generated connection key is too long."
// *Cause:  The size of the environment variables HOST and HOSTNAME were greater than 255 characters.
// *Action: Set the environment variables HOST and HOSTNAME to values whose length is no more than 255 characters.

// 5151 - 5199 : Reserved for CLSCRS-API return code converted to message text.
5151, 1, "Memory could not be allocated."
// *Cause:  An attempt to allocate memory for an entity failed.
// *Action: Check the system logs, correct the condition and retry the operation.
5152, 1, "The pointer to the context is invalid."
// *Cause:  A null pointer was passed as a pointer to the context.
// *Action: Create a valid context and pass its address to the requested operation.
5153, 1, "The entity pointer is invalid."
// *Cause:  A null pointer was passed to the API for the entity name or the entity value."
// *Action: Allocate memory for the entity name and the entity value and pass in the valid pointers to the API.
5154, 1, "The input attribute name not found in the entity's attribute list."
// *Cause:  An attempt was made to modify a nonexistent attribute of an entity.
// *Action: Provide an existing attribute of the entity and retry the operation.
5155, 1, "The end of the entity list was reached."
// *Cause:  An attempt was made to search beyond the end of the entity list.
// *Action: None.
5156, 1, "The entity has no attributes."
// *Cause:  An attempt was made to get the attribute list for an entity that has no attributes.
// *Action: Check the entity name that is being passed. If it's correct then delete the entity, register it with correct attributes and retry the operation.
5157, 1, "The pointer to the operation status message in the entity structure is null."
// *Cause:  The message pointer in the entity structure was null. The entity maybe corrupted.
// *Action: Delete the entity, register the entity and retry the operation.
5158, 1, "The entity list could not be found."
// *Cause:  An attempt was made to perform an operation on an entity list, but no valid entity list was passed.
// *Action: None
5159, 1, "The specified entity already exists."
// *Cause:  An attempt was made to add an entity that already exists.
// *Action: Check the entity name to be added. If it is correct and the existing entity must be recreated, then delete the entity and retry the operation.
5160, 1, "The entity list is empty."
// *Cause:  The query failed because the entity list was empty.
// *Action: Retry the query supplying the intended list of entities.
5161, 1, "The entity name contains invalid characters."
// *Cause:  An attempted operation was rejected because the specified entity name contained invalid characters.
// *Action: Retry the operation specifying a valid entity name.
5162, 1, "The name of a resource or a filter contains invalid characters."
// *Cause:  An attempted operation was rejected because the specified resource name or the filter name contained invalid characters.
// *Action: Retry the operation specifying a valid resource name or the filter name.
5164, 1, "The attribute name is longer than 255 characters."
// *Cause:  An attempt was made to use an attribute name with a length of more than 255 characters.
// *Action: Use an attribute name shorter than 255 characters and retry the operation.
5165, 1, "The supplied buffer is too small for the filter to string conversion."
// *Cause: The buffer supplied to the API was too small to hold the output string.
// *Action: Increase the buffer size and pass it to the API.
5166,    1, "The specified return code is invalid."
// *Cause:  The return code was not of the type 'enum clscrsret'.
// *Action: Verify that the return code argument is a valid code returned from the CLSCRS API and retry.
5167, 1, "The value contains invalid characters."
// *Cause:  An attempted operation was rejected because the specified attribute name or value contained invalid characters.
// *Action: Retry the operation using valid characters.

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
/Alert
5834, 1, "Resource '%s' monitoring disabled due to repeated agent failures. Details at %s in %s."
// *Cause: A cluster resource was disabled because it was causing repeated agent failures.
// *Action: Restart the resource after resolving the problems with the agent.
5835, 1, "Agent version incapable of processing this command"
// *Cause: A request encountered an older agent version that is not capable of processing that request.
// *Action: Upgrade the agent to the Clusterware version.
/Alert
5836, 1, "Agent '%s' version '%s' cannot process command. Details at %s in %s."
// *Cause: A request encountered an older agent version that is not capable of processing that request.
// *Action: Upgrade the agent to the Clusterware version.
5837, 1, "Unable to open environment file '%s'."
// *Cause: The environment file specified could not be opened.
// *Action: Verify that the filename, its location and its permsissions are correct.
5838, 1, "Syntax error in environment file '%s'."
// *Cause: The environment file specified did not have key value pairs in the
//         correct format.
// *Action: Correct the key value format and retry. Consult the administration
//          document for the correct format.
5839, 1, "The requested action '%s' for the resource '%s' on server '%s' was aborted due to a timeout."
// *Cause: The timeout specified for a custom action was reached before the action could complete.
// *Action: Revise the timeout setting and retry the action.

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
6016, 3, "Resource auto-start has completed for server %s"
// *Cause : CRS has completed startup of resources on the specified server.
// *Action: None
6017, 3, "Processing resource auto-start for servers: %s"
// *Cause :The blocking start of Oracle High Availability Services has updated its list
//         of servers to process.
// *Action:None
6018, 3, "===== Summary of resource auto-start failures follows ====="
// *Document: NO

/
/ License checking error
6020, 0, "Software is not licensed for use on this system."

6021, 2, "Could not set system resource limits for Clusterware: \"ulimit -%s %s\"."
// *Cause: A ulimit command issued internally to set system resource limits failed.
// *Action: Ensure that the correct resource limit values are set in the user profile and limits.conf.

6022, 3, "Starting Oracle High Availability Services-managed resources"
// *Cause : Oracle High Availability Services is attempting to start resources for the local server.
// *Action: None
6023, 3, "Starting Oracle Cluster Ready Services-managed resources"
// *Cause : Oracle Cluster Ready Services is attempting to start resources for the cluster.
// *Action: None
6024, 3, "Completed start of Oracle Cluster Ready Services-managed resources"
// *Cause : Oracle Cluster Ready Services has started resources for the cluster.
// *Action: None
6025, 3, "Reserved for ranked resource startup"
// * Document: NO
6026, 3, "Stopping Oracle Cluster Ready Services"
// *Cause: Oracle Cluster Ready Services was stopped on at least one server.
// *Action: None.
6027, 3, "Starting Oracle Cluster Ready Services"
// *Cause: Oracle Cluster Ready Services was started on at least one server.
// *Action: None.
6028, 3, "Starting Oracle Cluster Ready Services-managed resources on server '%(1)s'"
// *Cause: Oracle Cluster Ready Services has started managed resources on the
// specified server.
// *Action: None.

///////////////////////////////////////////////////////////////////////
// 6500 - 6999 More crsctl messages
///////////////////////////////////////////////////////////////////////
6500, 3, "  crsctl add category <categoryName> [-attr \"<attrName>=<value>[,...]\"] [-i] \nwhere \n    categoryName Name of server category to be added\n    attrName     Attribute name \n    value        Attribute value \n    -i           Fail if request cannot be processed immediately"
6501, 3, "  crsctl delete category {<categoryName> [...]|-w <filter>} [-i]\nwhere \n    categoryName [...]    One or more server categories to be deleted\n    -w                    Category filter (e.g., \"NAME = myCateg\")\n    -i                    Fail if request cannot be processed immediately"
6502, 3, "  crsctl modify category <categoryName> -attr \"<attrName>=<value>[,...]\" [-f] [-i] \nwhere \n    categoryName Name of server category to be modified\n    attrName     Attribute name \n    value        Attribute value \n    -f           Force option\n    -i           Fail if request cannot be processed immediately"
6503, 3, "  crsctl status category [<categoryName>[...] | -w <filter> | -server <serverName>] \n     Check status of designated server categories\nwhere \n     categoryName [...] One or more blank-separated category names\n     -w                 Server Category filter \n     -server            Used to list all the categories that a particular server matches"
6504, 1, "'%s' cannot be specified as an attribute."
// *Cause: An effort was made to explicitly specify an attribute that cannot be specified by the user 
// *Action: Remove the mentioned attribute, and re-issue the command.
6505, 1, "Format of the EXPRESSION attribute '%s' is invalid"
// *Cause: The EXPRESSION attribute is invalid.
// *Action: Provide a valid value for the EXPRESSION attribute.
// Msg 6506 continued in msg 6562
6506, 3, "Sample EXPRESSION:\n1. MEMORY_SIZE > 2\n2. ((CPU_COUNT > 4) OR (CPU_CLOCK_RATE = 10)) \n\nExpression Operators: =, >, <, !=,st, en, co, nc, coi, nci, eqi\n\twhere\n\t\tst  --> starts with\n\t\ten  --> ends with\n\t\tco  --> contains\n\t\tnc  --> does not contain\n\t\tcoi --> contains, case-insensitive\n\t\tnci -->"
6507, 3, "\n     -s               Server pool names (e.g. -s  pool1 pool2)\n" 
// Msg 6508 continued in msg 6563
6508, 3, " crsctl request action <actionName> {-r <resName>[...]|-w <filter>} [-env \"env1=val1,env2=val2,...\"] [-i]\n     Request the specified action\nwhere\n      actionName       Action to be requested\n      resName [...]    One or more blank-separated resource names\n      -w               Resource filter\n"
6509, 3, "  crsctl restart resource {<resName> [...]|-w <filter>} [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]  \n     Restart designated resources\nwhere"
6510, 3, "     resName [...]    One or more blank-separated resource names\n     -w               Resource filter (e.g., \"TYPE = ora.database.type\")\n     -k               Resource cardinality ID"
6511, 3, "     -d               Resource degree ID\n     -env             Attribute overrides for this command\n     -f               Force option\n     -i               Fail if request cannot be processed immediately\n"
6512, 3, "  crsctl restart resource {<resName> [...][-w <filter>] [-k <cid>] [-d <did>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i] "
6513, 0, "Resource is enabled."
6514, 0, "Resource is disabled."
// Msg 6515 continued in msg 6564
6515, 0, "where \n     spName          Modify named server pool attributes\n     attrName        Attribute name\n     value           Attribute value\n     policyName      Policy whose serverpool definition needs to be modified\n     -all_policies   Modify serverpool definition for all policies\n     -f              Force option"
6516, 3, "  crsctl query credentials -target <target>\n     Lists the valid credentials under a specific target"
6517, 3, "  crsctl add credentials -target <target> [[-user <user_name>] [-passwd]|[-keylength <nbits>]]\nwhere\n     target        Target as is listed by 'crsctl query credentials targetlist'\n     user_name     User to be added to wallet. If not specified, will \n                   be pseudo-randomly generated. Can only be specified with 'userpass' credentials."
// Msg 6518 continued in msg 6565
6518, 3, "     -passwd       Indication that password will be specified. Password \n                   will be read from standard input. If not specified, \n                   will be pseudo-randomly generated. Can only be specified with 'userpass' credentials.\n     nbits         Length of the key. If not specified, defaults to 128. "
6519, 3, "  crsctl query credentials targetlist\n     Lists the valid credentials targets to be used with credentials commands"
6520, 3, "Sample command: crsctl add category large -attr \"EXPRESSION='(CPU_COUNT > 3)'\"" 
6521, 3, "Sample command: crsctl modify category large -attr \"EXPRESSION='(CPU_COUNT > 3)'\"" 
6522, 3, "  crsctl eval add {resource|resourcegroup|server|serverpool} <name> <options>" 
6523, 3, "  crsctl eval modify {resource|resourcegroup|serverpool} <name> <options>"
6524, 3, "  crsctl eval delete {server|serverpool} <name> <options>"
6525, 3, "  crsctl eval start {resource|resourcegroup}  <name> <options>"
6526, 3, "  crsctl eval stop {resource|resourcegroup}  <name> <options>"
6527, 3, "  crsctl eval relocate {resource|resourcegroup|server} <name> <options>"
6528, 3, "  crsctl eval fail {resource|resourcegroup}  <name> <options>"
6529, 3, "  crsctl eval activate policy <name> <options>"
6530, 1, "cannot set node role because cluster is not configured in \"flex\" mode"
// *Cause: An attempt to set a node's role using 'crsctl set node role' was rejected because the cluster is not running in \"flex\" mode. Node roles can only be set for nodes in \"flex\" clusters.
// *Action: Reissue the command after the cluster is configured in \"flex\" mode."
/ Generic version mismatch error 
6531, 0, "Issued command is not supported in this version of CRS."
// *Cause: The command was rejected because the related feature is not supported in this release. 
// *Action: If this error occurred during rolling upgrade, wait for the upgrade to finish. Otherwise, upgrade to the required release or higher.
// Msg 6532 continued in msg 6566
6532, 3, "  crsctl get css noautorestart\n    List the problems for which automatic restart of Cluster Synchronization Services is disabled.\n\nPossible responses are:\n     all              Auto restart is disabled for any problem.\n     interconnect     Auto restart is disabled when an interconnect problem occurs.\n"
// Msg 6533 continued in msg 6567
6533, 3, "  crsctl set css noautorestart {all|interconnect|vf|none}\n    Stop the automatic restart of  Cluster Synchronization Services when a specific problem occurs.\n\nPossible problems are:\n     all              Disable auto restart when there is any problem occurring.\n     interconnect     Disable auto restart when an interconnect problem occurs.\n"
6534, 3, "Current SUPPRESS_AUTO_RESTART parameter value is %s."
6535, 0, "Cannot restart resource '%s' as a part of a dependency because the auto start capability of this resource has been disabled."
// *Cause: An attempt was made to start a resource due to a dependency requirement, but the resource could not be started automatically because the auto start capability of this resource was disabled.
// *Action: Enable auto start for the resource.
6536, 3, "  crsctl get cluster type\n   Display the type of resources the current cluster can run."
6537, 0, "The cluster type has been set to '%s'.\n"
6538, 1, "Could not set the cluster type to '%s'. The cluster type has already been set."
// *Cause: An attempt was made to change the cluster type, which has already been set. The cluster type can only be set once.
// *Action: Restart the cluster to reset its type.
6539, 0, "The cluster type is '%s'.\n"

/
/ crsctl split long messages : bug 20995151
/
6540, 3, "     -i                 Fail if request cannot be processed immediately\n     -env               Override environment values for this command\n     resourceGroupName  Resource group name"
6541, 3, "     -f             Force option\n     -i             Fail if request cannot be processed immediately"
6542, 3, "     -p                Print static configuration\n     -v                Print runtime configuration\n"
6543, 3, "     user_name       User whose password is to be modified.\n     passwd          Password will be read from standard input."
6544, 3, "   user_name     User name to be added to the admin list or \"*\"\n   -f            Override user name validity check"
6545, 3, "   options       Options to be passed to the add command"
6546, 3, "     -wait        Wait until startup is complete and display all progress and status messages"
6547, 3, "    -leaf           Start leaf nodes\n    -w              Start only servers that match a filter (e.g., \"ACTIVE_CSS_ROLE = hub\")\n"
6548, 3, "     -env             Attribute overrides for this command\n     -f               Force option\n     -i               Fail if request cannot be processed immediately"
6549, 3, "    -leaf           Stop leaf nodes\n    -w              Stop only servers that match a filter (e.g., \"ACTIVE_CSS_ROLE = hub\")\n    -f              Force option\n"
6550, 3, "     user_name       User to be queried from wallet.\n     all             List all users in wallet"
6551, 3, "     -k               Resource cardinality ID\n     -d               Resource degree ID"
6552, 0, "For detailed help on each command and object and its options use:\n    crsctl <command> <object> -h  e.g. crsctl relocate resource -h"
6553, 3, " contains, case-insensitive\n\t\tnci --> does not contain, case-insensitive\n\t\teqi --> equals, case-insensitiv\n\nSample command: crsctl status category -w \"TYPE = type1\""
6554, 3, " contains, case-insensitive\n\t\tnci --> does not contain, case-insensitive\n\t\teqi --> equals, case-insensitiv\n\nSample command: crsctl status server -w \"TYPE = type1\"" 
6555, 3, "      subnet           The subnet on which DHCP release lease packets will be sent\n"
6556, 3, "    port                The port on which the listener will listen. Default value is 53.\n    domain              The domain query for which to listen. By default, all domain queries are processed."
6557, 3, "    DNS_server_address  Address of the DNS server on which name needs to be looked up" 
6558, 3, "     -dependency       Display resource dependencies, default is start dependencies\n     -stop             Display resource stop dependencies\n     -pullup           Display resource pullup dependencies"
6559, 3, "   ctss          Cluster Time Synchronization Service\n   evm           EventManager\n   gipc          Grid Interprocess Communications\n   <name1>, ...    Module names (\"all\" for all names)"
6560, 3, "   ctss          Cluster Time Synchronization Service\n   evm           Event Manager\n"
6561, 3, "     xmlfile       Path to XML file to which credentials will be written.\n     sectionName   Section name.\n"
6562, 3, " does not contain, case-insensitive\n\t\teqi --> equals, case-insensitive\n\n" 
6563, 3, "      -env             Attribute overrides for this command\n      -i               Fail if request cannot be processed immediately\n"
6564, 0, "     -i              Fail if request cannot be processed immediately"
6565, 3, "                   Can only be specified with 'keypair' credentials."
6566, 3, "     vf               Auto restart is disabled when a voting files problem occurs.\n     none             Auto restart is enabled in all cases."
6567, 3, "     vf               Disable auto restart when a voting files problem occurs.\n     none             Enable Cluster Synchronization Services auto restart."
6568, 3, "     filter_expression\tRefer to product documentation.\n    -follow\t\tGives continuous output\n    -fullfmt\t\tDetail output format\n    -xmlfmt\t\tXML output format\n"
6569, 3, "     -f               Force option\n     -i               Fail if request cannot be processed immediately\n"
6570, 3, "     -p                Print static configuration\n     -v                Print runtime configuration\n"
6571, 3, "     -stop             Display resource group stop dependencies\n     -pullup           Display resource group pullup dependencies"
6572, 3, "     -f             Force option\n     -i             Fail if request cannot be processed immediately"
6573, 1, "cannot set node role because GNS is not configured in the cluster"
// *Cause: An attempt to set a node's role using 'crsctl set node role' was rejected because the cluster was not configured with GNS. Node roles can only be set to leaf if GNS is configured.
// *Action: Reissue the command after configuring GNS in the cluster.


/
/ Extended cluster
/
6574, 3, "  crsctl get cluster extended\n   Display whether the current cluster is extended."
6575, 3, "  crsctl query cluster site {<site_name> | -all}\n     List the nodes and disks that the sites contain. \nWhere\n       site_name             The site name to be queried\n       -all                  List all sites."
6576, 3, "  crsctl query crs site {-n <node_name> | -d <disk_name>}\n     List the site to which the node or disk belongs. \nWhere\n     node_name       The name of the node to be queried\n     disk_name       The name of the disk to be queried\n"
6577, 0, "The cluster is extended.\n"
6578, 0, "Site '%(1)s' identified by GUID '%(2)s' in state '%(3)s' contains nodes '%(4)s' and disks '%(5)s'.\n"
6579, 0, "The cluster is not extended.\n"
6580, 0, "Node '%s' belongs to site '%s'.\n"
6581, 1, "Node '%s' does not belong to any site."
// Cause:  An attempt to query a node failed because the indicated name did not
//         belong to any site.
// Action: Issue the command 'olsnodes' to retrieve the list of the nodes in the
//         cluster.
6582, 0, "Disk '%s' belongs to site '%s'.\n"
6583, 1, "Disk '%s' does not belong to any site."
// Cause:  An attempt to query a disk failed because no disk with the indicated 
//         name could be found on any site.
// Action: Issue the command 'asmcmd lsdsk' to retrieve the list of the disks in
//         the cluster.
6584, 0, "Site '%(1)s' identified by GUID '%(2)s' in state '%(3)s' contains nodes '%(4)s' and no disk.\n"
6585, 0, "Site '%(1)s' identified by GUID '%(2)s' in state '%(3)s' contains disks '%(4)s' and no nodes .\n"
6586, 0, "Site '%(1)s' identified by GUID '%(2)s' in state '%(3)s' contains no nodes and no disks\n"


6590, 3, "  crsctl add cluster site <site_name> [-guid <site_guid>]\n     Add the site to the cluster. \nWhere\n       site_name             The site name of the new site\n       site_guid             The site GUID (global unique ID) of the new site \n"
6591, 3, "  crsctl delete cluster site <site_name>\n     Delete the site from the cluster. \nWhere\n       site_name             The site name of the site to be deleted\n"
6592, 1, "Site '%s' cannot be added, deleted or quarantined because the cluster is not operating in extended mode."
// Cause:  An attempt to add, delete or quarantine a site was rejected because
//         the cluster was not operating in extended mode.         
// Action: Reconfigure the cluster in extended mode.
6593, 1, "Site '%s' cannot be deleted because the site still has nodes."
// Cause:  An attempt to delete a site was rejected because there were nodes 
//         present on that site.
// Action: Delete the cluster nodes from the site before deleting the site.
6594, 1, "Site '%s' cannot be deleted because the site still has disks."
// Cause:  An attempt to delete a site was rejected because there were disks
//         present on that site.
// Action: Delete the disks from the site before deleting the site.
6595, 3, "  crsctl modify cluster site <site_name> {-n <node>[...]|-s {rejuvenate|quarantine}|-l} \nwhere \n    site_name   Name of site to be modified\n    -n          Node change option\n    node [...]  The set of hosts to associate with the indicated site\n    -s          State change option\n    rejuvenate  Unquarantine the site\n    quarantine  Quarantine the site\n    -l          Change the site associated with the local node"
6596, 3, "  crsctl set cluster name <value>\n    Sets the cluster name"
6599, 1,   "cannot set the node's role to Leaf on an extended cluster"
// *Cause:  An attempt to set a node's role to Leaf was rejected
//          because the cluster was configured as an extended cluster
//          where only Hub Nodes were supported.
// *Action: None.
/
/ crsctl credential message 6600-6700
/
6600, 0, "Enter password:"
6601, 0, "Added credential set member %d"
6602, 1, "No password specified.\n"
// *Cause:  A password was not entered in response to the password prompt.
// *Action: Enter a password.
6603, 1, "Cannot modify '%s' policy."
// *Cause: An attempt was made to modify a read-only policy.
// *Action: Specify a policy that is not read-only.

/
/ crsctl start messages 6701-6720. Continued from 4116 - 4125
/
6701, 0, "  crsctl start rollingpatch"
6702, 0, "  crsctl start rollingpatch\n    Transition Oracle Clusterware and Oracle ASM to rolling patch mode"

6703, 0, "  crsctl start rollingupgrade <version>"
6704, 0, "  crsctl start rollingupgrade <version>\n    Transition Oracle Clusterware and Oracle ASM to rolling upgrade mode"

6705, 1, "Oracle Clusterware Release Version ('%s') does not match Software Version ('%s'). Oracle Clusterware cannot be started."
// *Cause: Oracle Clusterware was started from an older home that has since been upgraded.
// *Action: Start Oracle Clusterware from the upgraded home. Also, check the CRS home configured in olr.loc and the /etc/init.d/ohasd script to make sure they have not been accidentally changed.
6706, 1, "Oracle Clusterware Release patch level ('%u') does not match Software patch level ('%u'). Oracle Clusterware cannot be started."
// *Cause: Oracle Clusterware was started from an older home that has since been patched. 
// *Action: Start Oracle Clusterware from the patched home. Also, check the CRS home configured in olr.loc and the /etc/init.d/ohasd script to make sure they have not been accidentally changed.
6707, 1, "init.ohasd is not running."
// *Cause: Oracle High Availability Services startup failed because there was no init.ohasd running.
// *Action: 1. Check the run level to ensure that you are in the correct runlevel using cluvfy ("cluvfy stage -pre crsinst -n <nodelist>"); 2. If the run level is correct, diagnose the reason for init.d not starting init.ohasd.

/
/ crsctl stop messages 6721-6740. Continued from 4126 - 4135
/
6721, 0, "  crsctl stop rollingpatch"
6722, 0, "  crsctl stop rollingpatch\n    Transition Oracle Clusterware and Oracle ASM out of rolling patch mode"
6723, 3, "  crsctl get cluster name\n    Displays the current cluster name"
6724, 3, "Current cluster name is '%s'"
/
/
/ crsctl query messages 6741-6760. Continued from 4170 - 4178. Continued 41001 - 42000
/
6741, 0, "  crsctl query crs releasepatch"
6742, 0, "  crsctl query crs releasepatch\n     Lists the Oracle Clusterware release patch level"
6743, 0, "  crsctl query crs softwarepatch [<host>]"
6744, 0, "  crsctl query crs softwarepatch [<host>]\n     Lists the patch level of Oracle Clusterware software installed\nwhere\n     Default         List software patch level of the local host\n     host            List software path level of the named host"
6745, 0, "  crsctl query has releasepatch"
6746, 0, "  crsctl query has releasepatch\n     Lists the Oracle Clusterware release patch level"
6747, 0, "  crsctl query has softwarepatch"
6748, 0, "  crsctl query has softwarepatch\n     Lists the patch level of Oracle Clusterware software installed on the local host"
6749, 0, "unable to get the software version"
// *Cause:  The crsctl query failed because the software version could not be retrieved. Either the clusterware stack was down, or the user was not root (UNIX) or Administrator (WINDOWS).
// *Action: Bring up the clusterware stack or run the query as a privileged user. 
6750, 0, "unable to get the active version"
// *Cause:  The crsctl query failed because the active version could not be retrieved.  Either the clusterware stack was down, or the user was not root (UNIX) or Administrator (WINDOWS).
// *Action: Bring up the clusterware stack or run the query as a privileged user. 
6751, 0, "unable to get the software patch version"
// *Cause:  The crsctl query failed because the software patch version could not be retrieved.  Either the clusterware stack was down, or the user was not root (UNIX) or Administrator (WINDOWS).
// *Action: Bring up the clusterware stack or run the query as a privileged user. 
6752, 0, "Active version query failed."
// *Cause: The crsctl query failed because the active version could not be retrieved.
// *Action: See the accompanying error message and respond. 
6753, 0, "Software patch query failed."
// *Cause: The crsctl query failed because the software patch version could not be retrieved. 
// *Action: See the accompanying error message and respond. 
6754, 0, "Software version query failed for node %s."
// *Cause: The crsctl query failed to retrieve the software version. 
// *Action: See the accompanying error message and respond. 
6755, 3, "  crsctl query calog [-aftertime <after_timestamp>] [-beforetime <before_timestamp>] [-duration <time_interval> | -follow] [-filter <filter_expression>] [-fullfmt | -xmlfmt]\n     Lists the cluster activity log activities matching the specified criteria"
6756, 3, "  crsctl set calog <parameter> <value> [-f]\n    Sets the value of an Oracle cluster activity log parameter"
6757, 3, "  crsctl set calog <parameter> <value> [-f]\n    Sets the value of an Oracle cluster activity log parameter\n\n    Following are the valid parameters:\n    maxsize              - Maximum size of the cluster activity log in megabytes\n    retentiontime        - Retention time of the cluster activity log in hours\n   -f                    - Force option"
6758, 3, "  crsctl get calog <parameter> \n    Gets the value of an Oracle cluster activity log parameter"
6759, 3, "  crsctl get calog <parameter> \n    Gets the value of an Oracle cluster activity log parameter\n\n    Following are the valid parameters:\n    maxsize              - Maximum size of the cluster activity log\n    retentiontime        - Retention time of the cluster activity log"
6760, 3, "The maximum size of the Oracle cluster activity log is %d MB."

// WLM QoS Msgs

6761, 1,  "Invalid value for QoS Management policy management key '%s' in OCR."
// *Cause:  An invalid value for Quality of Service Management policy management key was found in the OCR.
// *Action: Contact Oracle Support Services.
6762, 0,  "Unable to use CRSCTL for Policy Management because Quality of Service Management (QoS) is managing the Clusterware policies." 
// *Cause: CRSCTL cannot be used for Policy Management because Quality of Service Management is configured to manage Clusterware policies. 
// *Action: Use Quality of Service Management for Policy Management.

6763, 0, "Maximum size specified for the cluster activity log is non-numeric."
// *Cause: A non-numeric value was specified for the maximum size of the cluster activity log. 
// *Action: Specify a maximum size that is a numeric value.
// Msg 6764 continued in msg 6568
6764, 3, "Where\n     after_timestamp\tTime in format \"YYYY-MM-DD HH24:MI:SS[.FF][TZH:TZM]\" OR \"YYYY-MM-DD\" OR \"HH24:MI:SS[.FF][TZH:TZM]\"\n     before_timestamp\tTime in format \"YYYY-MM-DD HH24:MI:SS[.FF][TZH:TZM]\" OR \"YYYY-MM-DD\" OR \"HH24:MI:SS[.FF][TZH:TZM]\"\n     time_interval\tTime interval in format \"DD HH:MM:SS\"\n"

/ Get/Set tracefileopts, other crsctl commands 6770 - 6780.
/ Continued from 4900 - 4980
/
6770, 3, "  crsctl set tracefileopts {mdns|gpnp|css|crf|crs|ctss|evm|gipc} [-filesize <file_size>[K|k|M|m|G|g]] [-numsegments <num_of_segments>]\n  Note: You must specify at least one of the clauses -filesize or -numsegments"
6771, 0, "An invalid value was specified for argument %s."
// *Cause: Invalid values were specified on the command line for the argument.
// *Action: Provide a positive non-zero integer value for the mentioned argument.
6772, 3, "  crsctl get tracefileopts {mdns|gpnp|css|crf|crs|ctss|evm|gipc}"
6773, 0, "Value out of range for argument %s."
// *Cause: An attempt to modify trace file options specified a value out of range. 
//         Either the value for the -filesize keyword was less than 1MB or greater than 
//         2GB or the value for the -numsegments keyword was greater than 4294967295.
// *Action: Specify a valid value for the identified keyword and retry the command. 
6774, 0, "Get %s: Trace File Options: %s "
6775, 1, "Daemon %s: Get trace file options request failed."
// *Cause: An unexpected internal error occurred.
// *Action:  Contact Oracle Support Services.
6776, 1, "Daemon %s: Set trace file options request failed."
// *Cause: An unexpected internal error occurred.
// *Action:  Contact Oracle Support Services.
6777, 1, " The command '%s' cannot be used for entity names starting with 'ora.'."
// *Cause: An attempt was made to use an unsupported entity name in CRSCTL.
// *Action: Provide an entity name that does not start with 'ora.'.

/ Retention time APIs for Calog 6781 - 6790
6781, 3, "The retention time of the cluster activity log is %d hours."
6782, 0, "Retention time specified for the cluster activity log is non-numeric."
// *Cause: A non-numeric value was specified for the retention time of the cluster activity log. 
// *Action: Specify a retention time in hours that is numeric.
6783, 1,   "cannot set the node's role to Leaf on a %s "
// *Cause:  An attempt to set a node's role to Leaf was rejected because the
//          cluster configuration supports only Hub nodes. 
// *Action: None.



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
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
/

7001, 1,  "Generic GPnP error"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
/

7002, 1, "Not enough memory"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
/

7003, 1, "GPnP facility initialization failed"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
/

7004, 1, "This feature is unsupported or not implemented"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/
 
7005, 1, "Requested item not found"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7006, 1, "Insufficient buffer size"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7007, 1, "Error in file I/O operation"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7008, 1, "Invalid permissions for the operation"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7009, 1, "Bad authority id"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7010, 1, "Key does not exist"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7011, 1, "Bad key"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7012, 1, "Hostname not found"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7013, 1, "GPNPD daemon is not running"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7014, 1, "Attempting to set a bad value"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7015, 1, "Bad hostname value"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7016, 1, "Bad authority id value"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7017, 1, "Not a cluster member"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7026, 1, "Profile is not given or not available"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7027, 1, "Badly formed profile"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7028, 1, "Profile is too big to be valid"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7029, 1, "Profile is older than the current"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7030, 1, "Profile exists in memory only, not saved"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7031, 1, "Request retry message from GPNPD"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7032, 1, "Value already set in profile"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7033, 1, "Request timed out"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7041, 1, "GPnP XML profile is not well formed"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7042, 1, "Invalid GPnP SOAP message"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7048, 1, "Communication error"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7054, 1, "Invalid URL for discoverable resource"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

// 7055, UNUSED
// *Cause: 
// *Action: 
// This error message is not used.
/

7056, 1, "OCR Init error"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7057, 1, "Reinit OCR to a different bootlevel"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7058, 1, "OCR error"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7059, 1, "Global OCR is not available"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7066, 1, "Requested GPnP wallet is not found"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7067, 1, "Invalid GPnP wallet password given"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7068, 1, "GPnP wallet is too big to be valid"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7069, 1, "GPnP wallet is corrupted or invalid"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7070, 1, "Bad or missing private key in GPnP wallet"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7071, 1, "Bad or missing public key in GPnP wallet"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7072, 1, "Bad or missing certificate in GPnP wallet"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7077, 1, "Crypto library error"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
/

7086, 1, "GPnP profile signature invalid" 
// *Cause:  This is an internal error.   
// *Action: Contact Oracle Support Services.
/

7087, 1, "GPnP profile valid peer signature"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7088, 1, "GPnP profile valid PA signature"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7089, 1, "GPnP profile was signed with a different wallet"
// *Cause:  This is an internal error. 
// *Action: Contact Oracle Support Services.
/

7090, 1, "Grid Naming Service (GNS) error"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
/

7091, 1, "Unable to contact Grid Naming Service (GNS)"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
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
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
/

7096, 1, "GPnP tool version"
// *Cause:  This is an internal error.
// *Action: Contact Oracle Support Services.
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
// Eval messages (continued) (8200 - 8299)
/
8201, 3, "where\n     spName         Name of the server pool\n     -explain       Generate a detailed explanation plan for the command.\n"
8202, 3, "\nwhere\n     resName        Name of a resource\n     -all           Relocate all resources\n     -s             Source server\n     -w             Resource filter (e.g., \"TYPE = ora.database.type\")\n     -n             Destination server\n     -f             Evaluate as with force option\n"
8203, 3, "where\n     serverName     Name of the server\n     toPool         ServerPool to add the server to\n     -f             Evaluate as with force option"
8204, 3, "where\n     resName            Name of the resource\n     attrName           Attribute name\n     value              Attribute value\n     resourceGroupName  Resource group\n     -f                 Evaluate as with force option\n"

8205, 3,"Considering server pool '%s' because its MIN_SIZE is %s and it has %s servers above MIN_SIZE."
8206, 3,"Considering server pools (IMPORTANCE): %s for suitable servers." 
8207, 3,"Rejected server pool '%s'." 
8208, 3,"Selected server pool '%(1)s' to contain server '%(2)s'." 
8209, 3,"Scanning server pools with fewer than MIN_SIZE servers in ascending order of IMPORTANCE."
8210, 3,"Scanning server pools with MIN_SIZE or more servers in ascending order of IMPORTANCE."
8211, 3,"Selected server '%(1)s' to move into pool '%(2)s'."
8212, 3,"Relocating server '%(1)s' to server pool '%(2)s'."
8213, 3,"Rejected server '%s'."
8214, 3,"Removing server '%(1)s' from server pool '%(2)s'."
8215, 3,"Server pool '%(1)s' is below the MIN_SIZE value of %(2)s with %(3)s servers."
8216, 3,"Invalid rejection code received from policy engine: %s. Contact Oracle Support Services for more help."
// *Cause:  CRSCTL client received an invalid rejection code.  
// *Action: Report the accompanying warning  to Oracle Support Services.
8217, 3,"Scanning server pools with fewer than MIN_SIZE servers in descending order of IMPORTANCE."
8218, 3,"Scanning server pools with MIN_SIZE or more servers in descending order of IMPORTANCE."
8219, 3,"Server '%(1)s' is removed from server pool '%(2)s'."
8220, 3,"Server '%s' is online."
8221, 3,"Scanning server pools with more than MIN_SIZE servers in ascending order of IMPORTANCE."
8222, 3,"Scanning server pools with MIN_SIZE or fewer servers in ascending order of IMPORTANCE."
8223, 3,"Rejected server pool '%s'. Server pool is at its MIN_SIZE value of %s."
8224, 3,"Server pool '%(1)s' cannot contain server '%(2)s' because it is at its MAX_SIZE value of %(3)s."
8225, 3,"Server pool '%(1)s' cannot contain server '%(2)s' because the server is not in server category '%(3)s'."
8226, 3,"Server pool '%(1)s' cannot contain server '%(2)s' because the server is not in PARENT_POOL."
8227, 3,"Server pool '%(1)s' cannot contain server '%(2)s' because the server is not in SERVER_NAMES."
8228, 3,"Server pool '%(1)s' cannot contain server '%(2)s' because the server pool belongs to EXCLUSIVE_POOLS."
8229, 3,"Rejected server pool '%s'. No privilege to act on this server pool."
8230, 3,"Removing server '%(1)s' from server pool '%(2)s'. MIN_SIZE has changed."
8231, 3,"Server pool '%(1)s' cannot contain server '%(2)s' because its current size %(3)s exceeds its MAX_SIZE %(4)s."
8232, 3,"Removing server '%(1)s' from server pool '%(2)s'. SERVER_CATEGORY has changed."
8233, 3,"Removing server '%(1)s' from server pool '%(2)s'. SERVER_NAMES has changed."
8234, 3,"Removing server '%(1)s' from server pool '%(2)s'. EXCLUSIVE_POOLS has changed."
8235, 3,"Removing server '%(1)s' from server pool '%(2)s'. PARENT_POOLS has changed."
8236, 3,"Rejected server pool '%s' because no more servers are needed."
8237, 3,"Rejected server pool '%s' because server pool is below its MIN_SIZE value of %s."
8238, 3,"Rejected server pool '%s' because server pool is empty."
8239, 3,"Rejected server pool '%s' because it is already at its MIN_SIZE value of %s and its IMPORTANCE value of %s is not less than that of server pool '%s'."
8240, 3,"Rejected server pool '%s' because it is below its MIN_SIZE value of %s and it's IMPORTANCE value of %s is not less than that of server pool '%s'."
8241, 3,"Rejected server '%s' because server is not in PARENT_POOL."
8242, 3,"Rejected server '%s' because server is exclusive and in a server pool."
8243, 3,"Rejected server '%s' because server not in SERVER_NAMES."
8244, 3,"Server '%(1)s' does not belong to server category '%(2)s'."
8245, 3,"Rejected server pool '%s'. Server pool is at or below its MIN_SIZE value of %s."
8246, 3,"Rejected server '%s' because server pool is at its MAX_SIZE."
8247, 3,"Rejected server pool '%s' because server is exclusive and in a pool."
8248, 3,"Starting to look for servers to meet the MIN_SIZE value of %s."
8249, 3,"Rejected server '%s' because server belongs to EXCLUSIVE_POOLS."
8250, 3,"Rejected server pool '%s' because server pool is more important."
8251, 3,"Starting to look for servers to meet the MAX_SIZE value of %s."
8252, 3,"Server pool '%(1)s' is at or below the MAX_SIZE value of %(2)s with '%(3)s' servers."
8253, 3,"Starting to look for server pools to reallocate servers from pool '%s'."
8254, 3,"Checking whether server pool '%(1)s' can consume server '%(2)s'." 
8255, 3,"Looking for a suitable server pool for server '%s'."
8256, 3,"Server pool '%(1)s' cannot donate server '%(2)s' because the server is not in server category '%(3)s'."
8257, 3,"Server pool '%(1)s' cannot contain server '%(2)s' because the server is not in server category '%(3)s' which is based on attribute %(4)s."
8258, 3,"Server pool '%(1)s' cannot donate server '%(2)s' because the server is not in server category '%(3)s' which is based on attribute %(4)s."
8259, 3,"Starting to look for server pools that will donate servers to be reallocated to the new pool '%s'."
8260, 3,"Starting to look at server pools due to a configuration change in the pool '%s'."
8261, 3,"Looking at other server pools to see whether MIN_SIZE value %(1)s of server pool '%(2)s' can be met."
8262, 3,"Server '%(1)s' can no longer be assigned to server pool '%(2)s' because the server is not in PARENT_POOL."
8263, 3,"Server '%(1)s' can no longer be assigned to server pool '%(2)s' because the server is not in SERVER_NAMES."
8264, 3,"Server '%s' can no longer be assigned to server pool '%s' because the server is not in server category '%s'."
8265, 3,"Server '%(1)s' can no longer be assigned to server pool '%(2)s' because the server is not in server category '%(3)s' which is based on attribute %(4)s."
8266, 3,"Starting to evaluate activation of policy '%(1)s' with server pools (MIN_SIZE, MAX_SIZE) '%(2)s'."
8267, 3,"Resource group '%s' (%s) will be in state '%s'."
8268, 3,"Resource group '%s' (%s) will be in state '%s' on server '%s'."
8269, 3, "where\n     serverName     Name of the server\n"
8270, 3,"Considering server pools (IMPORTANCE): %s for relocating servers." 
8271, 3, "invalid flag or combination of flags given for the 'eval' command"
// *Cause: The 'crsctl eval' command was executed with an invalid combination of flags.
// *Action: Reexecute the command with a valid combination of flags.
8272, 3,"Rejected server pool '%(1)s' because its IMPORTANCE value of %(2)s is not less than that of server pool '%(3)s' and server pool '%(4)s' is at or above its MIN_SIZE value of %(5)s."


///////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////
/
// Clsuterware process infrastructure (CLSB) messages (8500-8999)
/
///////////////////////////////////////////////////////////////////////

/ Alert
08500, 0, "Oracle Clusterware %s process is starting with operating system process ID %s"
// *Cause:  The indicated service or component of Oracle Clusterware
//          began execution.
// *Action: None.
/ Alert
08501, 0, "Oracle Clusterware %s process with operating system process ID %s is ending with return value %d"
// *Cause:  The indicated service or component of Oracle Clusterware
//          ended execution.
// *Action: None.
/ Alert
08502, 0, "Oracle Clusterware %s process with operating system process ID %s failed in initialization"
// *Cause:  The indicated service or component of Oracle Clusterware
//          was unable to complete initialization.
// *Action: Report this error to Oracle Support Services.
/ Alert
08503, 0, "Oracle Clusterware process %s with operating system process ID %s experienced fatal signal or exception code %s."
// *Cause:  The indicated service or component of Oracle Clusterware
//          encountered a fatal exception.
// *Action: Report this error to Oracle Support Services.
/ Alert
08504, 0, "Oracle Clusterware %s process with operating system process ID %s is exiting"
// *Cause:  The indicated service or component of Oracle Clusterware
//          ended execution using the operating system 'exit' function.
// *Action: None.
/ Alert
08505, 0, "Oracle Clusterware %s process with operating system process ID %s encountered internal error %s-%05d"
// *Cause:  The indicated service or component of Oracle Clusterware
//          encountered an internal error, causing an ADR incident to
//          be raised.
// *Action: Contact Oracle Support Services and report the internal error
//          code displayed in the message.
/

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

9003, 0, "Cluster Health Monitor is not supported in this configuration."
// *Cause: Grid Infrastructure Management Repository was not configured.
// *Action: Re-Install Grid Infrastructure and ensure that Grid Infrastructure
//          Management Repository is configured.

9004, 0, "Error reading from standard input"
// *Cause: Could not read commands from the command line.
// *Action: Report this error to Oracle Support Services.

9005, 0, "Quoted string not ended"
// *Cause: An unmatched " was found in the command entered.
// *Action: Put in the corresponding quote or remove the unmatched quote.

9006, 0, "Could not set environment, exiting."
// *Cause: Error occurred during initialization of oclumon.
// *Action: Report this to Oracle Support Services.

9007, 0, "failed to contact 'osysmond' daemon"
// *Cause: An attempt to get cluster mode was unable to contact the 'osysmond'
//         daemon.
// *Action: Ensure that the ora.crf resource is running and, if not, start it.

9008, 0, "Unknown verb %s"
// *Cause: Unknown or invalid verb passed to oclumon.
// *Action: Use 'oclumon -h' in command line or help command in interactive mode
//          to see the supported verbs.

9009, 0, "Error %s: Parsing error. Invalid arguments specified."
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
//          client node by using the 'ping' command for the specified node.

9013, 0, "Error %s: Invalid data received from the Cluster Logger Service"
// *Cause: Invalid or unknown data received from the Cluster Logger Service.
// *Action: Ensure that the Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the specified node.

9014, 0, "Error: Corrupt reply from the Cluster Logger Service"
// *Cause: Invalid or unknown data received from the Cluster Logger Service.
// *Action: Make sure that the version of both master and client installation
//          is same. Also, check the connectivity between master and client
//          using the 'ping'.

9015, 0, "Error %s: Connection timed out"
// *Cause: Connection timed out while connecting to the Cluster Logger Service.
// *Action: Ensure that the Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the specified node.

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

9020, 0, "Error %s: No master node name specified"
// *Cause: The master node name was not specified in the command.
// *Action: Pass the appropriate master node name with the command.

9021, 0, "Error %s: Invalid or no start time specified"
// *Cause: A start time was not specified or the time was passed in 
//         the wrong format.
// *Action: Pass the correct start time. For correct format, refer to 
//          command help.

9022, 0, "Error %s: Invalid or no end time specified"
// *Cause: A end time was not specified or the time was passed in 
//         the wrong format.
// *Action: Pass the correct end time. For correct format, refer to 
//          command help.

9023, 0, "Error %s: Time not specified or in wrong format or invalid"
// *Cause: Time was not specified or was invalid.
// *Action: Pass the correct and valid time. For correct format, refer to command
//          help.

9024, 0, "Error %s: No node name specified"
// *Cause: Node name not specified.
// *Action: Provide a node name in the command. Refer to the product
//          documentation or to the command online help for information.

9025, 0, "Error %s: No disk ID name specified"
// *Cause: Disk ID was not specified in the command with -diskid.
// *Action: Pass a valid disk ID with -diskid option.

9026, 0, "Error %s: No parameter specified"
// *Cause: The parameter was not specified in the query.
// *Action: Pass appropriate parameter for query. Refer to the product
//          documentation or to the command online help for information.

9027, 0, "Error %s: Parameter %s is not supported with this verb"
// *Cause: Invalid or unknown parameter passed.
// *Action: Pass the correct parameter. Refer to the product
//          documentation or to the command online help for information.

9028, 0, "Error %s: No NIC ID specified"
// *Cause: NIC ID was not specified in the command with -nicid.
// *Action: Pass a valid NIC ID with -nic option.

9029, 0, "Error %s: No PID specified"
// *Cause: PID was not specified in the command with -pid.
// *Action: Pass a valid PID with -pid option.

9030, 0, "Error %s: No region specified"
// *Cause: Incorrect or no region specified with -c option.
// *Action: Pass a valid region with -c option. Refer to the product
//          documentation or to the command online help for information.

9031, 0, "Error %s: Argument %s not supported with this verb"
// *Cause: Unknown or invalid argument passed with the command.
// *Action: Refer to the product documentation or to the command 
//          online help for information on supported arguments.

9032, 0, "Invalid hour specified in the time argument"
// *Cause: Invalid hour in the time string was passed.
// *Action: Pass a valid time string in accordance with the format. 
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9033, 0, "Invalid minutes specified in the time argument"
// *Cause: Invalid minutes in the time string was passed.
// *Action: Pass a valid time string in accordance with the format. 
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9034, 0, "Invalid seconds specified in the time argument"
// *Cause: Invalid seconds in the time string was passed.
// *Action: Pass a valid time string in accordance with the format. 
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9035, 0, "Arguments not in proper format, or invalid arguments"
// *Cause: Invalid arguments specified. 
// *Action: Pass  a valid verb and correct arguments for it.
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9036, 0, "Invalid Cluster Health Monitor repository size specified"
// *Cause: Non-numeric value or value out of range specified for Cluster Health Monitor repository size.
// *Action: Specify Cluster Health Monitor repository size in the valid range.
//          Refer to the product documentation or to the command
//          online help for information on supported arguments.

9037, 0, "%s Error: Node name not specified. -disk, -nic or -proc need node name"
// *Cause: The required node name was not specified for -disk, -nic or -proc.
// *Action: Provide a node name with -n option. Refer to the product
//          documentation or to the command online help for information
//          on supported arguments.

9038, 0, "Error: -s and -e need to be specified together"
// *Cause: Either -s or -e is missing.
// *Action: Start and end time need to be specified together for range queries,
//          which cannot be unbounded. Refer to the product documentation 
//          or to the command online help for information on supported arguments. 

9039, 0, "Error %s: -i is not allowed with the range query"
// *Cause: The -i option was specified on a oclumon range query. 
// *Action: Use -i only in continuous mode.  Refer to the command inline
//          help or product documentation for more information.

9040, 0, "Error %s: Band value not specified or incorrect"
// *Cause: The band value was not specified with -t option or was invalid.
// *Action: Provide a valid band value. Refer to the product
//          documentation or to the command online help for information
//          on supported arguments..

9041, 0, "Error %s: The -repos argument was specified without an option."
// *Cause: -repos was not specified with the option, generating a parsing error.
// *Action: Provide a valid option to -repos. Refer to the product documentation
//          or to the command online help for information on supported
//          arguments. 

9042, 0, "Error %s: No size specified with 'checkretentiontime'"
// *Cause: A valid value was not specified with 'checkretentiontime'.
// *Action: Provide a valid numerical value with 'checkretentiontime'. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments.

9043, 0, "Error %s: Non-numeric or invalid value for size: %s"
// *Cause: An invalid or non-numeric value was specified for size.
// *Action: Provide a valid numeric size. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments.

9044, 0, "No key specified with -getkey"
// *Cause: An option was not specified with -getkey.
// *Action: Provide a valid key as an option with -getkey. 

9045, 0, "No key specified for -get"
// *Cause: An option was not specified with -get.
// *Action: Provide a valid option with -get. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments.

9046, 0, "Invalid key specified"
// *Cause: An unknown key was specified with -get.
// *Action: Provide a supported key with -get. Refer to the product
//          documentation or to the command online help for information on
//          supported arguments. 

9047, 0, "Error %s: Error Dumping Log (return code:%d ) for node %s"
// *Cause: An error occurred while dumping local log.
// *Action: Report this error to Oracle Support Services. Cluster Health Monitor repository directory may be
//          unreachable, unreadable or incorrect.

9048, 0, "Error %s: No data received from the Cluster Logger Service after %d attempts"
// *Cause: Data was not received from the Cluster Logger Service after the specified number of
//         attempts or data was not available. 
// *Action: None.

9049, 0, "Error %s: Cannot get environment variable CRFHOME"
// *Cause: An internal error occurred.
// *Action: Report this error to Oracle Support Services.

9050, 0, "Error %s: Too many host names"
// *Cause: Too many host names were specified. 
// *Action: Provide valid number of host names. Refer to the product
//          documentation or to the command online help for information. 

9051, 0, "Error %s: Invalid interval size specified"
// *Cause: Non-numeric or invalid interval specified.
// *Action: Provide a valid numerical value for interval size. Refer to the
//          product documentation or to the command online help for 
//          information 

9052, 0, "Error %s: %s control not supported"
// *Cause: The specified debug control was not supported.
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

9055, 0, "module:level specified in invalid format or invalid value"
// *Cause: Invalid format or value specified for module:level.
// *Action: Provide correct module:level. Refer to the
//          product documentation or to the command online help for
//          information
 
9056, 0, "Error %s: Invalid Cluster Health Monitor repository location specified"
// *Cause: Invalid Cluster Health Monitor repository location specified.
// *Action: Provide a directory with read and write permissions for Cluster Health Monitor repository location. Refer to the
//          product documentation or to the command online help for 
//          information. 

9057, 0, "Error %s: No response received from the Cluster Logger Service"
// *Cause: No data received from the Cluster Logger Service for the query.
// *Action: Ensure that the Cluster Logger Service is running and reachable from the
//          client node by using the 'ping' command for the specified node.

9058, 0, "Error %s: Changing log level failed due to authentication failure"
// *Cause: Log level could not be changed due to authentication failure.
// *Action: Ensure that this command is run as root.

9059, 0, "Error %s: Changing log level failed due to connection failure"
// *Cause: A connection failure occurred while changing the log.
// *Action: Ensure that the daemons are running and are reachable.

9060, 0, "Error %s: Unable to send message due to memory allocation failure"
// *Cause: Memory could not be allocated for debug message.
// *Action: Report this error to Oracle Support Services.

9061, 0, "Error %s: Changing log level failed due to response time-out"
// *Cause: A time out happened while waiting for response.
// *Action: Report this error to Oracle Support Services.

9062, 0, "Error %s: Error in changing log level"
// *Cause: An error occurred while changing log level.
// *Action: Report this error to Oracle Support Services.

9063, 0, "Given time range is more than 1 hour"
// *Cause: The time range specified with showtrail command was more than one
// hour.
// *Action: Provide a range of less than 1 hour for showtrail.

9064, 0, "Error %s: Changing log level failed due to connection failure. Cannot connect to daemon %s."
// *Cause: A connection failure occurred while changing the log level.
// *Action: Ensure that the specified daemon is running and reachable.

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

9071, 0, "Internal error in Cluster Health Analysis during problem analysis"
// *Cause: An internal error occurred during problem analysis.
// *Action: Contact Oracle Support Services.

9072, 0, "Internal error in Cluster Health Analysis report output"
// *Cause: An internal error occurred while reporting a problem.
// *Action: Contact Oracle Support Services.

9073, 0, "No problems to display"
// *Cause: No problems were found that matched the selection criteria specified to the 'oclumon analyze' command. 
// *Action: None.

9074, 0, "No component specified to the component argument"
// *Cause: An 'oclumon analyze' command was issued without a component.
// *Action: Provide a component to the 'oclumon analyze' command. Refer to the
//           product documentation or to the command online help for 
//           information.

9075, 0, "Invalid component name '%s' specified as the component argument"
// *Cause: An 'oclumon analyze' command was issued with an invalid component.
// *Action: Pass a valid component to the 'oclumon analyze' command. Refer to 
//          the product documentation or to the command online help for 
//          information on supported arguments.

9076, 0, "Error loading the required Cluster Health models"
// *Cause: The required Cluster Health models did not exist, did not have 
//         the required permission, or had an invalid format.
// *Action: Ensure that the Cluster Health models are present in the
//          'cdata/model' subdirectory of the Oracle Grid Infrastructure home,
//          and that their permissions are correct. If the problem persists,
//          check for entries in the oclumon log file for more details.

9077, 0, "Invalid path '%s' was specified as the data directory argument"
// *Cause: An 'oclumon analyze' command was issued specifying a data directory
//         that does not exist or is not accessible to the user.
// *Action: Pass a valid path to the 'oclumon analyze' command. Look at
//          accompanying messages for more information.


9078, 0, "Invalid severity value '%s' provided as the severity argument"
// *Cause: An 'oclumon analyze' command was issued with an invalid severity
//         value.
// *Action: Pass a valid severity value to the 'oclumon analyze' command. Refer
//           to the product documentation or to the command online help for 
//           information.

9079, 0, "No instance name specified for the instance argument"
// *Cause: An 'oclumon' command was issued without an instance name.
// *Action: Provide an instance name with the 'oclumon' command. Refer to
//          the product documentation or to the command online help for 
//          information.

9080, 0, "data for other nodes of cluster cannot be viewed from this node"
// *Cause: An 'oclumon dumpnodeview -n' command was issued for other nodes from a leaf node. 
// *Action: Refer to the Cluster Health Monitor documentation for more information.

9081, 0, "Internal error in Cluster Health calibration"
// *Cause: An internal error occurred during cluster health model calibration.
// *Action: Contact Oracle Support Services.

9082, 0, "Insufficient permission to execute command. Require privileged user"
// *Cause: A non-privileged user attempted to execute a command requiring privilege.
// *Action: Issue the command again as a privileged user.

9083, 0, "No database name specified for the database argument"
// *Cause: An 'oclumon' command was issued without a database name.
// *Action: Provide a database name with the 'oclumon' command. Refer to
//          the product documentation or to the command online help for 
//          information.

9084, 0, "Error %s: Node name is greater than %s bytes"
// *Cause: An 'oclumon' command was issued with a node name that was too long.
// *Action: Supply a node name no greater than the indicated size with the 
//          'oclumon' command and retry. Refer to the product documentation or
//           to the command online help for information.

9085, 0, "Model name missing or invalid for the model argument"
// *Cause: The previous oclumon command was rejected because it did not 
//         include a valid model name.
// *Action: Reissue the oclumon command providing a valid model name. Refer to
//          the product documentation or to the command online help for 
//          information.

9086, 0, "Server pool name missing or invalid for the server pool argument"
// *Cause: The previous oclumon command was rejected because it did not 
//         include a valid server pool name.
// *Action: Reissue the oclumon command providing a valid server pool name. 
//          Refer to the product documentation or to the command online help 
//          for information.

9087, 0, "Server pool name specified in a cluster without user-defined server pools"
// *Cause: The previous oclumon command was rejected because it was issued 
//         with a server pool name on a cluster without user-defined server 
//         pools.
// *Action: Reissue the oclumon command without a server pool name. Refer to
//          the product documentation or to the command online help for 
//          information.

9088, 0, "Node name specified in a cluster with user-defined server pools"
// *Cause: The previous oclumon command was rejected because it was issued
//         with a node name on a cluster with user-defined server pools.
// *Action: Reissue the oclumon command without a node name. Refer to
//          the product documentation or to the command online help for 
//          information.

9089, 0, "Parameter '%s' is not supported in combination with parameter '%s'."
// *Cause: The command was rejected because the combination of parameters 
//         passed was invalid.
// *Action: Refer to the product documentation or to the online help for the
//          command and reissue the command with the correct parameters.

9090, 0, "Error %s: Parameter '%s' is specified multiple times."
// *Cause: The previous 'oclumon' command was rejected because the parameter
//         listed in the message was specified multiple times.
// *Action: Refer to the product documentation or to the online help for the
//          command and reissue the command with the correct parameters.

9091, 0, "database name '%s' is invalid"
// *Cause: An 'oclumon' command was issued with an invalid database name.
// *Action: Provide a valid database name with the 'oclumon' command. Refer to
//          the product documentation or to the online help for the command
//          for information.

9092, 0, "No instance of database '%s' is active on this node."
// *Cause: The 'oclumon calibrate' command was rejected because no instance
//         of the above listed database was active on the local node.
// *Action: Issue the 'srvctl start database' command to start the above listed
//          database. Issue the 'srvctl status database' command to retrieve 
//          a list of nodes on which the database instances are online. Issue
//          the 'oclumon calibrate' command again from a node on which the 
//          database instance is online. Refer to the product documentation or
//          to the online help for the command for information.

9093, 0, "Database '%s' of type '%s' is not supported in a cluster with user-defined server pools."
// *Cause: An 'oclumon' command was issued with an administrator-managed 
//         database in a cluster with user-defined server pools.
// *Action: Reconfigure the database to be policy-managed using the 
//          'srvctl modify database' command to enable monitoring by the Oracle
//          Cluster Health Analysis service. Verify the monitoring status 
//          using the 'srvctl status cha' command. Re-issue the 
//          'oclumon calibrate' command. Refer to the product documentation or 
//          to the online help for the command for information.

// LOGUI side messages

9100, 0, "Error setting Cluster Health Monitor repository size"
// *Cause: An error occurred while setting Cluster Health Monitor repository size on the Cluster Logger Service.
// *Action: Report this error to Oracle Support Services.

9101, 0, "Error updating Cluster Health Monitor repository size in configuration file."
// *Cause: An error occurred while writing the Cluster Health Monitor repository size to configuration 
//         files.
// *Action: Report this error to Oracle Support Services.

9102, 0, "No data for the node at the specified time"
// *Cause: Data was not found for the specified node.
// *Action: This is an informational message only.

9103, 0, "No data available"
// *Cause: Data was not available for the query. 
// *Action: Make sure the System Monitor Service is running on the specified node.

9104, 0, "No data available for the specified nodes"
// *Cause: Data was not available for specified nodes.
// *Action: Make sure the System Monitor Service is running on the specified nodes.

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
//          for the specified range query.

9108, 0, "Threshold out of acceptable range"
// *Cause: A threshold was specified that is outside the allowed range. 
// *Action: Make sure threshold is within the acceptable range. Refer
//          documentation or online help for more information

9109, 0, "New Cluster Health Monitor repository location same as the old location on node %s"
// *Cause: The new location specified for Cluster Health Monitor repository is same as the old location. 
// *Action: Provide a different location for Cluster Health Monitor repository. Refer
//          documentation or online help for more information.

9110, 0, "Cluster Health Monitor repository location not changed as the location specified does not exist on node %s."
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

9117, 0, " Grid Infrastructure Management Repository configuration error \n %s"
// *Cause: Grid Infrastructure Management Repository configuration error occurred. 
// *Action: Take the following steps.
//          1) Examine the accompanying ORA-nnnnn or CRS-nnnn error messages. If possible, correct the issue reported.
//          2) Issue a 'srvctl status mgmtdb' command to determine the status of the Grid Infrastructure Management Repository database. If it is not online, examine the database instance alert log to determine what happened.
//          3) If you are unable to determine or correct the problem, run 'diagcollection.pl' and contact Oracle Support Services.

9118, 0, "Grid Infrastructure Management Repository connection error \n %s"
// *Cause: Grid Infrastructure Management Repository connection error occurred. 
// *Action: Take the following steps.
//          1) Examine the accompanying ORA-nnnnn or CRS-nnnn error messages. If possible, correct the issue reported.
//          2) Issue a 'srvctl status mgmtdb' command to determine the status of the Grid Infrastructure Management Repository database. If it is not online, examine the database instance alert log to determine what happened.
//          3) If you are unable to determine or correct the problem, run 'diagcollection.pl' and contact Oracle Support Services.

9119, 0, "Warning: %s option has been deprecated and will be ignored."
// *Cause: A deprecated option was specified on the command line. The option
//          was ignored.
// *Action: Check the documentation for the new syntax of the command.

9120, 0, "oclumon was not able to connect to the Grid Infrastructure Management Repository because an authorization failure occurred. \n%s"
// *Cause: An authorization failure occurred when connecting to the Grid Infrastructure Management Repository.
// *Action: Run the 'srvctl config mgmtdb' command to verify that Grid Infrastructure Management Repository has been created successfully. If not, run the 'mgmtca' command to reset the passwords in the wallet. If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9121, 0, "oclumon was not able to connect to the Grid Infrastructure Management Repository because no listener was available."
// *Cause: An attempt to connect to the Grid Infrastructure Management Repository failed because no Grid Infrastructure Management Repository listener was running.
// *Action: Use the 'srvctl status mgmtlsnr' command to confirm that Grid Infrastructure Management Repository listener is running. If it is not, start it using the 'srvctl start mgmtlsnr' command. If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9122, 0, "oclumon was not able to retrieve the security keys from the wallet."
// *Cause: An attempt to retrieve the security keys from the wallet failed.
// *Action: Run the 'crsctl query wallet -type MGMTDB' command to verify that the wallet exists. If the problem persists, contact Oracle Support Services. 

9123, 0, "oclumon was not able to connect to the Grid Infrastructure Management Repository because a Cluster Synchronization Services request failed."
// *Cause: An attempt to connect to the Grid Infrastructure Management Repository failed due to a Cluster Synchronization Services failure.
// *Action: If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9124, 0, "Cluster Health Monitor repository retention change failed. Aborting retention change. Error: %s"
// *Cause: An error occurred while setting the Cluster Health Monitor repository size on the cluster logger service.
// *Action: Take the following steps.
//          1) Examine the accompanying ORA-nnnnn or CRS-nnnn error messages. If possible, correct the issue reported.
//          2) Issue a 'srvctl status mgmtdb' command to determine the status of the Grid Infrastructure Management Repository database. If it is not online, examine the database instance alert log to determine what happened.
//          3) If you are unable to determine or correct the problem, run 'diagcollection.pl' and contact Oracle Support Services.

9125, 0, "Error %s: Node name %s is unknown or invalid. No data found for this node in Grid Infrastructure Management Repository."
// *Cause: The 'oclumon' command could not be carried out as entered because the node name cited in the message was invalid. The cited node name was ignored and the query executed with any remaining names.
// *Action: Reissue the 'oclumon' command, if desired, supplying a valid name for the node name cited in the message. Refer to the product documentation or to command online help for information.

9126, 0, "Cluster Health Monitor repository retention change failed. Error: retention space is lower than size permitted."
// *Cause: An attempt to set the Cluster Health Monitor repository size on the cluster logger service was rejected because the specified size was smaller than the permitted minimum size.
// *Action: Retry the command specifying a retention size larger or equal to the minimum size of 1 GB.

9127, 0, "Error %s: Too many PIDs"
// *Cause: The command 'oclumon dumpnodeview -pid' failed because too many PIDs were specified. 
// *Action: Refer to the product documentation or to the command online help for information and reissue the command specifying a valid number of PIDs.

9128, 1, "Error %s: Write operation is not permitted."
// *Cause: The command 'oclumon dumpnodeview -dir <dir_name>' failed because the user was not allowed to write in the specified directory.
// *Action: Ensure that the user has write permission for the specified directory and retry.

9129, 1, "Error %s: Directory does not exist."
// *Cause: The command 'oclumon dumpnodeview -dir <dir_name> failed because the specified directory did not exist. 
// *Action: Create the specified directory and retry. 

9130, 1, "Error: 'dumpnodeview' option -v or -verbose conflicts with additional view options."
// *Cause: The command 'oclumon dumpnodeview' failed because either -v or -verbose option was specified in addition to other view options (-system, -process, -cpu, etc.). The verbose options imply the inclusion of every part.
// *Action: Retry the operation specifying other options without -v or -verbose or specifying -v or -verbose without other options.

// HELP MESSAGES FOR OCLUMON
//9200, 3, "For help from command line: oclumon <verb> -h\nFor help in interactive mode: <verb> -h\nCurrently supported verbs are:\nshowtrail, showobjects, dumpnodeview, manage, version, debug, quit, exit, and help\n"
9200, 3, "For help from command line: oclumon <verb> -h\nFor help in interactive mode: <verb> -h\nCurrently supported verbs are:\nshowobjects, dumpnodeview, manage, version, debug, quit, exit, and help\n"
// 9201 message will be used for Betatwo where showobjects will be disabled.
9201, 3, "For help from command line: oclumon <verb> -h\nFor help in interactive mode: <verb> -h\nCurrently supported verbs are:\ndumpnodeview, manage, version, set, debug, quit, exit, and help\n"
// Manage help (9221 - 9240)
9221, 3, "\nmanage verb usage\n=================\n  manage [[-repos {resize <time>|changesize <memsize>|reploc <new_loc> [[-maxtime <time>]|\n         [-maxspace <memsize>]] }]|[-get <key1> <key2>..]|\n[-enable diagsnap] |[-disable diagsnap]\n\n*Where\n"

9222, 3, ""
// Left blank so that it can be used in future when we bring back -m option
9223, 3, "  -repos       = Required to specify Cluster Health Monitor repository related options\n  -get         = Fetch manage information for one or more named keys\n  <key1> <key2>= <key> can be repsize, reppath, master and replica\n  resize       = Option for resizing Cluster Health Monitor repository\n  <time>       = Size of Cluster Health Monitor repository in number of seconds\n"
9224, 3, "                 must be more than %d (1 hour) and less than %d (%d days)\n"
9225, 3, "  changesize   = Option for Change Cluster Health Monitor repository space limit\n  <memsize>    = Size of Cluster Health Monitor repository in megabytes\n"
9226, 3, "  reploc       = Option for Change Repository Location\n  <new_loc>    = Path to new directory e.g.: /opt/db\n  -maxtime     = Option to specify Cluster Health Monitor repository size in terms of elapsed seconds of data capture for new location\n  -maxspace    = Option to specify space limit for new Cluster Health Monitor repository location\n -enable diagsnap     = Option to enable diagsnap  -disable diagsnap     = Option to disable diagsnap\n\n"

//  Debug Help (9241-9260)
9241, 3, "\ndebug, set, and get verb usage\n================\nset log <daemon> <module:level> = set log level. same as debug log command.\nget log <daemon> <module> = get current log level\ndebug {log <daemon> <module:level> | version}\n\n*Where\n  log            = To change log levels\n  <daemon>       = Daemon whose log level has to be changed\n                   Following daemons are supported :\n"
9242, 3, "                   osysmond, ologgerd, client, all\n"
9243, 3, "                   osysmond, ologgerd, client, all\n"
9244, 3, "  <module:level> = Module and level pair\n                   Supported osysmond modules:\n                   CRFMOND, CRFM, allcomp, etc.\n                   Supported ologgerd modules:\n                   CRFLOGD, CRFLDREP, CRFM, allcomp, etc.\n                   Supported client modules:\n                   OCLUMON, CRFM, allcomp, etc.\n"
9245, 3, "                   Supported oproxyd modules:\n                   CRFPROXY, allcomp\n"
9246, 3, "                   Supported log levels:\n                   0, 1, 2, 3\n  version        = To display versions\n\n*Note\n  modules supported for 'all' daemons: allcomp\n  All daemons support: CRFM, allcomp\n  See all modules in a daemon by calling oclumon get log <daemon> allcomp\n  Module name is case-sensitive.\n\n*Example:\n  oclumon debug log osysmond CRFMOND:3\n  oclumon set log ologgerd CRFLOGD:2\n  oclumon get log all allcomp\n"

// Dumpnodeview help (9261-9300)
9261, 3, "\ndumpnodeview verb usage\n=======================\nThe dumpnodeview command reports monitored records in the text format. The\ncollection of metrics for a node at a given point in time (a timestamp) is\ncalled a node view.\n\n* Usage\n"
9262, 3, "  dumpnodeview [-allnodes | -n <node1> ...] [-last <duration> |\n                -s <timestamp> -e <timestamp>][-i <interval>][-v]\n                [-system][-process][-device][-filesystem][-nic]\n                [-protoerr][-cpu][-topconsumer][-format <format type>]\n                [-dir <directory> [-append]]\n\n"
9263, 3, "*Where\n  -n <node1> ...   = Dump node views for specified nodes\n  -allnodes        = Dump node views for all nodes\n  -s <timestamp>   = Specify start time for range dump of node views\n  -e <timestamp>   = Specify end time for range dump of node views\n"
9264, 3, "                     Absolute timestamp must be in \"YYYY-MM-DD HH24:MI:SS\"\n                     format, for example \"2007-11-12 23:05:00\"\n  -last <duration> = Dump the latest node views for a specified duration.\n"
9265, 3, "                     Duration must be in \"HH24:MI:SS\" format, for example\n                     \"00:45:00\"\n"
9266, 3, "  -i               = Dump node views separated by the specified\n                     interval in seconds. Must be a multiple of 5.\n" 
9267, 3, "  -v               = Dump verbose node views containing all parts.\n  -system, -cpu,.. = Dump each indicate node view parts.\n  -format <format type> = format of the output.\n                     <format type> can be legacy, tabular, or csv.\n                     The default format is mostly tabular with legacy for\n                      nodeview parts with only one row.\n  -dir <directory> = Dump node view part to file(s) in spceified dir.\n                     With -append, will append the"
9268, 3, " files. Overwrite otherwise.\n\n *Requirements and notes\n  To stop continuous display, use Ctrl-C on Linux or UNIX and Esc on Windows.\n  -s and -e need to be specified together for range dumps of node views.\n  The local System Monitor Service (osysmond) must be running to get dumps.\n"
9269, 3, "  The Cluster Logger Service (ologgerd) must be running to get dumps.\n  For screen reader user, please use option -format legacy.\n\n"
9270, 3, "*Defaults :\n  Mode      : Continuous mode\n\n*Example :\n  oclumon dumpnodeview -n node1 node2 node3 -last \"12:00:00\"\n  oclumon dumpnodeview -last \"00:10:00\" -i 30\n  oclumon dumpnodeview -format csv -system -cpu -topconsumer\n"

// Showtrail Help  (9301-9340)
9301, 3, "\nSHOWTRAIL verb usage\n====================\n  showtrail [-n <node>] [[-diskid <diskid> <discparam>]|\n            [-nicid <nicid> <nicparam>]|[-pid <pid> <procparams>]|\n            [-sys <systemparam>]]\n"
9302, 3, "            [-c <regions>][-s <time> -e <time>]|[-last <time1>] [-h]\n\n*Where\n"
9303, 3, "  -n           = show trail for specified node\n  <node>       = node name for which trail needs to be shown\n  -s           = To specify time for the start of range queries\n"
9304, 3, "  -e           = To specify time for the end of range queries\n  <time>       = Absolute time to be specified within quotes in\n                 \"YYYY-MM-DD HH24:MI:SS\" format, like \"2007-11-12 23:05:00\"\n"
9305, 3, "  -last        = To specify time for last queries\n  <time1>      = Time in \"HH24:MI:SS\" format to be specified with -last option,like  \"00:45:00\"\n  -diskid      = To request trail of disk parameters\n"
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
9343, 3, "  -n        = showgaps for specified node\n  <node>    = node name for which gaps need to be shown\n  -s        = To specify time for the start of range queries\n  -e        = To specify time for the end of range queries\n"
9344, 3, "  <time>    = Absolute time to be specified within quotes in\n              \"YYYY-MM-DD HH24:MI:SS\" format, like \"2007-11-12 23:05:00\"\n  -last     = To specify time for last queries\n  <time1>   = Time in \"HH24:MI:SS\" format to be specified with -last option,like \"00:45:00\"\n"
9345, 3, "  -t        = To specify minimum threshold for a gap\n  <gapsize> = Gap size in seconds \n\n"
9346, 3, "*Requirements\n  -s and -e need to be specified together for range queries\n  The local System Monitor Service should be running to get gaps.\n  The Cluster Logger Service should be running to get gaps.\n\n*Defaults :\n  Threshold: 3 (least size of gap)\n  Time: Last 30 min\n\n" 
9347, 3, "*Example:\n  showgaps -n stadn59 -s \"2007-11-12 23:05:00\" -e \"2007-11-12 23:15:00\" -t 10\n" 

// Showobject help (9381-9420)

9381, 3, "\nshowobjects verb usage\n======================\nshowobjects [[-allnodes]|[-n <node> [[-disk]|[-proc]|[-nic]]]][-time <time> [-b <band>]]\n\n*Where\n"
9382, 3, ""
9383, 3, "  -n           = Show objects for specified node\n  <node>       = Node name for which objects need to be shown\n  -time        = Time at which objects are required\n  <time>       = Absolute time to be specified within quotes in\n                 \"YYYY-MM-DD HH24:MI:SS\" format, like \"2007-11-12 23:05:00\"\n  -disk"
9384, 3, "        = To request list of disks\n  -nic         = To request list of network interface cards\n  -proc        = To request list of processes\n  -allnodes    = Shows all the nodes which can be queried\n  -b           = For specifying maximum look up around <time> in seconds\n  <band>       = Size of band in seconds\n\n"
9385, 3, "*Requirements\n  Local System Monitor Service should be running to get objects.\n  Master loggerd should be running to get objects.\n\n*Defaults :\n  Time    : Current\n  Option  : -allnodes\n\n*Example :\n  showobjects -n stadn59 -disk -time \"2008-02-20 02:01:48\"\n "

// Analyze Help  (9421-9440)
9421, 3, "\nanalyze verb usage\n=======================\nThe analyze command reports problems pertaining to Oracle Clusterware, ASM and Database.\n\n" 
9422, 3, "*Usage\nanalyze [-allnodes|-n <node1> ...] [-s <time> -e <time>|-last <duration>]\n        [-r <severity>] [-y <component> ...] [-x <instance name>] [-v]\n\n"
9423, 3, "*Where\n  -n <node1> ...     = To limit the display to problems associated with the specified nodes\n"
9424, 3, "  -allnodes          = To analyze problems for all nodes\n  -s                 = To specify time for the start of range queries\n  -e                 = To specify time for the end of range queries\n"
9425, 3, "  <time>             = Absolute time to be specified within quotes in\n                       \"YYYY-MM-DD HH24:MI:SS\" format, like \"2007-11-12 23:05:00\n  -last              = To specify relative duration from current time\n  <duration>         = Duration must be in \"HH24:MI:SS\" format, like \"00:45:00\"\n"
9426, 3, "  -r                 = To limit the display to a subset of problems based on severity\n                       The severity can be HIGH, MEDIUM or LOW\n"
9427, 3, "  -b                 = To specify a directory containing user models, and override the default models\n"
9428, 3, "  -d                 = To specify a directory containing data for analysis\n                       If a component is specified, it must be ASM, DATABASE or both\n"
9429, 3, "  -y <component> ... = To limit the display to a subset of problems based on component\n                       The component can be CLUSTERWARE or DATABASE\n"
9430, 3, "  -x                 = To limit the display to problems associated with a specific database instance\n                       The component specified must be DATABASE\n"
9431, 3, "  -v                 = To display results in a verbose format\n"
9432, 3, "  \n\n*Requirements and notes\n  To stop the display, use Ctrl-C on Linux and Esc on Windows\n  The -s and -e options need to be specified together for range queries\n"
9433, 3, "  Analysis for the last 30 minutes is displayed when no time or duration is specified  \n  The Grid Infrastructure Management Repository must be active to complete the analysis\n\n"
9434, 3, "*Example:\n  oclumon analyze -n stadn59 -s \"2007-11-12 23:05:00\" -e \"2007-11-12 23:35:00\" -y CLUSTERWARE\n  oclumon analyze -n stadn19 -s \"2007-11-12 23:05:00\" -e \"2007-11-12 23:35:00\" -y DATABASE -x storedb3\n  oclumon analyze -allnodes -s \"2007-11-12 23:05:00\" -e \"2007-11-12 23:35:00\" -y CLUSTERWARE\n "

// Calibrate Help  (9441-9460)
9441, 3, "\ncalibrate verb usage\n=======================\nThe calibrate command calibrates the models pertaining to Oracle Clusterware, ASM and Database.\n\n" 
9442, 3, "*Usage\ncalibrate {-s <time> -e <time>}\n          -y <component>\n          {-allnodes|-n <host>|-o <serverpool name>|{-w <database name> [-o <serverpool name>]}}\n          [-q <model name>] [-v]\n\n"
9443, 3, "*Where\n  -s                 = To specify the start time of the data used for model calibration\n  -e                 = To specify the end time of the data used for model calibration\n"
9444, 3, "  <time>             = Absolute time to be specified within quotes in\n                       \"YYYY-MM-DD HH24:MI:SS\" format, like \"2012-11-12 23:05:00\"\n"
9445, 3, "  -y <component>     = To calibrate a specific model based on the component\n                       The component can be CLUSTERWARE, ASM or DATABASE.\n"
9446, 3, "  -allnodes          = Calibrate models for all nodes\n                       The component specified must be CLUSTERWARE.\n"
9447, 3, "  -n <host>          = To limit the model calibration to a specific host\n                       The component specified must be CLUSTERWARE.\n"
9448, 3, "  -w <database name> = To limit the model calibration to a specific database\n                       The component specified must be DATABASE.\n"
9449, 3, "  -o <serverpool name> = To limit the model calibration to a specific server pool in a policy-managed cluster\n"
9450, 3, "  -v                 = To display results in a verbose format\n"
9451, 3, "  -q <model name>    = Optional model provided by user.\n                       If a model is not provided, the current model is calibrated.\n                       If a model is provided, then an existing model is calibrated if one exists.\n                       If a model is provided, and it does not exist, then an existing model is cloned, and the cloned model is calibrated.\n"
9452, 3, "\n"
9453, 3, "  \n*Requirements and notes\n  To stop the display, use Ctrl-C on Linux and Esc on Windows.\n  The -s and -e options need to be specified together for range queries.\n"
9454, 3, "  The Grid Infrastructure Management Repository must be active to complete the calibration.\n"
9455, 3, "  An instance of the database must be active on the node the command is issued when the DATABASE component is specified."
9456, 3, "  The instance whose model will be calibrated may be remote and does not have to be active.\n"
9457, 3, "  The target i.e. database or host will not be monitored while the model is being calibrated.\n"
9458, 3, "  The command must be issued by a privileged user.\n\n"
9459, 3, "*Example :\n  oclumon calibrate -s \"2012-11-12 09:05:00\" -e \"2012-11-12 11:05:00\" -y CLUSTERWARE -n stadn59\n"
9460, 3, "  oclumon calibrate -s \"2012-11-12 10:05:00\" -e \"2012-11-12 12:35:00\" -y DATABASE -w storedb\n  oclumon calibrate -s \"2012-11-12 22:05:00\" -e \"2012-11-12 23:35:00\" -y DATABASE -w storedb -o SERVERPOOLBIG -q BACKUP\n "

// Manage help (9461 - 9480)
9461, 3, "\nManage verb usage\n=================\n  manage -repos {checkretentiontime <time> | changerepossize <memsize>} |\n\t -get {<key1> [<key2> ...] | alllogger [-details] | mylogger [-details]} |\n\t -enable {diagsnap} | -disable {diagsnap} \n\n*Where\n"
9462, 3, ""
// Left blank so that it can be used in future when we bring back -m option
9463, 3, "  -repos\t\t= Required to specify Cluster Health Monitor repository related options\n  -get\t\t\t= Fetch manage information for one or more named keys\n  <key1> <key2>\t\t= <key> can be repsize, reppath, master, mylogger and alllogger \n  alllogger\t\t= Special key with -get to get list of all nodes running Cluster Logger Service"
9464, 3, "\n  mylogger\t\t= Special key with -get to get the node running the Cluster Logger Service which is serving the current node\n  -details\t\t= Option with alllogger and mylogger for listing nodes served by the Cluster Logger Service\n  checkretentiontime    = Option to confirm whether specified time retention can be realized for current Cluster Health Monitor repository size"
9465, 3, "\n  <time>\t\t= Retention of Cluster Health Monitor repository in number of seconds\n"
9466, 3, "  changerepossize\t= Option for Change Cluster Health Monitor repository space limit\n  <memsize>\t\t= Size of Cluster Health Monitor repository in megabytes\n"
9467, 3, "  -csvlog\t\t= Options related to comma separated value output from Cluster Health Monitor\n  status\t\t= Comma separated values feature status: ON or OFF.  Feature is ON by default.\n  interval <time>\t= Option to specify comma separated values sampling interval in whole clock seconds. Default sampling interval is 60 seconds.\n"
9468, 3, "  logduration <size>\t= Option to specify comma separated values data file boundary in megabytes. Default file boundary is 10 megabytes.\n\n"
9469, 3, "*Requirements\n  The local cluster synchronization service must be running to change the retention time of the Cluster Health Monitor repository.\n  The Cluster Logger Service must be running to change the retention time of the Cluster Health Monitor repository.\n\n*Example :\n"
9470, 3, "  manage -get MASTER \n  manage -repos checkretentiontime 86400\n  manage -repos changerepossize 6000\n  manage -get alllogger -details\n  manage -enable diagsnap \n\n"
9471, 3, "  manage -csvlog status off\n  manage -csvlog interval 50\n  manage -csvlog logduration 300\n"
9472, 3, "\n"
9473, 3, "  -enable diagsnap\t= Option to enable diagsnap script\n  -disable diagsnap\t= Option to disable diagsnap script\n"

// Calibrate status messages 9481 - 9499)
// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9481, 1, "%s '%s': attempting to stop monitoring"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9482, 1, "%s '%s': successfully stopped monitoring"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9483, 1, "%s '%s': failed to stop monitoring"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9484, 1, "%s '%s': starting calibration of model"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9485, 1, "%s '%s': successfully recalibrated model"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9486, 1, "%s '%s': failed to recalibrate model"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9487, 1, "%s '%s': attempting to start monitoring"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9488, 0, "%s '%s': successfully started monitoring"
// *Document: NO

// %s '%s' = <type> '<name>', where type = host,instance,cluster,database
9489, 1, "%s '%s': failed to start monitoring"
// *Document: NO

// Cluster Health Monitor specific clusterware alert messages (9500 - 9599)

9500, 0, "The System Monitor Service aborted on host %s. Details at %s in %s."
// *Cause:  The System Monitor Service aborted due to an internal
//          error.
// *Action: If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9501, 0, "The Cluster Logger Service aborted on host %s. Details at %s in %s."
// *Cause:  The Cluster Logger Service aborted due to an internal
//          error.
// *Action: If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9502, 0, "The Cluster Health Monitor repository location %s is inaccessible. Details at %s in %s."
// *Cause: An error occurred while accessing the Cluster Health repository.
// *Action: Check that the Cluster Health Monitor repository location in question has the 
//          correct permissions. Determine whether this behavior is limited
//          to one node or whether it occurs across all of the nodes in 
//          the cluster. Use the 'oclumon manage -repos reploc <location>'
//          command to replace the Cluster Health Monitor repository location.

9503, 0, "The System Monitor Service on this host is unable to communicate with the Cluster Logger Service on host %s, and will log the Cluster Health Monitor data to the local repository."
// *Cause:  Communication was lost with the Cluster Logger Service node.
// *Action: Verify all network connections between cluster nodes and repair
//          any problematic connections. If network problems are not found,
//          execute the following steps:
//          1. Run diagcollection.pl.
//          2. Contact Oracle Support Services.

9504, 0, "The Cluster Logger Service on host %s is dropping the Cluster Health Monitor node view. Details at %s in %s."
// *Cause: The Cluster Logger Service was unable to insert Cluster Health Monitor node view into  Cluster Health Monitor repository .
// *Action: Contact Oracle Support Services.

9505, 0, "The Cluster Health Monitor repository is deleted due to corruption and the Cluster Logger Service is disabled on %s. Details at %s in %s."
// *Cause: A critical error occurred while operating on Cluster Health Monitor repository.
// *Action: Contact Oracle Support Services.

9506, 0, "The System Monitor Service local repository is disabled on the host %s. Details at %s in %s."
// *Cause: An internal error occurred while writing to the System Monitor Service local repository.
// *Action: Contact Oracle Support Services.

9507, 0, "The maximum Cluster Health Monitor repository retention time is reached. Deleting the oldest Cluster Health Monitor node views in age order."
// *Cause: The maximum time for which the oldest Cluster Health Monitor node view will be 
//         available on Cluster Health Monitor repository was reached.
// *Action: If necessary, use 'oclumon manage -repos changerepossize <size>' command to 
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

9511, 0, "The System Monitor Service was not able to collect disk information on node %s."
// *Cause: There was a problem in reading the disk-related information.
// *Action: Confirm that disks are properly configured and usable on the indicated node. If no issues are found and the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9512, 0, "The System Monitor Service was not able to collect network interface card information on node %s."
// *Cause: There was a problem in reading the network interface card related information.
// *Action: Confirm that network interface cards are properly configured and usable on the indicated node. If no issues are found and the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9513, 0, "The version of the Grid Infrastructure Management Repository [%s] is incompatible with the version of the Oracle Clusterware [%s]."
// *Cause: During startup, the Cluster Logger Service found that the version of Grid Infrastructure Management Repository was older than that of the Oracle Clusterware.
// *Action: Upgrade the Grid Infrastructure Management Repository to a version which is at least that of the Oracle Clusterware.

9514, 0, "The Cluster Logger Service encountered an unexpected error during inserting the data into the Grid Infrastructure Management Repository. \n%s."
// *Cause: An unexpected Oracle error was returned by the Grid Infrastructure Management Repository.
// *Action: 1) Examine the accompanying ORA-nnnnn error messages. If possible, correct the issue reported.
//          2) Issue a 'srvctl status mgmtdb' command to determine the status of the Grid Infrastructure Management Repository database. If it is not online, examine the database instance alert log to determine what happened.
//          3) If you are unable to determine or correct the problem, contact Oracle Support Services.

9515, 0, "The Cluster Logger Service encountered an unexpected error during deleting the data from Grid Infrastructure Management Repository. \n%s."
// *Cause: An unexpected Oracle error was returned by the Grid Infrastructure Management Repository.
// *Action: 1) Examine the accompanying ORA-nnnnn error messages. If possible, correct the issue reported.
//          2) Issue a 'srvctl status mgmtdb' command to determine the status of the Grid Infrastructure Management Repository database. If it is not online, examine the database instance alert log to determine what happened.
//          3) If you are unable to determine or correct the problem, contact Oracle Support Services.

9516, 0, "Encountered an unexpected error during querying the data from Grid Infrastructure Management Repository. \n%s."
// *Cause: An unexpected Oracle error was returned by the Grid Infrastructure Management Repository.
// *Action: 1) Examine the accompanying ORA-nnnnn error messages. If possible, correct the issue reported.
//          2) Issue a 'srvctl status mgmtdb' command to determine the status of the Grid Infrastructure Management Repository database. If it is not online, examine the database instance alert log to determine what happened.
//          3) If you are unable to determine or correct the problem, contact Oracle Support Services.

/ Alert
9517, 0, "An unrecoverable configuration error occurred in the Grid Infrastructure Management Repository. Details at %s in %s. \n%s"
// *Cause: An unexpected condition happened in the Grid Infrastructure Management Repository.
// *Action: 1) Examine the accompanying ORA-nnnnn error messages. If possible, correct the issue reported.
//          2) Issue a 'srvctl status mgmtdb' command to determine the status of the Grid Infrastructure Management Repository database. If it is not online, examine the database instance alert log to determine what happened.
//          3) If you are unable to determine or correct the problem, contact Oracle Support Services.

9518, 0, "The Cluster Logger Service was not able to connect to the Grid Infrastructure Management Repository because an authorization failure occurred. \n%s"
// *Cause: An authorization failure occurred when connecting to the Grid Infrastructure Management Repository.
// *Action: Run the 'srvctl config mgmtdb' command to verify that Grid Infrastructure Management Repository has been created successfully. If not, run the 'mgmtca' command to reset the passwords in the wallet. If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9519, 0, "The Cluster Logger Service was not able to connect to the Grid Infrastructure Management Repository because no listener was available."
// *Cause: An attempt to connect to the Grid Infrastructure Management Repository failed because no Grid Infrastructure Management Repository listener was running.
// *Action: Use the 'srvctl status mgmtlsnr' command to confirm that Grid Infrastructure Management Repository listener is running. If it is not, start it using the 'srvctl start mgmtlsnr' command. If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9520, 0, "The storage of Grid Infrastructure Management Repository is %u%% full. The storage location is '%s'."
// *Cause: The storage of Grid Infrastructure Management Repository was close to full. This storage can be a shared file system or an Oracle ASM disk group.
// *Action: Make sure there is sufficient free space in repository location.

9521, 0, "Grid Infrastructure Management Repository was not available on the node %s. The System Monitor Service will store the data in its local repository on all nodes. \n%s"
// *Cause: Grid Infrastructure Management Repository was initializing or was shutting down when the Cluster Logger Service tried to connect, insert or delete the data.
// *Action: Check if the Grid Infrastructure Management Repository is online using the 'srvctl status mgmtdb' command. If it is offline, start it using the 'srvctl start mgmtdb' command.

9522, 0, "The Cluster Logger Service was not able to retrieve the security keys from the wallet."
// *Cause: The Cluster Logger Service could not get the security keys due a wallet read failure.
// *Action: Run the 'crsctl query wallet -type MGMTDB' command to verify that the wallet exists. If the problem persists, contact Oracle Support Services. 

9523, 0, "The Cluster Logger Service was not able to connect to the Grid Infrastructure Management Repository because a Cluster Synchronization Services request failed."
// *Cause: An attempt to connect to the Grid Infrastructure Management Repository failed due to a Cluster Synchronization Services failure.
// *Action: If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9524, 0, "The System Monitor Service on this host is unable to communicate with the Cluster Logger Service on host %s, and will log the Cluster Health Analysis data to the local repository."
// *Cause:  Communication was lost with the Cluster Logger Service node.
// *Action: Verify all network connections between cluster nodes and repair
//          any problematic connections. If network problems are not found,
//          execute the following steps:
//          1. Run diagcollection.pl.
//          2. Contact Oracle Support Services.

9525, 0, "The Cluster Health Analysis local repository is disabled on host %s. Details at %s in %s."
// *Cause: An internal error occurred while writing to the Cluster Health Analysis local repository.
// *Action: Contact Oracle Support Services.

9526, 0, "The Cluster Logger Service was unable to reset the password for Cluster Health Monitor."
// *Cause: A password reset failure occurred when the Cluster Logger Service tried to reset the Cluster Health Monitor password after finding that the password had expired.
// *Action: Run the 'srvctl config mgmtdb' command to verify that Grid Infrastructure Management Repository has been created successfully. If not, run the 'mgmtca setpasswd -user CHM' command to reset the password for Cluster Health Monitor. If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9527, 0, "The Cluster Logger Service was unable to reset the password for Cluster Health Analysis."
// *Cause: A password reset failure occurred when the Cluster Logger Service tried to reset the Cluster Health Analysis password after finding that the password had expired.
// *Action: Run the 'srvctl config mgmtdb' command to verify that Grid Infrastructure Management Repository has been created successfully. If not, run the 'mgmtca setpasswd -user CHA' command to reset the password for Cluster Health Analysis. If the problem persists, run 'diagcollection.pl' and contact Oracle Support Services.

9528, 0, "The Grid Infrastructure Management Repository exceeded the size set for it; disabling logging."
// *Cause: An internal error caused the size of the Grid Infrastructure Management Repository to be reset to an unexpectedly large value. Logging was disabled to prevent further problems.
// *Action: Contact Oracle Support Services.

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
/  Messages below need to be kept in sync with PRVG messages 10002-10050
/  in opsm/jsrc/oracle/ops/verification/resources/PrvgMsg.msg
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
10005, 1, "unable to determine local host name"
// *Cause: The host name could not be determined.
// *Action: Check that the host name for the local machine is valid. Look at the accompanying messages. If the problem persists, contact Oracle Support Services.
/
10006, 1, "APPVIP type needs a VIP name. Specify a VIP name using -vip commandline option."
// *Cause: VIP resource name was missing in the command line for APPVIP type.
// *Action: Specify a VIP name using -vip option.
/
10007, 3, "client ID : %s"
// *Document: NO
// *Cause:
// *Action:
/
10008, 1, "unable to generate client ID for VIP type %s, cluster name %s, VIP resource name %s"
// *Cause: An attempt to generate client ID for the specified cluster name, VIP type and resource name failed. 
// *Action: Ensure that the cluster name and VIP resource name do not exceed 252
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
// *Action: Ensure that the DHCP servers exist on the network and are listening 
//          on port specified. If they are listening on a different port then
//          specify that port using the -port option. For more information refer 
//          to help for 'crsctl discover dhcp' command. 
/
10011, 1, "unable to request DHCP lease for client ID %s on port %d"
// *Cause: An attempt to request DHCP lease for the specified client ID on specified port failed.
// *Action: Ensure that there are DHCP servers with IP addresses available on the network. 
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
// *Action: Ensure that there are DHCP servers listening on port specified. If the DHCP server 
//          is listening on a different port specify an alternative port using -port option. For more
//          information refer to help for 'crsctl release dhcp' command.
/
/
10014, 1, "HOSTVIP type needs a node name. Specify a node name using -n option."
// *Cause: Node name was missing in the command line for HOSTVIP type.
// *Action: For HOSTVIP type node name needs to be specified via -n option.
/
10015, 1, "VIP type %s is invalid"
// *Cause: An invalid VIP type was specified for DHCP client ID generation.
// *Action: Ensure that the VIP type is a valid VIP type. Refer to 
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
10023, 1, "Domain name look up for name %s failed."
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
// *Action: Resubmit the request with an integer value.
/
10037, 3, "    -once               Flag indicating that DNS listener should exit after one DNS query packet is received\n    -v                  Verbose output"
// *Document: NO
// *Cause:
// *Action:
/
10038, 3, "invalid IP address '%s' specified"
// *Cause:  An invalid IPv4 or IPv6 address was supplied on command line.
// *Action: Supply an IP address that conforms to IETF RFC-791 or IETF RFC-2373.
/
10039, 3, "invalid subnet '%s' specified"
// *Cause:  An invalid IPv4 or IPv6 subnet was supplied on the command line.
// *Action: Supply a subnet address that conforms to IETF RFC-950 or IETF RFC-5942.
/
10040, 3, "unable to get list of network interfaces"
// *Cause:  An attempt to retrieve the list of network interfaces failed.
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
10044, 3, "invalid cluster name '%s' specified"
// *Cause:  An invalid cluster name was supplied to the CRSCTL utility.
// *Action: Specify a cluster name which is at least one character long but no
//          more than 15 characters in length. The cluster name consists of
//          alphanumeric characters and the hyphen (-) character
//          (a..z,A..Z,0..9,-). It cannot begin or end with the hyphen (-)
//          character.
/
10045, 3, "invalid node name '%s' specified"
// *Cause:  An invalid node name was supplied to the CRSCTL utility.
// *Action: Specify a node name which is at least one character long but no more
//          than 63 characters in length. The node name consists of alphanumeric
//          characters and the hyphen (-) character (a..z,A..Z,0..9,-).
//          It cannot begin or end with the hyphen (-) character.
/
10046, 3, "invalid client ID '%s' specified"
// *Cause:  An invalid client ID was supplied to the CRSCTL utility.
// *Action: The client ID can be obtained by running the command 'crsctl get 
//          clientid dhcp'. 
/
10047, 3, "invalid query type '%s' specified"
// *Cause:  An invalid DNS query type was supplied to crsctl.
// *Action: Supply a query type of A for an IPv4 address or AAAA for an IPv6 address.
/
10048, 1, "Name '%s' was not resolved to an address of the specified type by name servers '%s'."
// *Cause: An attempt to look up an address of a specified type for the
//         indicated name using the name servers shown did not yield any
//         addresses of the requested type.
// *Action: Retry the request providing a different name or querying for a
//          different IP address type.
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
10104, 00000, "Executable %s does not reside in %s."
// *Cause:  The script crswrapexece.pl attempted to invoke the indicated
//          executable, which was not found in the proper directory.
// *Action: This error is unexpected and should not normally occur. Contact
//          Oracle Support Services.
/
10105, 00000, "Executable %s is not a file."
// *Cause:  The script crswrapexece.pl attempted to invoke the indicated
//          executable, but the executable is not a file.
// *Action: This error is unexpected and should not normally occur. Contact
//          Oracle Support Services.
/
10106, 00000, "Executable %s does not exist."
// *Cause:  The script crswrapexece.pl could not find the specified executable.
// *Action: This error is unexpected and should not normally occur. Contact
//          Oracle Support Services.
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


10201, 1, "Internal error"
// *Cause: An unexpected condition was detected in the cluster event module.
// *Action: Contact Oracle Support Services.
10202, 1, "Failed to allocate process memory"
// *Cause:  Insufficient system memory resources.
// *Action: Correct the system memory resources problem and retry. If this does not appear to be caused by an operating system issue, contact Oracle Support Services.
10203, 1, "Could not connect to the Event Manager daemon"
// *Cause: Unable to communicate with Event Manager daemon.
// *Action: Run the 'crsctl check evmd' command to determine whether Event Manager daemon is properly configured and is running.
///////////////////////////////////////////////////////////////////////////////
/
/ 10250 - 10300: crsctl <action> wallet related messages
/
///////////////////////////////////////////////////////////////////////////////
10250, 0, "Database name is required to access database wallets. Use -name option to supply a database name."
// *Cause: The option -name was missing on the command line.
// *Action: For APPQOSDB wallet types -name is a mandatory parameter. Retry the command with -name option.
/
10251, 0, "User name is required to create OSUSER wallets. Use -user option to supply a username."
// *Cause: The option -user was missing on the command line.
// *Action: For OSUSER wallet types -user is a mandatory parameter. Retry the command with -user option.
/
10252, 3, "Aliases present in the wallet '%s' are: "
// *Documented: NO
// *Cause:
// *Action:
/

//////////////////////////////////////////////////////////////////////////////
/
/ 10301 - 10400: CCL-RD specific messages
/
//////////////////////////////////////////////////////////////////////////////
10301, 0, "Unable to contact Oracle high availability service on peer nodes for cluster wide commands. Details at %s in %s."
// *Cause: Multicast Domain Name Server (mDNS) or Grid Plug and Play (GPnP) or both daemons on the local node were not running.
// *Action: If you are shutting down the Clusterware stack, this is expected. If you had issued a cluster wide command, reissue the command after the stack has been restarted. If you are not shutting down the stack, the missing component(s) may have failed and may restart automatically. Any cluster wide commands can be retried after a few seconds. However, the failure should be investigated and reported to Oracle Support Services.
/
10302, 0, "Oracle high availability service on peer nodes is reachable. Details at %s in %s."
// *Cause: Oracle high availability service on peer nodes was reachable.
// *Action: None.
/

//////////////////////////////////////////////////////////////////////////////
/
/ 10401 - 10500: credential-specific messages
/
//////////////////////////////////////////////////////////////////////////////
10401, 1, "Internal error in credentials processing."
// *Cause: An unexpected condition was detected in the credentials module.
// *Action: Contact Oracle Support Services.
10402, 1, "Failed to allocate process memory."
// *Cause:  There were insufficient system memory resources.
// *Action: Correct the system memory resources problem and retry. If this does not appear to be caused by an operating system issue, contact Oracle Support Services.
10403, 1, "Could not connect to credential storage: %s."
// *Cause: An attempt to communicate with Oracle Cluster Registry (OCR) or Oracle Local Registry (OLR) credential storage failed.
// *Action: Run the 'crsctl check crs' command to determine whether Cluster Ready Services or Oracle High Availability Services are online.
10405, 1, "Credential domain already exists."
// *Cause: The provided credential domain already existed.
// *Action: Specify another credential domain path.
10406, 1, "Authorization error."
// *Cause: The user did not have permissions to view or modify the provided credential information.
// *Action: Use a different user to view or modify the credential information.
10407, 1, "Credential domain does not exist."
// *Cause: The provided credential domain did not exist.
// *Action: Specify another credential domain path or create the credential domain.
10408, 1, "Credential set already exists."
// *Cause: The provided credential set already existed.
// *Action: Specify another credential domain path to which the credential set will be added.
10409, 1, "Credential target already exists."
// *Cause: The provided credential target already existed.
// *Action: Specify another credential target name, or modify the value of the existing one.
10410, 1, "Credential set member does not exist."
// *Cause: The provided credential set member did not exist.
// *Action: Specify another credential set member or create a new member.
10411, 1, "Credential set does not exist."
// *Cause: The provided credential set did not exist.
// *Action: Specify another credential set or create a new member.
10412, 1, "Security layer returned failure: %s."
// *Cause: Credential operation failed due to error from security layer.
// *Action: Depending on the reason, this operation may be retried after correcting the situation.
10413, 1, "Invalid argument specified for attribute."
// *Cause: An invalid argument was found for a given attribute.
// *Action: Rerun the command using correct value.
10414, 1, "User name or group name does not match the owner or group of the credential object."
// *Cause: Credential permissions for the owner could not be modified because the user name did not match the owner of the credential.
// *Action: Specify the owner's user ID in the argument to change owner's permission.
10415, 1, "ACL string is missing the user or group modifier."
// *Cause: The access control list (ACL) string did not specify whether user's or group's permission needs to be changed.
// *Action: Specify the correct format in the argument and rerun the command.
10416, 1, "Credentials target does not exist."
// *Cause: The provided credentials target did not exist.
// *Action: Specify another credentials target.
10417, 1, "The directory '%s' does not exist."
// *Cause: The specified directory did not exist.
// *Action: Provide a directory for which the user has read and write permissions.
10418, 1, "The directory '%s' is not accessible."
// *Cause: An attempt to access the specified directory failed.
// *Action: Ensure that the user has read and write permissions on the directory.
10419, 1, "Unable to open file '%s' for read access."
// *Cause: An attempt to open the specified file for read access failed.
// *Action: Ensure that the user has read access permission on the file.
10420, 1, "Unable to open file '%s' for write access."
// *Cause: An attempt to open the specified file for write access failed.
// *Action: Ensure that the user has write access permission on the file.
10421, 1, "Section name does not exist."
// *Cause: The credentials could not be imported because the provided section name did not exist in the XML file.
// *Action: Verify the sections included in the credentials file and retry the import supplying the correct section name.
10422, 1, "Credential set of type '%s' does not support the specified attribute '%s'."
// *Cause: An attempted operation on a credential set of the indicated type was rejected because it specified an attribute that was not valid for credential sets of that type.
// *Action: Retry the operation specifying an attribute supported for the set.
10423, 1, "Credential file specified is either empty or corrupt."
// *Cause: Credential import failed because the import file was empty or
//         corrupt.
// *Action: Specify a valid credential file and try again.
/
//////////////////////////////////////////////////////////////////////////////
/
/ 10501 - 10700: CLSU specific messages
/
//////////////////////////////////////////////////////////////////////////////
10502, 0001, "failed to delete site '%s' because it was the last remaining site"
// *Cause:  An attempt to delete the indicated site was rejected because it was
//          the last remaining site.
// *Action: Execute the command 'crsctl query cluster site -all' to list the
//          the existing sites. Refer to the command inline help or product
//          documentation for more information.
//
10503, 0001, "invalid site name '%s' specified"
// *Cause:  The indicated string was provided where a site name was required,
//          but it was not a valid site name.
// *Action: Specify a site name which is at least one character long but no more
//          than 15 characters in length. A site name consists of alphanumeric 
//          characters and the hyphen character (a..z,A..Z,0..9,-). It cannot
//          begin or end with the hyphen (-) character.
//
10504, 0001, "The configured site name '%s' is invalid."
// *Cause:  A failure occurred while retrieving site information. The 
//          configured site name was invalid.
// *Action: Contact Oracle Support Services.
//
10505, 0000, "The number of sites defined is more than the maximum."
// *Cause:  A failure occurred while retrieving site information. There were 
//          more sites defined than the maximum allowed.
// *Action: Contact Oracle Support Services.
//
10506, 0002, "The site GUID '%s' configured for site '%s' is invalid."
// *Cause:  A failure occurred while retrieving site information. The 
//          configured site Globally Unique Identifier (GUID) was 
//          syntactically invalid.
// *Action: Contact Oracle Support Services.
//
10507, 0002, "Host '%s' not assigned to a site."
// *Cause:  A failure occurred while retrieving the site assignment for the 
//          indicated host. The host has not been assigned to any site.
// *Action: Contact Oracle Support Services.
//
10508, 0001, "The site '%s' does not exist."
// Cause:  An attempt to query or delete a site failed because the indicated 
//         name had not been defined as a site name.
// Action: Execute the command 'crsctl query cluster site -all' to list the
//         the existing sites. Retry the original command with a site name
//         that has been defined.
//
10509, 0001, "The site '%s' already exists."
// Cause:  An attempt to define an additional site failed because the 
//         indicated name had already been defined as a site name.
// Action: To define an additional site, execute the command 
//         'crsctl query cluster site -all' to list the the existing sites. 
//         Retry the original command with a site name that has not already
//         been defined.
//
10510, 0002, "The site GUID '%s' configured for host '%s' is invalid."
// *Cause:  A failure occurred while retrieving the site information for the 
//          indicated host. The site GUID configured for the indicated host
//          was invalid.
// *Action: Contact Oracle Support Services.
//
10511, 0000, "failed to add site '%s' because the number of sites cannot exceed %d"
// *Cause:  The maximum number of sites were already defined.
// *Action: To add the indicated site name, execute the command 
//          'crsctl query cluster site -all' to list the existing sites, delete
//          an existing site using the command 'crsctl delete cluster site',
//          and retry the original command. Refer to the command inline help or
//          product documentation for more information.
//
10512, 0001, "invalid site GUID '%s' specified"
// *Cause:  An attempt to add a site required for an Exadata Cell was rejected
//          because the supplied Globally Unique Identifier (GUID) was 
//          syntactically invalid.
// *Action: Retry the command specifying the Globally Unique Identifier (GUID) 
//          as a text string of 16 hexadecimal digits (0-f) without a hyphen (-)
//          character or the hexadecimal literal prefix (0x). Refer to the
//          command inline help or product documentation for more information.
//
10513, 0002, "failed to add site '%s' because specified GUID '%s' is already configured"
// Cause:  An attempt to add the indicated site with the indicated Globally
//         Unique Identifier (GUID) was rejected because a site with that GUID
//         had already been defined.
// Action: Execute the command 'crsctl query cluster site -all' to list the
//         existing sites. Retry the original command with a site GUID 
//         that has not already been configured.
//
10514, 0000, "failed to add site '%s' because the number of sites cannot exceed %s"
// *Cause:  An attempt to add the indicated site was rejected because the 
//          maximum allowed number of sites had already been defined.
// *Action: To add the indicated site name, execute the command 
//          'crsctl query cluster site -all' to list the existing sites, delete
//          an existing site using the command 'crsctl delete cluster site',
//          and retry the original command. Refer to the command inline help or
//          product documentation for more information.

//////////////////////////////////////////////////////////////////////////////
/
/ 10701 - 11000: CLSM specific messages
/
//////////////////////////////////////////////////////////////////////////////

10701, 1, "Internal error in cluster management module."
// *Cause: An unexpected condition was detected in the cluster management
//         module.
// *Action: Contact Oracle Support Services.

10702, 1, "could not find cluster property '%s'"
// *Cause: The specified cluster property was not found.
// *Action: Contact Oracle Support Services.

10703, 1, "invalid cluster class '%s' retrieved"
// *Cause: An invalid cluster class was retrieved from the configuration.
// *Action: Contact Oracle Support Services.

//////////////////////////////////////////////////////////////////////////////
/
/   20000-39999: CHA model messages
/
/   20000-23999: OSCWASM model
/   24000-28999: DB model
/
/   Every 10 messages are made for a node in the model. A node can be a problem
/   (target) or probe (observation). For each node, the five messages are
/   listed in the order description, corrective action, details (there can be
/   up to 8 details per node).
//////////////////////////////////////////////////////////////////////////////
/ IP_Protocol_Problems
20000, 1, "IP Protocol Problem"
// *Document: NO
/ TCP_Network_Protocol_Problems
20010, 1, "TCP Network Protocol Problem"
// *Document: NO
/ UDP_Network_Protocol_Problems
20020, 1, "UDP Network Protocol Problem"
// *Document: NO
/ Private_Network_Bandwidth_Problems
20030, 1, "Private Network Bandwidth Problem"
// *Document: NO
/ Private_Network_Problems
20040, 1, "Private Network Problem"
// *Document: NO
20041, 0, "Ensure that the private network used by cluster is functioning properly, including all the cables, network cards, switches and routers etc. between this node and the listed node. Correct any problems discovered."
// *Document: NO
/ V_D_Wait_Problem
20050, 1, "Voting Disk Wait Time Problem"
// *Document: NO
/ V_D_Problems
20060, 1, "Voting Disk Problem"
// *Document: NO
20061, 0, "Verify the staus of the voting file using the 'crsctl query css votedisk' command. Ensure that all elements in the I/O path are working properly. Failure of a majority of voting files results in a node eviction."
// *Document: NO
/ OCSSD_Died_Unexpectedly
20070, 1, "Cluster Synchronization Services Terminated"
// *Document: NO
20071, 0, "The Cluster Synchronization Services is not active. Examine the Oracle Clusterware alert log for messages providing details of the error. If the error is correctable, do so and then issue the 'crsctl start crs' command. If the condition persists, run 'diagcollection.pl' and contact Oracle Support Services."
/
// *Document: NO
20072, 1, "The Cluster Synchronization Services is no longer running."
// *Document: NO
/ CSS_Problems
20080, 1, "CSS Problem"
// *Document: NO
/ OCFS_Problems
20090, 1, "OCFS Problem"
// *Document: NO
/ Runaway_Top_Memory_Consumer
20100, 1, "Runaway Top Memory Consumer Problem"
// *Document: NO
20101, 0, "Verify if this is expected behavior for the above listed process. If the process is managed by Oracle, contact Oracle Support Services."
// *Document: NO
/ Sys_PROC_Rate_Problem
20110, 1, "System Process Creation Rate Problem"
// *Document: NO
/ Sys_FD_Rate_Problem
20120, 1, "System File Descriptor Rate Problem"
// *Document: NO
/ Logon_Storm
20130, 1, "Logon Storm"
// *Document: NO
/ Memory_Starvation_Problem
20140, 1, "Memory Starvation Problem"
// *Document: NO
20141, 0, "The system is running low on memory. Free up memory on system."
// *Document: NO
/ OSTool_Gap
20150, 1, "CHM/OS Data Discontinuity"
// *Document: NO
/ Node_Stats_Reset_Confirm
20160, 1, "Node Statistics Reset"
// *Document: NO
/ Node_Recycled
20170, 1, "Node Recycled"
// *Document: NO
/ Swap_Space_Problem
20180, 1, "Swap Space Problem"
// *Document: NO
/ Swap_Wait_Problem
20190, 1, "Swap Wait Time Problem"
// *Document: NO
/ Swap_In_Problem
20200, 1, "Swap In Problem"
// *Document: NO
/ Swap_Out_Problem
20210, 1, "Swap Out Problem"
// *Document: NO
/ Swapper_Process_Problem
20220, 1, "Swapper Process Problem"
// *Document: NO
/ Swapping_Problem
20230, 1, "Swapping Problem"
// *Document: NO
/ SwapProblems
20240, 1, "Swap Problem"
// *Document: NO
/ Runaway_Top_CPU_Consumer_RT
20250, 1, "Runaway RealTime Top CPU Consumer"
// *Document: NO
/ Runaway_Top_CPU_Consumer
20260, 1, "Runaway Top CPU Consumer"
// *Document: NO
/ Process_High_CPU
20270, 1, "Process High CPU Problem"
// *Document: NO
/ CPU_Starvation_Problem
20280, 1, "CPU Starvation Problem"
// *Document: NO
/ Sys_FD_Usage_Problem
20290, 1, "System File Descriptor Problem"
// *Document: NO
/ CRS_Home_Full
20300, 1, "CRS Home Full"
// *Document: NO
/ Clusterware_Problems
20310, 1, "Clusterware Problems"
// *Document: NO
/ Node_Reboot
20320, 1, "Node Eviction"
// *Document: NO
/ Public_Network_Bandwidth_Problems
20330, 1, "Public Network Bandwidth Problem"
// *Document: NO
/ Public_Network_Problems
20340, 1, "Public Network Problem"
// *Document: NO
20341, 0, "Ensure that the public network used by cluster is functioning properly, including all the cables, network cards, switches and routers etc. between this node and the listed node. Correct any problems discovered."
// *Document: NO
/ ASM_Disk_Problem
20350, 1, "ASM Disk Problem"
// *Document: NO
/ ASM_NonFatal_BG_Problem
20360, 1, "ASM Non Fatal Background Process Problem"
// *Document: NO
/ Incident_Problem
20370, 1, "Incident Problem"
// *Document: NO
/ ASM_Memory_Starvation_Problem
20380, 1, "ASM Memory Starvation Problem"
// *Document: NO
/ ASM_Fatal_BG_Problem
20390, 1, "ASM Fatal Background Process Problem"
// *Document: NO
/ ASM_Instance_Problem
20400, 1, "ASM Instance Problem"
// *Document: NO
/ ASM_Problems
20410, 1, "ASM Problem"
// *Document: NO
/ Node_Degradation
20420, 1, "Node Degradation"
// *Document: NO
/ Space_UnAvailable_Problem
20430, 1, "Space Unavailable Problem"
// *Document: NO
/ OSCW_Root_Problem
20440, 1, "OS-Clusterware Root Problem"
// *Document: NO
/ Runaway_Top_Thread_Consumer
20450, 1, "Runaway Top Thread Consumer Problem"
// *Document: NO
/ Runaway_Top_FD_Consumer
20460, 1, "Runaway Top File Descriptor Consumer Problem"
// *Document: NO
/ CHMOS_Failed
20470, 1, "CHM/OS Failed"
// *Document: NO
/ V_D_Wait
20480, 1, "Voting File Wait Time"
// *Document: NO
20482, 1, "Voting file '%s' has an average wait time of %d milliseconds."
// *Document: NO
/ V_D_Q_Len
20500, 1, "Voting File Queue Length"
// *Document: NO
20502, 1, "Voting file '%s' has an average queue length of %d."
// *Document: NO
/ OCFS_Presence_Test
20520, 1, "OCFS Presence Test"
// *Document: NO
/ ASM_Disk_Observation
20530, 1, "ASM Disk Observation"
// *Document: NO
/ CPUSystem
20540, 1, "System CPU Usage"
// *Document: NO
20542, 1, "The system is using %d%% CPU."
// *Document: NO
/ PhysMemFree
20550, 1, "Free Physical Memory"
// *Document: NO
20552, 1, "The system is running low on memory. The current free memory is %d KB."
// *Document: NO
/ Private_NetworkBW
20560, 1, "Private Network Bandwidth"
// *Document: NO
20562, 1, "Private network interface card '%s' is approaching the bandwidth limit."
// *Document: NO
/ NonOracleVendor_ClusterWare_Test
20570, 1, "NonOracle Vendor ClusterWare Problems"
// *Document: NO
/ OCSSD_dead
20580, 1, "OCSSD Dead"
// *Document: NO
/ Reboot_Message
20590, 1, "Reboot Message"
// *Document: NO
/ UDPProtocolErrors
20600, 1, "UDP Errors"
// *Document: NO
20602, 1, "The system has significant UDP errors over the last %d seconds."
// *Document: NO
/ Syslog_Entry_2
20610, 1, "Operating System Log Entry"
// *Document: NO
/ OSTool_Gap_2
20620, 1, "CHM/OS Data Discontinuity Observation"
// *Document: NO
20622, 1, "The Grid Infrastructure Management Database was missing %d samples or the System Monitor Service restarted on this node."
// *Document: NO
/ VIP_Presence
20630, 1, "Reboot Message"
// *Document: NO
/ Default_Gateway_Ping_Returned
20640, 1, "Default Gateway Ping Returned"
// *Document: NO
/ Username_Lookup_Unresponsive
20650, 1, "Username Lookup Unresponsive"
// *Document: NO
/ Permissions_Problems_Test
20660, 1, "Permissions Problems Test"
// *Document: NO
/ CRS_Stat_VIP_Offline_Test
20670, 1, "CRS Status VIP Offline Test"
// *Document: NO
/ Hostname_Lookup_Unresponsive
20680, 1, "Hostname Lookup Unresponsive"
// *Document: NO
/ Space_UnAvailable
20690, 1, "Space Unavailable"
// *Document: NO
/ Filesystem_UnResponsive
20700, 1, "Filesystem Unresponsive"
// *Document: NO
/ SwapSpaceSize
20710, 1, "Swap Space Size"
// *Document: NO
20712, 1, "The system has free swap space %d KB."
// *Document: NO
/ TCPProtocolErrors
20720, 1, "TCP Errors"
// *Document: NO
20722, 1, "The system has significant TCP errors over the last %d seconds."
// *Document: NO
/ IPProtocolErrors
20730, 1, "IP Errors"
// *Document: NO
20732, 1, "The system has significant IP errors over the last %d seconds."
// *Document: NO
/ CPUQueueLen
20740, 1, "CPU Queue Length"
// *Document: NO
20742, 1, "The number of processes waiting in the run queue is %d per CPU."
// *Document: NO
/ Swap_Wait
20750, 1, "Swap Wait Time"
// *Document: NO
20752, 1, "Swap device '%s' has an average wait time of %d milliseconds."
// *Document: NO
/ Public_NetworkBW
20760, 1, "Public Network Bandwidth"
// *Document: NO
20762, 1, "Public network interface card '%s' is approaching the bandwidth limit."
// *Document: NO
/ Swap_In
20770, 1, "Swap In"
// *Document: NO
20772, 1, "The average system swap in rate is %d KB/second."
// *Document: NO
/ Swap_Out
20780, 1, "Swap Out"
// *Document: NO
20782, 1, "The average system swap out rate is %d KB/second."
// *Document: NO
/ Top_Process_Memory_Usage
20790, 1, "Top Process Memory Usage"
// *Document: NO
20792, 1, "Process '%s' with process identifier %d is consuming %d KB memory out of %d KB total usable memory and growing at a rate of %d KB/second."
// *Document: NO
/ Realtime_Process_Spin_Test
20800, 1, "Realtime Process Spin Test"
// *Document: NO
20802, 1, "The number of real time processes spinning is %d."
// *Document: NO
/ Top_Process_CPU_Usage
20810, 1, "Top Process CPU Usage"
// *Document: NO
20812, 1, "Process '%s' with process identifier %d is consuming %d%% CPU."
// *Document: NO
/ Protocol_Error_Reset
20820, 1, "Protocol Error Statistics Reset"
// *Document: NO
/ Swapper_Process
20830, 1, "Swapper Process CPU Usage"
// *Document: NO
20832, 1, "Process '%s' with process identifier %d is consuming %d%% CPU."
// *Document: NO
/ Sys_PROC_Rate
20840, 1, "System Process Creation Rate"
// *Document: NO
20842, 1, "The increasing rate of number of processes %d is high. The number of processes %d seconds ago was %d."
// *Document: NO
/ Sys_FD_Rate
20850, 1, "System File Descriptor Creation Rate"
// *Document: NO
20852, 1, "The increasing rate of number of open file structures %d is high. The number of open file structures %d seconds ago was %d."
// *Document: NO
/ Top_Process_Thread_Usage
20860, 1, "Top Process Thread Usage"
// *Document: NO
20862, 1, "Process '%s' with process identifier %d has high thread count %d."
// *Document: NO
/ Top_Process_FD_Usage
20870, 1, "Top Process File Descriptor Usage"
// *Document: NO
20872, 1, "Process '%s' with process identifier %d has large number of open file descriptors %d."
// *Document: NO
/ Incident_Obs
20880, 1, "Incident Observation"
// *Document: NO
/ ASM_NonFatal_BG_Obs
20890, 1, "Oracle ASM Non Fatal Background Process"
// *Document: NO
/ ASM_Instance_Fatal_BG
20900, 1, "Oracle ASM Fatal Background Process"
// *Document: NO
20902, 1, "Fatal Background: %s."
// *Document: NO
/ ASM_Memory_Starvation_Obs
20910, 1, "ASM Memory Starvation"
// *Document: NO
/ Sys_FD
20920, 1, "System File Descriptor"
// *Document: NO
20922, 1, "The number of open file structures %d is approaching the system limit of open file descriptors %d."
// *Document: NO
/ CRS_Home_File_System_Usage
20930, 1, "Grid Infrastructure Home File System Usage"
// *Document: NO
20932, 1, "The Grid Infrastructure Home is %d%% full."
// *Document: NO
/ High_FD_Consumer_Problem
20940, 0, "High File Descriptor Consumer Problem"
// *Document: NO
20941, 0, "Verify if this is expected behavior for the above listed process. If the process is managed by Oracle, contact Oracle Support Services."
// *Document: NO
/ High_Thread_Consumer_Problem
20950, 0, "High Thread Consumer Problem"
// *Document: NO
20951, 0, "Verify if this is expected behavior for the above listed process. If the process is managed by Oracle, contact Oracle Support Services."
// *Document: NO
/ High_Memory_Consumer_Problem
20960, 0, "High Memory Consumer Problem"
// *Document: NO
20961, 0, "Verify if this is expected behavior for the above listed process. If the process is managed by Oracle, contact Oracle Support Services."
// *Document: NO
/ High_Memory_Usage
20970, 0, "High Memory Usage"
// *Document: NO
20972, 3, "The process name '%s' with process identifier %d is consuming %d KB memory."
// *Document: NO
/ High_FD_Usage
20980, 0, "High File Descriptor Usage"
// *Document: NO
20982, 3, "The process name '%s' with process identifier %d has %d open file descriptors."
// *Document: NO
/ High_Thread_Usage
20990, 0, "High Thread Usage"
// *Document: NO
20992, 3, "The process name '%s' with process identifier %d has a high thread count %d."
// *Document: NO
/ Abnormal_Process_Problem
21000, 0, "Abnormal Process Problem"
// *Document: NO
/ V_D_Q_Len_Problem
21010, 1, "Voting Disk Queue Length Problem"
// *Document: NO
// Public_NIC_Status
21020, 1, "Public NIC Status"
// *Document: NO
21022, 1, "No activity detected for the public network interface card '%s'."
// *Document: NO
/ Public_NIC_Unavailable
21030, 1, "Public NIC Unavailable"
// *Document: NO
/ 21040 - 21200 used. Do not reuse

//////////////////////////////////////////////////////////////////////////////
/
/   24000-28999: DB model
/
//////////////////////////////////////////////////////////////////////////////
/
/ GC_Block_Slow
24000, 1, "Slow global cache block transfer"
// *Document: NO
24001, 1, "Check load and disk performance on peer nodes."
// *Document: NO
/ Datafile_write_bottleneck
24010, 1, "Data file write bottleneck"
// *Document: NO
24011, 1, "Check CHM/OS data using the 'oclumon dumpnodeview' command for disks with high write timings."
// *Document: NO
/ Datafile_read_bottleneck
24020, 1, "Data file read bottleneck"
// *Document: NO
24021, 1, "Check CHM/OS data using the 'oclumon dumpnodeview' command for disks with high read timings."
// *Document: NO
/ Foreground_direct_IO_slow
24030, 1, "Slow foreground disk I/O"
// *Document: NO
24031, 1, "Check disks hosting instance data files."
// *Document: NO
/ Controlfile_IO_slow
24040, 1, "Slow control file I/O"
// *Document: NO
24041, 1, "Check disks hosting instance control files."
// *Document: NO
/ Cell_disk_IO_saturation
24050, 1, "Exadata cell disk I/O saturated"
// *Document: NO
24051, 1, "Check disk performance of Exadata cells."
// *Document: NO
/ Cell_Failure
24060, 1, "Exadata cell failure"
// *Document: NO
24061, 1, "Check log files on cell nodes. Cell server may be unresponsive or down."
// *Document: NO
/ Disks_offlined_by_ASM
24070, 1, "Disk offlined by ASM instance"
// *Document: NO
24071, 1, "Check Oracle ASM instance log file for disk errors."
// *Document: NO
24072, 1, "Disk offlined by the Oracle ASM instance"
// *Document: NO
/ Sequence_Cache
24080, 1, "Contention on cached database sequence"
// *Document: NO
24081, 1, "Application level tuning. Increase sequence cache."
// *Document: NO
/ Sequence_Nocache
24090, 1, "Contention on uncached database sequence"
// *Document: NO
24091, 1, "Reduce contention on sequence. Evaluate usage of cached sequence."
// *Document: NO
/ Space_management
24100, 1, "Contention due to disk space management"
// *Document: NO
24101, 1, "Tune objects storage parameters."
// *Document: NO
/ Slow_object_checkpoint
24110, 1, "Slow object checkpointing"
// *Document: NO
24111, 1, "Application level tuning."
// *Document: NO
/ Slow_object_reuse_checkpoint_partition_drop_or_truncate
24120, 1, "Object reuse after drop or truncate"
// *Document: NO
24121, 1, "No action required."
// *Document: NO
/ Wait_for_ITL_slot
24130, 1, "Too many concurrent transactions in block"
// *Document: NO
24131, 1, "Reduce concurrency on blocks. If the block is an index block consider reverse indexes."
// *Document: NO
/ Dynamic_Remastering_2
24140, 1, "Waiting for dynamic remastering to complete"
// *Document: NO
24141, 1, "No action required."
// *Document: NO
24142, 1, "Dynamic remastering in progress."
// *Document: NO
/ Instance_waiting_to_shut_down
24150, 1, "Waiting for process to shut down"
// *Document: NO
24151, 1, "No action required."
// *Document: NO
24152, 1, "Waiting for process shutdown."
// *Document: NO
/ Diagnostic_dump_in_progress
24160, 1, "Diagnostic dump in progress"
// *Document: NO
24161, 1, "Check database alert log for dump file name and location."
// *Document: NO
24162, 1, "Diagnostic dump in progress."
// *Document: NO
/ IPC_Send_Timeout_Warning
24170, 1, "Slow or disconnected interconnect"
// *Document: NO
24171, 1, "Check for disconnected interconnect or hung peer node."
// *Document: NO
/ Interconnect_lost_blocks
24180, 1, "Lost blocks on interconnect"
// *Document: NO
24181, 1, "Run ifconfig or check CHM/OS data using the 'oclumon dumpnodeview' command for errors reported on the interconnect NIC. Make sure UDP receive buffers are large enough and flow control is enabled. Make sure flow control is also enabled on the switch."
// *Document: NO
24182, 1, "Transfer of database blocks via interconnect failed."
// *Document: NO
/ Archivelog_disk_space_depleted
24190, 1, "Archiver stuck due to depleted disk space"
// *Document: NO
24191, 1, "Free disk space of archive log destinations."
// *Document: NO
24192, 1, "User may experence hanging sessions because the archiver is unable to archive redo logs."
// *Document: NO
/ Info_Archiver_working
24200, 1, "Archiving in progress"
// *Document: NO
24201, 1, "No action required."
// *Document: NO
24202, 1, "Instance is archiving redo log files."
// *Document: NO
/ Logwriter_slow
24210, 1, "Busy or hung LGWR process"
// *Document: NO
24211, 1, "Check for spinning or hanging LGWR process."
// *Document: NO
/ GC_Block_Busy
24220, 1, "LMS busy on peer node"
// *Document: NO
24221, 1, "Check for busy LMS process on peer node. Make sure LMS is running in realtime scheduling class."
// *Document: NO
/ GC_Block_Congested
24230, 1, "Congested peer node"
// *Document: NO
24231, 1, "Check for overloaded or faulty peer node."
// *Document: NO
/ GC_Grant_Slow
24240, 1, "Slow block grant due to busy peer node"
// *Document: NO
24241, 1, "Check for overloaded or faulty peer node."
// *Document: NO
/ Interconnect_Slow
24250, 1, "Slow interconnect transfer"
// *Document: NO
24251, 1, "Check interconnect performance."
// *Document: NO
24252, 1, "Slow global cache operation due to slow interconnect performance, overload or unresponsive peer node."
// *Document: NO
/ Clusterwide_Problem
24260, 1, "Cluster wide issue"
// *Document: NO
/ Library_cache_concurrency
24270, 1, "Concurrency in library cache"
// *Document: NO
24271, 1, "Application level tuning."
// *Document: NO
/ Index_contention_Block_split
24280, 1, "Index contention because of index block split"
// *Document: NO
24281, 1, "User may experience performance degradation due to index block splits. Avoid monotonically increasing key values on insert."
// *Document: NO
/ Index_contention_Disk_IO
24290, 1, "Index contention because of slow disk I/O"
// *Document: NO
24291, 1, "Check disk performance and reduce concurrency of insert operations."
// *Document: NO
/ DBWR_slow
24300, 1, "Sessions waiting for free buffers"
// *Document: NO
24301, 1, "Check I/O subsystem performance."
// *Document: NO
/ DBWR_slow_due_to_IO
24310, 1, "Sessions waiting for free buffers because of slow disk I/O"
// *Document: NO
24311, 1, "Check I/O subsystem write performance."
// *Document: NO
/ Processes_waiting_for_CF_enqueue
24320, 1, "Processes waiting for control file enqueue"
// *Document: NO
24321, 1, "Check disks hosting instance control files."
// *Document: NO
/ CF_wait_due_to_slow_disk_IO
24330, 1, "Processes waiting for control file enqueue due to slow disks"
// *Document: NO
24331, 1, "Check disks hosting instance control files."
// *Document: NO
/ Slow_disk_access_impacts_buffer_cache
24340, 1, "Disk bottleneck impacts buffer cache"
// *Document: NO
24341, 1, "Tune disk access and reduce contention on buffer cache."
// *Document: NO
/ Log_File_I_O_slow
24350, 1, "Slow I/O to redo log file"
// *Document: NO
24351, 1, "Check performance of disks hosting redo log files."
// *Document: NO
24352, 1, "Performance degradation due to slow log file write."
// *Document: NO
/ Disk_Problem
24360, 1, "Disk I/O issue (Bandwidth)"
// *Document: NO
24361, 1, "Check CHM/OS data using the 'oclumon dumpnodeview' command for excessive disks timings."
// *Document: NO
/ Hot_Blocks
24370, 1, "Transactional row level contention"
// *Document: NO
24371, 1, "Reduce concurrent access to object."
// *Document: NO
/ Disk_I_O_Timeout
24380, 1, "Datafile read or write time exceeds timeout"
// *Document: NO
24381, 1, "Check CHM/OS data using the 'oclumon dumpnodeview' command for faulty disks."
// *Document: NO
/ Logfile_I_O_Timeout
24390, 1, "Logfile write time exceeds timeout"
// *Document: NO
24391, 1, "Check CHM/OS data using the 'oclumon dumpnodeview' command for faulty disks."
// *Document: NO
/ Disk_Error
24400, 1, "Disk error (faulty disk)"
// *Document: NO
24401, 1, "Check CHM/OS data for faulty disks."
// *Document: NO
24402, 1, "Possible disk failure."
// *Document: NO
/ Database_Performance
24410, 1, "Performance issue"
// *Document: NO
/ Process_hang_on_CF_enqueue
24420, 1, "Process waiting for control file enqueue for more than 10 seconds"
// *Document: NO
24421, 1, "Monitor session holding control file enqueue."
// *Document: NO
/ LGWR_hang_on_CF_enq
24430, 1, "LGWR process waiting for controlfile enqueue"
// *Document: NO
24431, 1, "Monitor session holding control file enqueue. May require killing the blocking session."
// *Document: NO
/ Logwriter_slow_due_to_IO
24440, 1, "LGWR process slow due to disk I/O"
// *Document: NO
24441, 1, "Check performance of disks hosting redo log files."
// *Document: NO
/ CPU_Starvation_Problem
24450, 1, "CPU Starvation Problem"
// *Document: NO
24451, 1, "Reduce CPU load and look for over-consuming processes."
// *Document: NO
24452, 1, "Performance degradation due to high CPU utilization."
// *Document: NO
/ Logwriter_slow_due_to_CPU_starvation
24460, 1, "LGWR process slowdown"
// *Document: NO
24461, 1, "Reduce CPU load and look for over-consuming processes."
// *Document: NO
24462, 1, "Slow LGWR process during high CPU load period."
// *Document: NO
/ Wait_for_log_file_switch
24470, 1, "Incomplete checkpoint"
// *Document: NO
24471, 1, "Increase number of log file groups and size of redo log files. Lower FAST_START_MTTR_TARGET to reduce peaks in DBWR activity."
// *Document: NO
24472, 1, "Service degradation due to sessions waiting for log file to switch into next group."
// *Document: NO
/ Database_hang
24480, 1, "Suspected database hang"
// *Document: NO
/ Info_Reconfiguration
24490, 1, "Cluster reconfiguration in progress"
// *Document: NO
24491, 1, "No action required."
// *Document: NO
24492, 1, "Cluster reconfiguration in progress."
// *Document: NO
/ OS_thread_startup_failed
24500, 1, "Thread startup failure"
// *Document: NO
24501, 1, "Check database alert log file for additional information."
// *Document: NO
24502, 1, "OS thread startup failure."
// *Document: NO
/ Information
24510, 1, "Informational message"
// *Document: NO
/ Database_Problems
24520, 1, "General database problem"
// *Document: NO
/ Info_Statistics_collection
24530, 1, "Statistics collection"
// *Document: NO
24531, 1, "No action required."
// *Document: NO
24532, 1, "The database is collecting feature usage and CPU statistics."
// *Document: NO
/ Undo_Segment_Operations
24540, 1, "Undo segment operations in progress"
// *Document: NO
24541, 1, "Application level tuning."
// *Document: NO
/ Commit_propagation_slow
24550, 1, "Slow commit propagation"
// *Document: NO
24551, 1, "Check for overloaded or faulty peer node."
// *Document: NO
/ Streams_flow_control_slows_down_logminer
24560, 1, "Streams flow control slows down log miner"
// *Document: NO
24561, 1, "Check performance of public and private network interface."
// *Document: NO
/ Cursor_pin_waits
24570, 1, "Cursor pin waits"
// *Document: NO
24571, 1, "Application level tuning."
// *Document: NO
/ Cursor_mutex_waits
24580, 1, "Cursor mutex waits"
// *Document: NO
24581, 1, "Application level tuning."
// *Document: NO
/ Private_Network_Problems
24590, 1, "Private Network Problem"
// *Document: NO
24591, 1, "Check CHM/OS data using the 'oclumon dumpnodeview' command for faulty private network connection."
// *Document: NO
/ Memory_Starvation_Problem
24600, 1, "Memory Starvation Problem"
// *Document: NO
24601, 1, "Check CHM/OS data using the 'oclumon dumpnodeview' command for memory starvation."
// *Document: NO
/ gc_cr_block_2_way
24612, 1, "Session %s is waiting for %s milliseconds for global cache transfer to complete."
// *Document: NO
/ gc_cr_block_3_way
24622, 1, "Session %s is waiting for %s milliseconds for global cache transfer to complete."
// *Document: NO
/ gc_current_block_2_way
24632, 1, "Session %s is waiting for %s milliseconds for global cache transfer to complete."
// *Document: NO
/ gc_current_block_3_way
24642, 1, "Session %s is waiting for %s milliseconds for global cache transfer to complete."
// *Document: NO
/ gc_current_block_busy
24652, 1, "Session %s is waiting for %s milliseconds for block from busy peer node."
// *Document: NO
/ gc_cr_block_busy
24662, 1, "Session %s is waiting for %s milliseconds for block from busy peer node."
// *Document: NO
/ gc_cr_request
24672, 1, "Session %s is waiting for interconnect reply."
// *Document: NO
/ gc_current_request
24682, 1, "Session %s is waiting for interconnect reply."
// *Document: NO
/ read_by_other_session
24692, 1, "Slow disk access impacts session %s accessing object '%s'. Block is '%s'."
// *Document: NO
/ buffer_busy_waits
24702, 1, "Slow disk access impacts session %s accessing object '%s'. Block is '%s'."
// *Document: NO
/ latch_cache_buffers_chains
24712, 1, "Transactional row level contention on object %s, block '%s'. SQL ID is '%s'."
// *Document: NO
/ enq_CF_contention
24722, 1, "Session %s is waiting for control file enqueue held by Session '%s'."
// *Document: NO
/ cell_smart_table_scan
24732, 1, "Session %s is waiting for %s milliseconds for disk read to complete."
// *Document: NO
/ cell_multiblock_physical_read
24742, 1, "Session %s is waiting for %s milliseconds for disk read to complete."
// *Document: NO
/ cell_single_block_physical_read
24752, 1, "Session %s is waiting for %s milliseconds for disk read to complete."
// *Document: NO
/ cell_list_of_blocks_physical_read
24762, 1, "Session %s is waiting for %s milliseconds for disk read to complete."
// *Document: NO
/ db_file_parallel_write
24772, 1, "Session %s is waiting for %s milliseconds for disk write to complete. File# is '%s'."
// *Document: NO
/ local_write_wait
24782, 1, "Session %s is waiting for %s milliseconds for disk write to complete. File# is '%s'."
// *Document: NO
/ db_file_scattered_read
24792, 1, "Session %s is waiting for %s milliseconds for disk read to complete. File# is '%s'."
// *Document: NO
/ db_file_sequential_read
24802, 1, "Session %s is waiting for %s milliseconds for disk read to complete. File# is '%s'."
// *Document: NO
/ direct_path_write
24812, 1, "Session %s is waiting for %s milliseconds for disk write to complete. File# is '%s'."
// *Document: NO
/ direct_path_read
24822, 1, "Session %s is waiting for %s milliseconds for disk read to complete. File# is '%s'."
// *Document: NO
/ control_file_sequential_read
24832, 1, "Session %s is waiting for %s milliseconds for control file I/O to complete."
// *Document: NO
/ control_file_parallel_write
24842, 1, "Session %s is waiting for %s milliseconds for control file I/O to complete."
// *Document: NO
/ DFS_lock_handle_SQ
24852, 1, "User may experience performance degradation due to contention on cached sequences. Object ID is '%s'."
// *Document: NO
/ row_cache_lock_dc_sequences
24862, 1, "User may experience performance degradation due to contention on non-cached sequences. Object ID is '%s'."
// *Document: NO
/ enq_SQ_contention
24872, 1, "User may experience performance degradation due to contention on cached sequences. Object ID is '%s'."
// *Document: NO
/ free_buffer_waits
24882, 1, "Database writer waiting for %s milliseconds for disk I/O to complete."
// *Document: NO
/ enq_HW_contention
24892, 1, "Session %s is waiting for high water mark extension. Object ID is '%s'. Block ID is '%s'."
// *Document: NO
/ enq_RO_fast_object_reuse
24902, 1, "Session %s is waiting for %s milliseconds for object checkpoint to complete. Object ID is '%s'."
// *Document: NO
/ enq_KO_fast_object_checkpoint
24912, 1, "Session %s is waiting for %s milliseconds for object checkpoint to complete. Object ID is '%s'."
// *Document: NO
/ enq_CR_block_range_reuse_ckpt
24922, 1, "Session %s is waiting for %s milliseconds for object checkpoint to complete. Object ID is '%s'."
// *Document: NO
/ enq_TX_allocate_ITL_entry
24932, 1, "Contention on data or index block '%s' for object ID '%s'."
// *Document: NO
/ cursor_mutex_X
24942, 1, "Session %s executing module '%s' is waiting for exclusive cursor mutex. SQL ID is '%s'."
// *Document: NO
/ cursor_pin_S
24952, 1, "Session %s executing module '%s' is waiting for shared cursor pin. SQL ID is '%s'."
// *Document: NO
/ cursor_pin_X
24962, 1, "Session %s executing module '%s' is waiting for exclusive cursor pin. SQL ID is '%s'."
// *Document: NO
/ cursor_pin_S_wait_on_X_2
24972, 1, "Session %s executing module '%s' is waiting for exclusive cursor pin. SQL ID is '%s'."
// *Document: NO
/ cursor_mutex_S
24982, 1, "Session %s executing module '%s' is waiting for shared cursor mutex. SQL ID is '%s'."
// *Document: NO
/ log_file_parallel_write
24992, 1, "LGWR process waiting for %s milliseconds for disk write to complete."
// *Document: NO
/ log_file_sync
25002, 1, "Session %s is waiting for %s milliseconds for LGWR process to respond."
// *Document: NO
/ wait_for_scn_ack
25012, 1, "Session %s executing module '%s' is waiting for SCN acknowledge from peer node. SQL ID is '%s'."
// *Document: NO
/ gc_current_grant_busy
25022, 1, "Session %s is waiting for %s milliseconds for block grant from busy peer node."
// *Document: NO
/ gc_cr_grant_busy
25032, 1, "Session %s is waiting for %s milliseconds for block grant from busy peer node."
// *Document: NO
/ gc_current_block_congested
25042, 1, "Session %s is waiting for %s milliseconds for block from congested peer node."
// *Document: NO
/ gc_cr_block_congested
25052, 1, "Session %s is waiting for %s milliseconds for block from congested peer node."
// *Document: NO
/ gc_current_grant_congested
25062, 1, "Session %s is waiting for %s milliseconds for block grant from congested peer node."
// *Document: NO
/ gc_cr_grant_congested
25072, 1, "Session %s is waiting for %s milliseconds for block grant from congested peer node."
// *Document: NO
/ gc_current_grant_2_way
25082, 1, "Session %s is waiting for %s milliseconds for block grant from peer node."
// *Document: NO
/ gc_cr_grant_2_way
25092, 1, "Session %s is waiting for %s milliseconds for block grant from peer node."
// *Document: NO
/ library_cache_mutex_X
25102, 1, "Session %s executing module '%s' is waiting for library cache mutex for %s milliseconds. SQL ID is '%s'."
// *Document: NO
/ enq_TX_index_contention
25112, 1, "Performance degradation due to index contention caused by disk I/O. Object ID is '%s'."
// *Document: NO
/ gc_current_split
25122, 1, "Performance degradation due to index contention caused by block split. Object ID is '%s'."
// *Document: NO
/ enq_CF_contention2
25132, 1, "Slow I/O to control file is causing control file enqueue waits. Session %s is holding control file enqueue."
// *Document: NO
/ enq_TX_row_lock_contention
25142, 1, "Transactional row level contention on object '%s', block '%s'. SQL ID is '%s'."
// *Document: NO
/ db_file_parallel_write_2
25152, 1, "Possible disk failure of data file disk. Wait time is %s milliseconds."
// *Document: NO
/ db_file_scattered_read_2
25162, 1, "Possible disk failure of data file disk. Wait time is %s milliseconds."
// *Document: NO
/ db_file_sequential_read_2
25172, 1, "Possible disk failure of data file disk. Wait time is %s milliseconds."
// *Document: NO
/ log_file_parallel_write_2
25182, 1, "Possible disk failure of log file disk. LGWR process waiting for %s milliseconds."
// *Document: NO
/ os_thread_startup
25192, 1, "Waited %s milliseconds for thread startup."
// *Document: NO
/ enq_US_contention
25202, 1, "Session %s is waiting %s milliseconds for undo segment operations."
// *Document: NO
/ Logwriter_hang_due_to_incomplete_checkpoint
25210, 1, "LGWR hang due to incomplete checkpoint"
// *Document: NO
25211, 1, "Add disks to diskgroup hosting redo logs."
// *Document: NO
/ 25220 - 25830 used. Do not reuse

//////////////////////////////////////////////////////////////////////////////
/
/   29000-29999: VmAgent
/
//////////////////////////////////////////////////////////////////////////////
/
29000, 1, "Oracle VM Manager job failed with the following error:\n%s"
// *Cause:  The Oracle Virtual Machine (Oracle VM) Manager was unable to complete the action due to the indicated error.
// *Action: Consult Oracle Virtual Machine (Oracle VM) documentation if the problem persists.
/
29001, 1, "could not find Grid Infrastructure virtual machine '%s'"
// *Cause:  The name specified for the Grid Infrastructure virtual machine was not found.
// *Action: Specify a known virtual machine, or create a new virtual machine with the specified name and add it to the Oracle Clusterware cluster.
/
29002, 1, "could not find a virtual machine with the ID '%s'"
// *Cause:  The ID specified for the virtual machine was not found.
// *Action: Specify a known virtual machine, or create a new virtual machine with the specified ID.
/
29003, 1, "could not find a virtual machine with the name or ID '%s'"
// *Cause:  Either the name or the ID provided for the virtual machine was not found.
// *Action: Specify a known virtual machine, or create a new virtual machine with the specified name or ID.
/
29004, 0, "not authorized to perform the Oracle VM Manager operation"
// *Cause:  The Oracle Virtual Machine (Oracle VM) user name and password combination did not work, or the user did not have permission to perform the action requested.
// *Action: Update the user's password using the 'srvctl modify ovmm' command, or specify a different user who has the correct permissions.
/
29005, 0, "could not connect to the Oracle VM Manager on host %s at port %s"
// *Cause:  A connection to the Oracle Virtual Machine (Oracle VM) Manager could not be established or timed out.
// *Action: Start the Oracle VM Manager on the appropriate host and port, or specify a different host or port using the 'srvctl modify ovmm' command.
/
29006, 0, "could not find Oracle VM Manager credentials"
// *Cause:  Authentication credentials were not found for the Oracle Virtual Machine (Oracle VM) Manager.
// *Action: Create or modify the credentials by using the 'srvctl {add | modify} ovmm' command.
/

//33001-35000 : CRS ResourceGroup Messages
33210, 1, "could not find resource group '%s'"
// *Cause:  An attempt was made to operate on a resource group that is not
//          registered.
// *Action: Ensure that the resource group name is specified correctly using the command 'crsctl status resourcegroup'.
33500, 1, "cannot stop resource group '%s' because it is not running"
// *Cause:  A request to stop a resource group that is not running was received.
// *Action: Check the current state of the resource group; it should no
//          longer be running.
33501, 1, "Resource group '%s' is disabled."
// *Cause:  The resource group is currently disabled and so may not be operated on.
// *Action: Enable the resource group and re-submit your request.
33503, 1, "Resource group '%s' is in UNKNOWN state and must be stopped first."
// *Cause:  An attempt to start a resource group failed because the group state was UNKNOWN.
// *Action: Stop the resource group manually, make sure it is OFFLINE, and then
//          re-submit the request.
33504, 1, "cannot start resource group '%(1)s' because no online server satisfies its placement policy"
// *Cause:  An attempt to start the indicated resource group failed
//          because no online server satisfies the constraints imposed by its
//          placement policy.
// *Action: Reissue the command after modifying the placement policy for the
//          resource group or adding appropriate servers to the cluster.
33509, 1, "Resource group type '%(1)s' used in dependency '%(2)s' does not exist or is not registered."
// *Cause:  An attempt to configure the dependencies of a resource group was rejected because the 
//          indicated resource group type does not exist.
// *Action: Reissue the command specifying a valid resource group type.
33510, 1, "Resource group '%(1)s' used in dependency '%(2)s' does not exist or is not registered."
// *Cause:  An attempt to configure the dependencies of a resource group was rejected because the 
//          indicated resource group does not exist.
// *Action: Reissue the command specifying a valid resource group.
33514, 1, "Dependency attribute specification '%(1)s' is invalid in resource group '%(2)s'."
// *Cause:  An attempt to configure the dependencies of a resource group failed because of 
//          errors in the dependency specification.
// *Action: Check the accompanying error messages and reissue the command after correcting the
//          dependency specification.
33515, 1, "Circular dependency found for resource group '%(1)s'."
// *Cause:  An attempt to configure the dependencies of a resource group resulted in a
//          circular dependency and was rejected.
// *Action: Reissue the command after correcting the cause of the circular dependency.
33516, 1, "Server pool is not specified for resource group '%s'."
// *Cause:  The resource group profile does not have a server pool specified.
// *Action: Specify an existing server pool in the profile and re-submit the request.
33517, 1, "Required attribute '%(1)s' is not specified for resource group '%(2)s'."
// *Cause:  A required attribute is missing from the resource group profile.
// *Action: Add the attribute to the profile and resubmit the request.
33525, 1, "All instances of the resource group '%s' are already running; relocate is not allowed because the -force option was not specified."
// *Cause:  All instances of the resource group are running and the start 
//          request did not have the -force option specified.
// *Action: Either specify the -force option or re-evaluate the need for the 
//          request.
33526, 1, "There are no available instances of resource group '%(1)s' to start on node '%(2)s'"
// *Cause:  All instances of the resource group were already running or otherwise 
//          unavailable to be started on the specified server.
// *Action: Create more instances or re-evaluate the need for the request.
33527, 1, "unable to start resource group '%(1)s' because it has a '%(2)s' dependency on resource group '%(3)s'"
// *Cause:  Start or relocate of the resource group is impossible because it has a dependency
//          on another entity which prevents it from being able to start.
// *Action: This message will usually be coupled with another one that details
//          the nature of the problem with the other resource group. Follow up
//          on the action recommended for that message.
33528, 1, "unable to start an instance of resource group '%(1)s' because instances are already running on all possible servers."
// *Cause:  An attempt to start an instance of the indicated resource group 
//          failed because instances of that resource group were already 
//          running on all servers available for that resource.
// *Action: Reissue the command after adding more servers or modifying the
//          resource group's placement policy to select more servers.
33529, 1, "unable to act on resource group '%(1)s' on server '%(2)s' because that would require stopping or relocating resource group '%(3)s' but the -force option was not specified"
// *Cause:  The attempted operation on the indicated resource group and server 
//          was rejected because it would have required stopping or relocating 
//          the additional resource group as shown. The -force option would 
//          have been required to allow the additional effects.
// *Action: Reevaluate the request and, if appropriate, specify the -force 
//          option and resubmit.
33534, 1, "Resource group type '%s' is not registered."
// *Cause:  The specified resource group type is not registered.
// *Action: Re-evaluate the request or specify a registered type.
33539, 1, "A resource group with the name '%s' is already registered."
// *Cause:  A resource group with specified name was already registered.
// *Action: Use a unique name for the new resource group.
33547, 1, "illegal attempt to update internal or read-only attribute '%(1)s' for resource group '%(2)s'"
// *Cause:  An internal or read-only attribute of the resource group was specified in the update resource group request.
// *Action: Exclude internal and read-only attributes from your request.
33555, 1, "cannot relocate local resource group '%(1)s'" 
// *Cause:  An attempt to relocate the indicated resource group failed because
//          resource groups of type local cannot relocate to another server.
// *Action: Reissue the command specifying only relocatable resource groups.
33556, 1, "Resource group '%s' cannot be restored to its original state after a failed relocate attempt."
// *Cause:  After an unsuccessful attempt to relocate a resource group, CRSD was unable to restore the resource group.
// *Action: Manual intervention may be required. Re-try starting the resource group.
33558, 1, "Resource group type '%s' cannot be unregistered because there are types that are based on it."
// *Cause:  An attempt was made to unregister a resource group type that has other types inherited from it.
// *Action: Remove inherited types first, then remove this one.
33559, 1, "Resource group type '%(1)s' cannot be unregistered because it has the following resource groups: %(2)s"
// *Cause:  An attempt was made to unregister a resource group type when resource groups based on that type exist.
// *Action: Remove the specified resource groups first, then remove the type.
33560, 1, "Resource group type '%s' does not exist."
// *Cause:  An attempt was made to unregister a resource group type that does not exist.
// *Action: Specify a registered resource group type.
33561, 1, "Resource group type '%(1)s' cannot be unregistered because it is referenced by resource group '%(2)s'."
// *Cause:  An attempt was made to unregister a resource group type when other resource groups are dependent on the type.
// *Action: Make sure there are no existing resource groups that reference this type in their dependencies.
33562, 1, "Resource group '%(1)s' cannot be relocated because it is not running."
// *Cause:  An attempt to relocate the resource group failed because it was not running.
// *Action: Ensure that the resource group is running before issuing the request.
33564, 2, "Failed to relocate resource group '%(1)s'. Will attempt to restore it on '%(2)s' now."
// *Cause:  Relocate of a resource group failed on all possible servers and
//          is now being restarted on original server.
// *Action: None, this is an informational message.
33565, 2, "Attempt to relocate resource group '%(1)s' to '%(2)s' has failed. Will re-retry on '%(3)s' now."
// *Cause: Relocate of a resource group has failed for the server; a retry 
//         is in progress.
// *Action: None, this is an informational message.
33568, 1, "Base resource group type '%s' does not exist."
// *Cause:  An attempt was made to register a resource group type with an unknown base type.
// *Action: Use an existing type as a base. Run 'crsctl status resourcegrouptype' to list registered resource group types.
33571, 1, "Dependency type '%(1)s' is specified more than once for resource group '%(2)s'."
// *Cause:  An attempt to configure the dependencies of a resource group was rejected
//          because a dependency type was used more than once in the profile of the resource group.
// *Action: Reissue the command after combining multiple specifications of the same 
//          dependency type into a single clause.
33585, 1, "cannot unregister built-in resource group type"
// *Cause: An attempt was made to delete a built-in resource group type.
// *Action: Specify a resource group type that is not built-in.
33607, 1, "cannot specify attribute '%s' on a per-server basis"
// *Cause:  An attempt was made to register or update a resource group with an invalid per-server attribute.
// *Action: Check the permitted per-server attributes for the resource group, fix and resubmit. Run 'crsctl status resourcegroup' to check the attributes of the resource group.
33613, 1, "could not find resource group '%s'"
// *Cause:  An attempt was made to operate on a resource group that is not 
//          registered.
// *Action: Check if the resource group is registered. Run 'crsctl status resourcegroup' to list all registered resource groups.
33625, 1, "The owner of resource group '%(1)s' does not have execute permission on pool '%(2)s'."
// *Cause: An attempt to start a resource group referenced a server pool on which the
// owner of the resource group lacks execute permission.
// *Action: Either have the pool's permission changed appropriately or
// use a different pool.
33632, 1, "There are no more servers to attempt to place resource group '%(1)s' that would satisfy its placement policy."
// *Cause: An operation to start, relocate or failover the indicated resource
//         group failed after attempts were made on all available servers.
// *Action: Reissue the command after rectifying the failure condition. 
33640, 1, "Required resource group '%s' is missing."
// *Cause: A resource group that's configured as required is not registered.
// *Action: Register the missing resource group or update the dependency
// specification so as to the missing resource group is not required for
// start.
33643, 1, "The server pools where resource group '%s' could run have no servers."
// *Cause: An attempt to start a resource group failed because all the configured
// server pools have no servers assigned.
// *Action: Either make sure there are active servers in the pools or
// use different pools for the resource group.
33644, 1, "No hosting members of resource group '%s' are online or are allowed to be used by the resource group."
// *Cause: An attempt to start a resource group failed because no server specified as
// hosting member is online or, if it is, may be used by the resource group.
// *Action: Either add more servers to the cluster or request permission to pools to 
// which currently available servers are assigned.
33645, 1, "cannot create resource groups of abstract type '%s'"
// *Cause: An attempt to create a resource group specified an abstract resource group type.
// *Action: Specify a concrete resource group type for the resource group.
33667, 1, "Resource Group '%(1)s' with %(2)s=%(3)s may only run on servers assigned to pools %(4)s and %(5)s, both of which are empty."
// *Cause: An attempt to start a resource group failed because it's  placement policy only allows 
// it to run on servers assigned to the specified pools, and they are all empty.
// *Action: Either change the placement policy of the resource group, or
// change the cluster configuration so that there are servers in those
// pools.
33672, 3, "Attempting to start resource group '%(1)s' on server '%(2)s'"
// *Cause: This is a status message.
// *Action: None.
33673, 3, "Attempting to stop resource group '%(1)s' on server '%(2)s'"
// *Cause: This is a status message.
// *Action: None.
33674, 1, "Start of resource group '%(1)s' on server '%(2)s' failed."
// *Cause: This is a status message.
// *Action: None.
33675, 1, "Stop of resource group '%(1)s' on server '%(2)s' failed."
// *Cause: This is a status message.
// *Action: None.
33676, 3, "Start of resource group '%(1)s' on server '%(2)s' succeeded."
// *Cause: This is a status message.
// *Action: None.
33677, 3, "Stop of resource group '%(1)s' on server '%(2)s' succeeded."
// *Cause: This is a status message.
// *Action: None.
33717, 1, "Server '%(1)s' is not in any of the server pools hosting resource group '%(2)s'."
// *Cause: An attempt was made to start a resource group on a server that is
// not currently an active server in any of the resource group's server pools.
// *Action: Use a server name that is currently an active server of the
// resource group's server pools.
33718, 1, "Server '%(1)s' is not a hosting member of resource group '%(2)s'."
// *Cause: An attempt was made to start the resource group on a server not
// listed as a hosting member of the resource group.
// *Action: Use a server name that is listed as a hosting member.
33719, 1, "Resource group '%(1)s' cannot be started on server '%(2)s' because the server is not in either '%(3)s' or '%(4)s' server pools."
// *Cause: The resource group's placement policy only allows it to run in
// the specified server pools. An attempt was made to start it on a server
// assigned to a different pool.
// *Action: Either use a different server or set the value of
// SERVER_POOLS to *, which will allow the resource to run on any server.
33722, 1, "The instance of resource group '%(1)s' can only run on server '%(2)s'; check on server '%(3)s' is unnecessary."
// *Cause: A check was issued on a server for a resource group instance that can only
// run on a particular server.
// *Action: Issue a check on the server where the resource group instance is
// supposed to be run.
33723, 1, "No instance of resource group '%(1)s' found on server '%(2)s'."
// *Cause: A check command failed because the resource group was not running on the specified server
// and no offline instances were available for the resource group.
// *Action: Reissue the command, specifying a server where a resource group instance 
// might be running.
33728, 1, "A resource group type with the name '%s' is already registered."
// *Cause:  An attempt to register a resource group type specified a name that is already registered.
// *Action: Use a unique name for the new resource group type.
33729, 1, "Attribute '%s' cannot be overridden for a resource group type."
// *Cause: An attribute was specified that is not allowed in a resource group type.
// *Action: Do not specify the indicated attribute for a resource group type.
33730, 1, "Resource group '%s' depends on resource group '%s'."
// *Cause: An attempt to unregister a resource group failed because another resource
//         group is dependent on it.
// *Action: Reissue the command after removing all dependencies on the resource group to
//          be unregistered.
33731, 1, "The resource group '%(1)s' is already running on target server '%(2)s'."
// *Cause: An attempt to relocate the indicated resource group failed because
//         the resource group was already running on the indicated server.
// *Action: No action is required.
33736, 1, "cannot proceed with command because it requires stopping resource group '%(1)s' on server '%(2)s'"
// *Cause: The command failed because the force option was not specified to
//         stop the indicated resource groups.
// *Action: Reissue the command after adding more servers to the cluster or 
//          specify the force option.
33779, 1, "Failed to delete resource group type '%(1)s' from repository. Details at %(2)s in %(3)s."
// *Cause: An attempt to delete a resource group type encountered an internal error while updating the repository.
// *Action: Use the ocrcheck utility to detect errors in OCR. If problems exist, the registry may need to be recovered or restored.
33789, 1, "cannot stop resource group '%(1)s' because it is not running on server '%(2)s'"
// *Cause:  An request to stop a resource group on a server where it is not
//          running was received.
// *Action: Check the current state of the resource group; it should no
//          longer be running on that server.
33801, 1, "No instance of resource group '%s' should be running."
// *Cause: An attempt to relocate a resource group was rejected  because the TARGET attributes of the instances of the resource group were set to OFFLINE.
// *Action: Restart the resource group to change the value of the TARGET attribute to ONLINE. 
33805, 1, "cannot start resource group '%(1)s' because it has a '%(2)s' dependency on resource group type '%(3)s' and no resource group of that type can satisfy the dependency"
// *Cause:  An attempt to start the indicated resource group failed because a
//          resource group of the indicated type did not exist to satisfy the dependency.
// *Action: Reissue the command after registering a resource group of the indicated type.
33828, 1, "failed to stop resource group while attempting CARDINALITY modification"
// *Cause: An attempt to stop a resource group during CARDINALITY modification failed.
// *Action: Use 'crsctl stop resourcegroup' to stop the resource group manually and then retry the update operation.
33835, 1, "Resource group '%(1)s' cannot start on server '%(2)s' because the server does not belong to the resource group's server category."
// *Cause: An attempt to start the resource group group failed because the server specified does not
// belong to the server category of the resource group.
// *Action: Specify a server that belongs to the category.
33837, 1, "There are no servers that belong to the server category '%(1)s' of resource group '%(2)s'."
// *Cause: The resource group cannot be started as there are no available servers that belong to its category.
// *Action: Add servers to the cluster or change the category to be more inclusive.
33855,3, "Resource group '%(1)s' is not configured to run in server pool '%(2)s'."
// *Cause: An attempt was made to start or stop the resource group in a server pool where the resource group was not configured to run.
// *Action: Modify resource group's attribute to have this server pool or specify a different resource group.
33857, 1, "cannot stop resource group '%(1)s' because it is not running in server pool '%(2)s'"
// *Cause: A resource group stop request specified a server pool on which the resource group is not running. 
// *Action: Check the current state of the resource group; it should no
//          longer be running in that server pool.
33904, 1, "cannot relocate resource group '%(1)s' because it is not a singleton resource group"
// *Cause: A relocate resource group request specified a resource group that
//         has multiple instances.
// *Action: Reissue the request specifying a singleton resource group or
//          use a filter that resolves to an instance of the group.
33919, 1, "Resource group '%s' has no instances to act upon."
// *Cause: An attempt was made to act on a resource group that has no
// instances because it is configured to run on servers that
// have never existed in the cluster.
// *Action: Retry the command when the resource group has instances.
33969, 1, "cannot add resource group '%s' because a resource exists with the same name"
// *Cause: An attempt to add a resource group failed because a resource with
//         the same name was already registered.
// *Action: Reissue the command specifying a different name for the new resource group.
34801, 3, "  crsctl modify resourcegroup <rgName> -attr \"<specification>[,...]\" [-f] [-delete] [-i]\n     <specification>:   {<attrName>=<value> | <attrName>@<scope>=<value>}\n        <scope>:   {@SERVERNAME(<server>) |\n                       @CARDINALITYID(<cid>) }\nwhere"
34802, 3, "     rgName          Modify named resourcegroup\n     attrName        Attribute name\n     value           Attribute value\n     server          Server name\n     cid             Resource group cardinality ID\n     -f              Force option\n     -delete         Delete named attribute\n     -i              Fail if request cannot be processed immediately"
34803, 3, "  crsctl add resourcegroup <rgName> -type <rgtypeName> [[-file <filePath>] | [-attr \"<specification>[,...]\"]] [-f] [-i]\n     <specification>:   {<attrName>=<value> | <attrName>@<scope>=<value>}"
34804, 3, "  crsctl delete resourcegroup {<rgName> [...]|-w <filter>} [-f] [-i]\nwhere \n    rgName [...]   One or more resource group names to be deleted\n    -w             Resource group filter (e.g., \"TYPE = rgtype1\")\n    -f             Force option\n    -i             Fail if request cannot be processed immediately"
34805, 3, "  crsctl delete resourcegrouptype {<typeName> [...]|-w <filter>} [-i]\nwhere \n    typeName [...]  One or more blank-separated resource group type names\n    -w              Type filter (e.g., \"TYPE_NAME = test_type\")\n    -i              Fail if request cannot be processed immediately"
34806, 3, "     rgName          Add named resource group\n     rgtypeName      Resource group type\n     filePath        Attribute file\n     attrName        Attribute name\n     value           Attribute value\n     server          Server name"
34807, 3, "     cid             Resource cardinality ID\n     -f              Force option\n     -i              Fail if request cannot be processed immediately"
34808, 3, "        <scope>:   {@SERVERNAME(<server>) |\n                       @CARDINALITYID(<cid>)}\nwhere"
34809, 3, "  crsctl add resourcegrouptype <rgtypeName> -basetype <baseTypeName> {-file <filePath> | -attr \"ATTRIBUTE=<attrName>,TYPE={string|int}[,DEFAULT_VALUE=<defaultValue>][,FLAGS=<typeFlags>][,...]\" } [-i]\nwhere"
34810, 3, "     rgtypeName     Add named resource group type\n     baseTypeName   Base resource group type\n     filePath       Attribute file\n     attrName       Attribute name\n     defaultValue   Default value"
34811, 3, "     typeFlags      One or more flag values separated by '|':\n       CONFIG         Attribute may be configured\n       READONLY       Attribute is read-only\n       REQUIRED       Attribute value is required\n       HOTMOD         Attribute is hot-modifiable\n     -i             Fail if request cannot be processed immediately"
34812, 3, "  crsctl modify resourcegrouptype <rgtypeName> -attr \"ATTRIBUTE=<attrName>[,TYPE={string|int}][,DEFAULT_VALUE=<defaultValue>][,FLAGS=<typeFlags>][,...]\" [-f] [-i]\nwhere"
34813, 3, "     rgtypeName     Modify named resource group type attributes\n     attrName       Attribute name\n     defaultValue   Default value\n     typeFlags      One or more flag values separated by '|':"
34814, 3, "       CONFIG         Attribute may be configured\n       READONLY       Attribute is read-only\n       REQUIRED       Attribute value is required\n       HOTMOD         Attribute is hot-modifiable\n     -f             Force option\n     -i             Fail if request cannot be processed immediately"
34815, 3, "  crsctl start resourcegroup {<rgName> [...]|-w <filter>]|-all} [-n <server> | -s <server_pools>] [-k <cid>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i] [-l] \n     Start designated resource groups\nwhere"
34816, 3, "     rgName [...]     One or more blank-separated resource group names\n     -w               Resource Group filter (e.g., \"TYPE = ora.database.type\")\n     -all             All resource groups\n     -n               Server name\n     -k               Resource Group cardinality ID"
34817, 3, "     -env             Attribute overrides for this command\n     -f               Force option\n     -i               Fail if request cannot be processed immediately\n     -l               Leave affected resource groups as-is if request fails"
34818, 3, "\n     -s               Server pool names (e.g. -s  pool1 pool2)\n" 
34819, 3, "  crsctl stop resourcegroup {<rgName>[...]|-w <filter>|-all} [-n <server> | -s <server_pools>] [-k <cid>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i] [-l] \n     Stop designated resource groups\nwhere"
// Msg 34820 continued in msg 6569
34820, 3, "     rgName [...]     One or more blank-separated resource group names\n     -w               Resource group filter (e.g., \"TYPE = ora.database.type\")\n     -all             All resource groups\n     -n               Server name\n     -k               Resource cardinality ID\n     -env             Attribute overrides for this command\n"
34821, 3, "     -l               Leave affected resource groups as-is if request fails\n     -s               Server pool names (e.g. -s  pool1 pool2)\n"
34822, 3, "  crsctl status resourcegrouptype [<rgtypeName>[...]|-w <filter>] [-p|-f|-g]\n     Check status of designated resource group types\nwhere \n     rgtypeName [...]  One or more blank-separated resource group type names"
34823, 3, "     -w                Resource group type filter (e.g., \"BASE_TYPE = cluster_resourcegroup\")\n     -g                Check if resource group types are registered\n     -p                Print static configuration\n     -f                Print full configuration"
34824, 3, "  crsctl status resourcegroup [<rgName>[...]|-w <filter>] [-p [-attr <attribName>[,...] [-noname]] |-v [-attr <attribName>[,...] [-noname]]] | [-f|-l|-g] | [[-k <cid>|-n <server>] [-e [-p|-v]] ] | [-s -k <cid> ] | [-noauto]\n     Check status of designated resource groups\n\n  crsctl status resourcegroup [<rgName>[...]|-w <filter>] -t [-x]"

// Msg 34825 continued in msg 6570
34825, 3, "     Print status of resource groups in tabular format\n\n  crsctl status resourcegroup [<rgName>[...]] -dependency [-stop | -pullup]\n    Print resource group dependencies\nwhere \n     rgName [...]      One or more blank-separated resource group names\n     -w                Resource group filter (e.g., \"TYPE = ora.database.type\")"

34826, 3, "     -attr             Print specific attributes\n     -noname           Bypass the default printing of the resource group name\n     -e                Evaluate a resource group instance's special values\n     -f                Print full configuration\n     -l                Print all cardinality members"
// Msg 34827 continued in msg 34843 & 6571
34827, 3, "     -g                Check if resource groups are registered\n     -k                Cardinality ID\n     -n                Server name\n     -s                Get target servers for relocation\n     -t                Tabular display\n     -x                Display member resources\n     -noauto           Do not display automatic resource groups"
34828, 1, "Sample filters:\n1. TYPE = type1\n2. ((TYPE = type1) AND (CHECK_INTERVAL > 50))\n3. (TYPE = type1) AND ((CHECK_INTERVAL > 30) OR (AUTO_START co never))"
34829, 3, "  crsctl relocate resourcegroup {<rgName> [-k <cid>]| -all|-w <filter>} -s <server> [-n <server>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]\n     Relocate designated resource groups"
// Msg 34830 continued in msg 6572
34830, 3, "\nwhere\n     rgName         Resource group name\n     -all           Relocate all resource groups\n     -s             Source server\n     -w             Resource group filter (e.g., \"TYPE = ora.database.type\")\n     -n             Destination server\n     -k             Cardinality ID\n     -env           Attribute overrides for this command\n"
34831, 3, "  crsctl eval add resourcegroup <rgName> -type <typeName> [-file <filePath> | -attr  \"<attrName>=<value>[,...]\"]  [-f]\n    Evaluate add of specified resource group"
34832, 3, "where\n     rgName          Name of the resource group\n     typeName        Resource group type\n     attrName        Attribute name\n     value           Attribute value\n     -f              Evaluate as with force option\n\n"
34833, 3, "  crsctl eval modify resourcegroup <rgName> -attr \"<attrName>=<value>[,...]\" [-f] \n    Evaluate modification of specified resource group"
34834, 3, "where\n     rgName          Name of the resource group\n     attrName        Attribute name\n     value           Attribute value\n     -f              Evaluate as with force option\n\n"
34835, 3, "  crsctl eval start resourcegroup {<rgName>|-w <filter>}[-n server] [-f]\n    Evaluate start of specified resource groups"
34836, 3, "where\n     rgName         Name of a resource group\n     -w             Resource group filter\n     -n             Server Name\n     -f             Evaluate as with force option\n\n"
34837, 3, "  crsctl eval stop resourcegroup {<rgName>|-w <filter>} [-f]\n    Evaluate stop of specified resource groups"
34838, 3, "where\n     rgName         Name of a resource group\n     -w             Resource group filter\n     -f             Evaluate as with force option\n\n"
34839, 3, "  crsctl eval relocate resourcegroup {<rgName> | -all} -s <server> | -w <filter>} {-n <server>} [-f]\n    Evaluate relocate of specified resource groups"
34840, 3, "\nwhere\n     rgName         Name of a resource group\n     -all           Relocate all resource groups\n     -s             Source server\n     -w             Resource group filter (e.g., \"TYPE = ora.database.type\")\n     -n             Destination server\n     -f             Evaluate as with force option\n\n"
34841, 3, "  crsctl eval fail resourcegroup {<rgName> | -w <filter>} [-n <server>] [-env \"<attr>=<val>[,...]\"]\n    Evaluate failure of specified resource group"
34842, 3, "where\n     rgName          Name of the resource group\n     -w              Resource group filter\n     -n              Server Name\n     -env            Attribute overrides for this command\n\n"
34843, 3, "     -dependency       Display resource group dependencies, default is start dependencies"
34844, 3, "Resource group '%s' is registered."
34845, 3, "Resource group '%s' is not registered."
34846, 3, "  crsctl check resourcegroup {<rgName> [...]|-w <filter>} [-n <server>] [-k <cid>]\n     Check status of resource groups\nwhere \n     rgName [...]     One or more blank-separated resource group names\n     -w               Resource group filter (e.g., \"TYPE = ora.database.type\")\n     -n               Server name\n"
34847, 3, "     -k               Resource group cardinality ID"
34848, 3, "  crsctl check resourcegroup {<rgName> [...]|-w <filter>} [-n <server>] [-k <cid>] \n     Check status of resource groups"
34849, 3, "  crsctl restart resourcegroup {<rgName> [...]|-w <filter>} [-k <cid>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i]  \n     Restart specified resource groups\nwhere"
34850, 3, "     rgName [...]     One or more blank-separated resource group names\n     -w               Resource group filter (e.g., \"TYPE = ora.database.type\")\n     -k               Resource group cardinality ID"
34851, 3, "     -env             Attribute overrides for this command\n     -f               Force option\n     -i               Fail if request cannot be processed immediately\n"
34852, 3, "  crsctl restart resourcegroup {<rgName> [...][-w <filter>] [-k <cid>] [-env \"env1=val1,env2=val2,...\"] [-f] [-i] "
34901, 0, "Register Resource Group"
// *Document: NO
34902, 0, "Unregister Resource Group"
// *Document: NO
34903, 0, "Register Resource Group Type"
// *Document: NO
34904, 0, "Unregister Resource Group Type"
// *Document: NO
34905, 0, "Start Resource Group"
// *Document: NO
34906, 0, "Stop Resource Group"
// *Document: NO
34907, 0, "Relocate Resource Group"
// *Document : NO
34908, 0, "Resource Group State Change"
// *Document : NO
34909, 0, "Check Resource Group State"
// *Document: NO
34911,0,  "cannot delete the resource group because it does not exist"
// *Cause:  An attempt to delete a resource group failed because the resource group specification did not identify an existing resource group. Either there was no resource group with the specified name, or no resource group satisfied the specified filter.
// *Action:  Reissue the command specifying the name of an existing resource group or a filter that will select an existing resource group.
34912,0,  "cannot delete the resource group type because it does not exist"
// *Cause:  An attempt to delete a resource group type failed because the resource group type specification did not identify an existing resource group type. Either there was no resource group type with the specified name, or no resource group type satisfied the specified filter.
// *Action:  Reissue the command specifying the name of an existing resource group type or a filter that will select an existing resource group type.
34913, 3, "Restored the state of resource group '%(1)s' on server '%(2)s'"
// *Cause: This is a status message.
// *Action: None.
34914, 0, "Resource '%(1)s' is already a member of resource group '%(2)s'."
// *Cause: An attempt was made to add a resource to a group while the resource was already a member of another group.
// *Action: Reissue the command after removing the resource from its current group.
34915, 0, "cannot add local resource '%(1)s' to cluster resource group '%(2)s'"
// *Cause: An attempt was made to add a local resource to a cluster resource group. Only cluster resources can be added to a cluster resource group.
// *Action: Reissue the command by specifying only cluster resources.
34916, 0, "cannot add cluster resource '%(1)s' to local resource group '%(2)s'"
// *Cause: An attempt was made to add a cluster resource to a local resource group. Only local resources can be added to a local resource group.
// *Action: Reissue the command by specifying only local resources.
34917, 0, "Resource '%(1)s' cannot be added to resource group '%(2)s' because their '%(3)s' attribute values are not identical."
// *Cause: An attempt was made to add a resource to a resource group when the resource's profile is not compatible with the group.
// *Action: Reissue the command after updating the resource's profile to match the resource group's profile or specify a compatible resource group.
34918, 0, "cannot register resource group '%s' because CRITICAL_RESOURCES attribute is not specified"
// *Cause: An attempt was made to add a resource group without specifying the critical resources of the group.
// *Action: Reissue the command after designating some resource(s) as critical for the group.
34919, 0, "cannot register resource group '%(1)s' because critical resource '%(2)s' is not a member of the group"
// *Cause: An attempt was made to add or update a resource group and an 
//         invalid resource was specified as critical.
// *Action: Reissue the command after correcting the CRITICAL_RESOURCES 
//          attribute of the group or specify the -force option.
34920, 0, "Dependency type '%(1)s' not supported for resource '%(2)s' because it is a member of resource group '%(3)s'"
// *Cause: A dependency type was specified for a resource that is not supported when a resource is a member of a group.
// *Action: Reissue the command, specifying a supported dependency type.
34921, 0, "Resource '%(1)s' cannot have a dependency on resource '%(2)s' because they are not members of the same resource group."
// *Cause: An attempt was made to define a dependency between resources who are not members of the same resource group.
// *Action: Reissue the command, specifying a target resource that is member of the group.
34922, 0, "cannot modify internal resource group '%s'"
// *Cause: An attempt was made to modify an internal resource group created by Oracle Clusterware.
// *Action: Reissue the command by specifying an appropriate resource group.
34923, 0, "cannot delete internal resource group '%s'"
// *Cause: An attempt was made to delete an internal resource group created by Oracle Clusterware.
// *Action: Reissue the command by specifying an appropriate resource group.
34924, 0, "cannot start resource group '%(1)s' because it is incomplete"
// *Cause: An attempt to start a resource group failed because it had not been completely populated.
// *Action: Check the RESOURCE_LIST and CRITICAL_RESOURCES attributes of the resource group, ensure they are not blank and retry.
34925, 0, "cannot start resource '%(1)s' outside of its resource group '%(2)s'"
// *Cause: An attempt to start the indicated critical resource of the indicated resource group failed because critical resources cannot be started independently of the group.
// *Action: Start the resource group and that will start the critical resources of the group.
34926, 0, "cannot start resource '%(1)s' because its resource group '%(2)s' is not running"
// *Cause: An attempt to start the indicated resource of the indicated resource group failed because the resource group was not online.
// *Action: Start the resource group before attempting to start the resources of the group.
34927, 0, "cannot stop resource '%(1)s' outside of its resource group '%(2)s'"
// *Cause: An attempt to stop the indicated resource of the indicated resource group failed because it was a critical resource necessary for continuing group operation.
// *Action: To stop the indicated resource, stop the entire resource group.
34928, 0, "cannot modify critical resources of a resource group when it is running"
// *Cause: An attempt was made to modify the CRITICAL_RESOURCES attribute of a resource group when it was running.
// *Action: Reissue the command after stopping the resource group on all servers.
34929, 0, "cannot remove critical resource '%(1)s' from resource group '%(2)s'"
// *Cause: An attempt was made to remove a critical member resource of a resource group.
// *Action: Reconsider the removal. If it is necessary, update the CRITICAL_RESOURCES attribute of the group to categorize the resource as not critical, then reissue this command.
34930, 0, "cannot remove resource '%(1)s' from resource group '%(2)s' because another resource in the group '%(3)s' is dependent on it"
// *Cause: An attempt was made to remove a member resource of a group when other group members were dependent on it.
// *Action: Reconsider the removal. If it is necessary, update other resources in the group to remove dependencies on the indicated resource, then reissue the command.
34931, 0, "cannot remove resource '%(1)s' from resource group '%(2)s' because it is dependent on other resources in the group"
// *Cause: An attempt was made to remove a member resource of a group when it was dependent on other resources in the group.
// *Action: Reconsider the removal. If it is necessary, update the indicated resource to remove all dependencies, then reissue the command.
34932, 0, "cannot delete resource '%(1)s' because it is a member of resource group '%(2)s'"
// *Cause: An attempt was made to delete a resource that was a member of a resource group.
// *Action: Reissue the command after removing the resource from the resource group.
34933, 0, "cannot start resource group '%(1)s' because it is in debug mode"
// *Cause: An attempt to start the resource group failed because the DEBUG attribute was set to 1.
// *Action: Reissue the command after setting the DEBUG attribute of the resource group to 0.
34934, 0, "cannot set resource group '%(1)s' to debug mode because it is ONLINE"
// *Cause: An attempt to update the DEBUG attribute of the resource group failed because it was running.
// *Action: Reissue the command after stopping the resource group on all servers.
34935, 0, "cannot clear debug mode of resource group '%(1)s' because some members are ONLINE"
// *Cause: An attempt to update the DEBUG attribute of the resource group failed because some member resources were running.
// *Action: Reissue the command after stopping all member resources of the indicated group.
34936, 3, "Found no resource groups to stop."
34937, 3, "Found no resource groups to start."
34938, 3, "No resource groups found running on server '%(1)s'."
34939, 0, "Resource group '%(1)s' is not running on server '%(2)s'."
// *Cause: An attempt to relocate the resource group failed because it was not running on the specified server.
// *Action: Ensure that the correct server is specified and reissue the command.
34940, 0, "cannot add resource '%(1)s' to resource group '%(2)s' because the resource is online"
// *Cause: An attempt to add a resource to a resource group was rejected because the resource was online.
// *Action: Reissue the command after stopping the resource on all servers.
34941, 0, "cannot delete resource group '%(1)s' because it has member resources"
// *Cause: An attempt to delete a resource group failed because because it had member resources.
// *Action: Reissue the command after removing all resources from the group.
34942, 1, "User '%(1)s' does not have sufficient permissions to update the resource group '%(2)s'."
// *Cause: An attempt to update the resource group of a resource was rejected because the user did not have update privileges on the resource group.
// *Action: Reissue the command after update privileges have been granted on the resource group.
34943, 1, "cannot add resource '%(1)s' to resource group '%(2)s' because the resource group owner '%(3)s' cannot operate on the resource"
// *Cause: An attempt to add a resource to a resource group was rejected because the resource group owner did not have execute privileges on the resource.
// *Action: Reissue the command after granting execute privileges on the resource to the resource group owner.
34944, 0, "Resource group '%(1)s' cannot be started because the critical resource '%(2)s' is disabled."
// *Cause: An attempt to start the indicated resource group failed because a critical resource was disabled.
// *Action: Reissue the command after enabling the indicated critical resource.
34945, 0, "cannot configure attribute '%(1)s' because the resource is a member of a resource group"
// *Cause: An attempt to update an attribute of a member resource was rejected because that attribute cannot be configured at an individual resource level.
// *Action: Reissue the command after removing the indicated attribute.
34946, 0, "Invalid dependency modifier '%(1)s' specified for a group member resource."
// *Cause: An attempt to configure the dependencies of a resource was rejected because the indicated modifier was invalid for resources belonging to a group.
// *Action: Reissue the command without the indicated modifier in the dependency specification of the resource.
34947, 3, "Resource group '%(1)s' is already running on '%(2)s'."
// *Cause: This is a status message.
// *Action: None.
34948, 0, "cannot start resource group '%(1)s' because critical resource '%(2)s' is not a member of the group"
// *Cause: An attempt was made to start a resource group and an invalid 
//         resource was specified as critical.
// *Action: Reissue the command after correcting the CRITICAL_RESOURCES 
//          attribute of the group.
/
//////////////////////////////////////////////////////////////////////////////
/
/   40000-41000: CLSCAL specific messages
/
//////////////////////////////////////////////////////////////////////////////
/
40002, 3, "No activities match the query."
// *Cause: There were no activities found in the cluster activity log that matched the query provided.
// *Action: Verify the query parameters and retry.
40003, 1, "Cluster Synchronization Services is unavailable."
// *Cause: The requested operation failed because of a failure to communicate with the Cluster Synchronization Services daemon.
// *Action: Run the command 'crsctl check css' to determine whether the Cluster Synchronization Services daemon is properly configured and is running.
40004, 1, "authorization wallet not found"
// *Cause: An attempt to access the cluster activity log failed because the authorization wallet could not be found.
// *Action: Contact Oracle Support Services.
40005, 1, "internal error"
// *Cause: An unexpected condition was detected in the cluster activity log module.
// *Action: Contact Oracle Support Services.
40006, 1, "unable to allocate process memory"
// *Cause:  The requested operation failed because of a failure to allocate process memory. This was probably due to a lack of system resources.
// *Action: Correct the system memory resources problem and retry. If this does not appear to be caused by an operating system issue, contact Oracle Support Services.
40007, 1, "unable to connect to the Event Manager daemon"
// *Cause: The requested operation failed because of a failure to communicate with the Event Manager daemon.
// *Action: Run the command 'crsctl check evmd' to determine whether the Event Manager daemon is properly configured and is running.
40008, 1, "insufficient permission for accessing the cluster activity log"
// *Cause: A non-privileged user attempted to view or modify the cluster activity log.
// *Action: Issue the command again as a privileged user.
40009, 1, "invalid filter expression '%s'"
// *Cause: An attempt to access the cluster activity log failed because the specified filter was invalid.
// *Action: Correct the syntax of the filter being provided and try again.
40010, 1, "invalid regular expression '%s'"
// *Cause: An attempt to access the cluster activity log failed because the specified regular expression was invalid.
// *Action: Correct the syntax of the regular expression being provided and try again.
40011, 1, "unable to connect to the Oracle Cluster Registry: %s"
// *Cause: An attempt to communicate with the Oracle Cluster Registry (OCR) or the Oracle Local Registry (OLR) failed.
// *Action: Run the command 'crsctl check crs' to determine whether Cluster Ready Services or Oracle High Availability Services are online.
40012, 0, "Cluster activity log is not supported in this configuration."
// *Cause: The Grid Infrastructure Management Repository was not configured.
// *Action: Re-Install Grid Infrastructure and ensure that the Grid 
//          Infrastructure Management Repository is configured.
40013, 3, "cluster activity log maximum size below minimum of 100 MB"
// *Cause: An attempt to set the maximum size of the cluster activity log specified a value less than the minimum of 100 MB.
// *Action: Specify a maximum size of 100 MB or more.
40014, 1, "invalid timestamp '%s'"
// *Cause: An attempt to access the cluster activity log failed because the specified timestamp was invalid.
// *Action: Reissue the command with a valid timestamp. Refer to the command line help for more information.
40015, 1, "invalid duration '%s'"
// *Cause: An attempt to access the cluster activity log failed because the specified duration was invalid.
// *Action: Reissue the command with a valid duration. Refer to the command line help for more information.
40016, 3, "Setting the maximum size for cluster activity log failed."
// *Cause: The cluster activity log maximum size could not be modified.
// *Action: See the accompanying error message and respond accordingly.
40017, 3, "Setting the retention time for cluster activity log failed."
// *Cause: The cluster activity log retention time could not be modified.
// *Action: Examine the accompanying error messages and respond accordingly.
40018, 3, "invalid combination of parameters 'timestamp_before', 'timestamp_after' and 'timestamp_duration'"
// *Cause: The parameters 'timestamp_before', 'timestamp_after' and 'timestamp_duration' were all specified as part of the cluster acitivity log query.
// *Action: Retry the cluster activity log query with a valid parameter combination.
40019, 3, "Resize operation for cluster activity log failed because the maximum size or retention time specified was too large. Detailed error: '%s'"
// *Cause: The value specified for the maximum size or retention time of the cluster activity log was too large and could not be accommodated.
// *Action: Specify a lower value for maximum size or retention time.
40020, 1, "The operation will delete all entries in cluster activity log. Rerun with '-f' option."
// *Cause: The operation to shrink the cluster activity log was issued without the '-f' option.
// *Action: If appropriate, reissue the command with the '-f' option.

/
/ crsctl query messages 41001 - 42000. Continued from 4170 - 4178, 6741 - 6760
/
41001, 3, "  crsctl query crs lastactivetimestamp [<host>]"
41002, 3, "  crsctl query crs lastactivetimestamp [<host>]\n     Lists the Last active timestamp of a leaf node.\nwhere\n     Default         Lists the last active timestamp of the local leaf node\n     host            Lists the last active timestamp of the named leaf node"
41003, 1, "unable to get the last active timestamp"
// *Cause: The crsctl query failed because the last active timestamp could not
//         be retrieved. Either the clusterware stack was down, or the
//         requesting user was not root (UNIX) or Administrator (WINDOWS).
// *Action: Bring up the clusterware stack using the command 'crsctl start crs'
//          and retry the query or retry the query as a privileged user.
41004, 1, "Last active timestamp query failed for node %s."
// *Cause: The crsctl query failed to retrieve the last active timestamp for
//         the indicated node.
// *Action: Examine the accompanying error message, address issues reported and
//          retry the query.
41005, 3, "The last active timestamp of node [%s] is [%s]\n"
41006, 1, "Node %s is not a leaf node."
// *Cause: An attempt to list the last active timestamp for the indicated node
//         was rejected because that node was not a leaf node.
// *Action: Rerun the command from a leaf node or specifying a leaf node that
//          is a cluster member or was a cluster member.
41007, 3, "  crsctl get cluster class\n     Get the cluster class"
41008, 3, "Cluster class is '%s'"
41009, 3, "Node '%s' configured role is '%s', but active role is '%s'."
41010, 3, "Node '%s' active role is '%s', but configured role is '%s'."
41011, 3, "Restart Oracle High Availability Services for the new role to take effect."
41012, 3, "insufficient permission to create or delete a member cluster configuration"
// *Cause: An attempt was made to create or delete a member cluster 
//         configuration by a user who was not an Oracle Grid Infrastructure
//         user.
// *Action: Rerun the command as an Oracle Grid Infrastructure user.
41013, 3, "The member cluster configuration must be run on a \"Domain Services Cluster\" only."
// *Cause: An attempt was made to create a member cluster configuration on a
//         cluster which is not a \"Domain Services Cluster\".
// *Action: Rerun the command on a \"Domain Services Cluster\"."
41014, 3, "  crsctl get cluster configuration\n    Displays the  cluster configuration information"
41015, 3, "Name      : %(1)s\nClass     : %(2)s\nType      : %(3)s\n"
41016, 0,   "failure getting the cluster configuration"
// *Cause:  An attempt to get additional configuration information from
//          the Grid Infrastructure Management Respository (GIMR) failed.
//          This is an internal error.
// *Action: Contact Oracle Support Services.
41017, 0,   "permission to retrieve the cluster configuration denied"
// *Cause:  An attempt to retrieve the configuration failed because
//          the stack was down and permission to retrieve the
//          cluster configuration with the stack down was denied.
// *Action: Run the query when the Oracle Clusterware stack is up or
//          as a privileged user such as root (on UNIX) or
//          administrator (on Windows).
41018, 0,   "failure getting the local node number from Cluster Synchronization Services (return code %d)"
// *Cause:  An attempt to execute the command 'crsctl get node role status'
//          failed  because Cluster Synchronization Services (CSS) 
//          was not running.
// *Action: Ensure that the CSS daemon is running on this node, and then retry
//          the operation.
41019, 0,   "the active status role of node '%(1)s' is unknown"
// *Cause:  An attempt to execute the command 'crsctl get node role status'
//          failed for the indicated node  because Cluster Synchronization
//          Services (CSS) was not running.
// *Action: Ensure that CSS daemon is running on the indicated node, and 
//          then retry the operation.


/
/ cluster rename specific messages 42001 - 42100
/
42001, 3, "Brief Usage: crsrename cluster <new_clustername>"
42002, 1, "operation not supported for single-instance high availability configurations"
// *Cause: An attempt was made to execute a command to rename a cluster, 
//         which was not supported in the current single-instance high 
//         availability configuration.
// *Action: None. 
/
42003, 1, "operation only supported for standalone cluster"
// *Cause: An attempt to rename a cluster was rejected because that operation 
//         was only supported for standalone cluster configurations.
// *Action: None. 
42004, 3, "successfully set the cluster name"
42005, 1, "failed to set the cluster name"
// *Cause: There was an internal error while setting the cluster name.
// *Action: Contact Oracle Support Services.
42006, 1, "cluster name is invalid"
// *Cause: An attempt to rename a cluster was rejected because an invalid
//         cluster name was specified.
// *Action: Rerun the command with a valid cluster name. A valid cluster name
//          should be at least one character long but no more than 15 characters
//          in length. The cluster name consists of alphanumeric characters and
//          the hyphen (-) character (a..z,A..Z,0..9,-). It cannot begin or end
//          with the hyphen (-) character.
42007, 1, "operation not supported for clusters where an RHP Server or an RHP Client is configured"
// *Cause: An attempt to rename a cluster was rejected because that operation 
//         was not supported for clusters where an RHP Server or 
//         an RHP Client is configured.
// *Action: None.
42008, 1, "operation not supported for clusters where Quality of Service Management is configured and is in use"
// *Cause: An attempt to rename a cluster was rejected because that operation
//         was not supported for clusters where Quality of Service Management
//         was configured and was in use.
// *Action: None.
