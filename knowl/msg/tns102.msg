/ Copyright (c) 1991, 1996, 1997, 1998, 1999, 2000, 2001 by the Oracle Corporation.  All rights reserved.
/
/
/ $Header: netius.msg 16-may-2006.05:51:20 rsriniv Exp $
/
/
/ NAME
/   netius.msg - NETwork Internal message file - U.S. english version
/
/
/ FUNCTION
/   Internal network error message file, American English version.
/
/
/ NOTES
/       Only internal errors are to be put into this file. External
/       messages are to put into netus.msg.
/
/       This file, along with netus.msg, forms tnsus.msg. As a result, the
/       errors in this file may not overlap with the errors in that file.
/       Otherwise, errors will result when generating tnsus.msb.
/
/       Message text should be limited to a maximum of 76 characters.
/       Messages containing embedded % directives should not overrun
/       the 76 character limit unless they signal unusual errors
/       which do not occur as part of user applications.  For example,
/       startup errors and system-dependent errors can probably get
/       away with longer message text.
/
/
/       '/' at beginning-of-line for comments.
/       '//' at beginning-of-line for *Cause: and *Action: fields.
/
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/////////////////////////// Please maintain this map //////////////////////
/
/ 00000		  Not an error.
// 00001 - 00500   NR  (not reportable to OSN) - do not document
/ 00501 - 01000   NT  (not reportable to OSN) - do not document
/  00540 - 00579  NTZ/SSL  (not reportable to OSN) - do not document
/ 01001 - 02500   NSG (not reportable to OSN) - do not document
/ 02501 - 03500   NA  (not reportable to OSN) - do not document
/ 03501 - 03600   NSPING (not reportable to OSN) - NS ping utility
/ 03601 - 03700   NSUT (not reportable to OSN) - NS trace route utility
/ 04001 - 04200   NFP (not reportable to OSN) - do not document
/ 04201 - 04300   NU  (not reportable to OSN) - do not document
/ 04301 -         Oracle Network Java components (04301 - 06000)
/ 04301 - 04400   Java Trace Assistant
/ 04400 - 04500   Config API
/       .
/ 04600 -         NL Java Net (jsrc/oracle/net/nl)
/       .
/       - 06000   Oracle Network Java components (04301 - 06000)

/       .
/       .
/
/ 12150 - 12285   See net12150.msg
/ 12500 - 12699   See net12500.msg
/////////////////////////// Please maintain this map //////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/
/
/
/ OWNER
/   Network and Management Products - Server Technologies
/
/ MODIFIED
/    rsriniv    05/16/06 - Backport skramas_lsnsec from main 
/    rsriniv    02/04/05 - Added message (1192) for tnslsnr. 
/    skramas    01/11/05 - Add lsnrctl error message for alias name too long 
/    rmallika   01/31/05 -  Fix for bug 4105454 
/    rmallika   01/18/05 - New error message for cman 
/    ppovinec   04/14/04 - More for localOSauth 
/    smckinle   04/13/04 - NTVL .ora parsing/config error messages. 
/    ppovinec   09/30/03 - New listener errors for localOSauth 
/    ppovinec   01/24/03 - Add error msg for incompatible listening endpoints
/    asankrut   01/07/03 - Modified CMAN messages
/    ppovinec   12/05/02 - Listener filtering rules message
/    cozhang    12/04/02 - Add NLS_DO_NOT_TRANSLATE comment.
/    asankrut   10/31/02 - Change Proxy LSNRCTL messages to be generic ones
/    skramas    10/21/02 - Replace CMAN9i messages with those for CMAN10i
/    ppovinec   10/14/02 - Listener nsgr messages
/    rneela     09/09/02 - new block of errors for javanet NL
/    ktarkhan   10/14/02 - Config API errors
/    asankrut   10/11/02 - Added messages for proxy LSNRCTL
/    mclose     10/03/02 - Improving messages
/    ppovinec   08/19/02 - New lsnr message for proxy services
/    cozhang    03/15/02 - Add NSGMETREGLIMIT (1181), reg limit reached.
/    rneela     09/27/01 - add new errors for trcasst.
/    ppovinec   02/19/01 - New lsnrctl serv message.
/    ppovinec   02/08/01 - Net8 --> Oracle Net rename.
/    cozhang    12/13/00 - Remove dbsnmp-related messages
/    ppovinec   10/20/00 - NSGLSN messages for PID.
/    ppovinec   09/05/00 - Add quotes in 1037.
/    ppovinec   07/18/00 - New listener messages for 8.2.
/    ppovinec   06/28/00 - Add msg 1080 for tnslsnr.
/    loramasa   02/17/00 - added message for tnsping
/    ppovinec   07/27/99 - TNSLSNR messages in support of NSGR.
/    sguan      07/22/99 - Changed <cman_name> to be predefined names
/    sguan      07/08/99 - modified cman messages
/    sguan      07/01/99 - Added new cmctl status messages
/    rwessman   06/24/99 - Added Entrust errors
/    rwessman   06/10/99 - Added messages for the SSL NT adapter
/    sguan      06/29/99 - modified message 4099
/    sguan      06/28/99 - added new messages for new 8.1.6 commands
/    sguan      05/28/99 - for new parser
/    ppovinec   02/10/99 - Messages for listener's dynamic endpoints registrati
/    smendiol   02/12/99 - Fixing TrcAsst typo
/    emalasky   10/29/98 - add direct_handoff_listener param
/    emalasky   03/27/98 - add/modify messages for 8.1 services
/    emalasky   03/06/98 - add 1179 - lsnr cannot load instance class
/    skanjila   03/13/98 - Make translation changes for CMan in 805.
/    emalasky            - add lsnrctl services output
/    smendiol   01/22/98 - Adding NU error messages
/    emalasky            - better listener logging
/    tmlee      04/30/97 - executable name changes, new names: cmctl, cmgw, and
/    emalasky   04/15/97 - adding lsnrctl mesgs
/    pmitra     03/28/97 - CLB errors 2401-2500
/    jgraham    03/21/97 - remove reference to CONFIG.ORA
/    rwessman   03/19/97 - Eliminated references to Secure Network Services. It
/    rwessman   03/16/97 - Fixed comment
/    rwessman   03/09/97 - Split from tnsus.msg
/    dhwu       10/24/96 - fix for 356374
/    ygan       10/19/96 - Bug #358488:  Modify message for 12500
/    dlau       10/10/96 - Adding Connection Manager messages
/    dlau       10/07/96 - Add Connection Manager messages.
/    emalasky   09/30/96 -
/    emalasky   09/17/96 -
/    ygan       08/06/96 - Change message for set password for the listener
/    ygan       08/06/96 - Bug 350196
/    mkanaley    02/19/92     Add NSG messages, remove 1040
/
/    sviavant    02/18/92     Creation
/
///////////////////////////////////////////////////////////////////////////
/
00000, 00000, "Not An Error"
// *Cause:  Everything is working as it should.
// *Action: Don't worry: Be happy.
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ 00001 - 00500 NR errors
/
///////////////////////////////////////////////////////////////////////////
/
/ The range 00100 to 00200 should be reserved for the Network Routing
/ Gateway ConTroL program.  The messages will include status messages
/ as well as error messages.
/
/ Start with error messages first.
/
00001, 00000, "INTCTL: error while getting command line from the terminal"
// *Cause: Improper standard input connection from the terminal.
// *Action: Normally not visible to the user. Start the INTCTL program again.
// If error persists, contact Oracle Customer Support.
/
00002, 00000, "INTCTL: error while starting the Interchange"
// *Cause: The Interchange could not be started.
// *Action: Check the Interchange configuration files (INTCHG.ORA, TNSNET.ORA
// and TNSNAV.ORA) for errors and confirm that no other programs are using
// the ADDRESS(es) specified. If error continues, turn on tracing in the
// Interchange components and examine the trace files to determine the
// cause of the problem. Be sure to turn tracing off when the problem has been
// rectified.
/
00003, 00000, "INTCTL: error while sending request to the Interchange"
// *Cause: Improper command sent to the Interchange or the Interchange
// is not responding. Not normally visible to the user.
// *Action: Verify that the command sent to the Interchange is valid.
// Also check that the Interchange is running by using the INTCTL STATUS
// command. If necessary, start the Interchange using the INTCTL START
// command.
/
00004, 00000, "INTCTL: error while starting the Navigator"
// *Cause: The Navigator could not be started.
// *Action: Check to make sure that executables for the Navigator (navgatr)
//  are present in the ORACLE executable directory on
//  your platform. Check the configuration files TNSNET.ORA and TNSNAV.ORA
//  for errors. If error continues, turn on tracing in the Interchange
//  components and examine the trace files to determine the cause of the
//  problem. Be sure to turn tracing off when the problem has been
//  rectified.
/
00005, 00000, "INTCTL: error while sending request to the Navigator"
// *Cause: The Navigator is not responding. Either the Navigator is not
// running or another process is responding.
// *Action: Check that the Navigator is running by using the STATUS command
// of the Interchange Control Utility. Verify that the correct addresses
// are listed in the TNSNAMES.ORA, TNSNET.ORA, and TNSNAV.ORA configuration
// files.
/
00006, 00000, "INTCTL: HOST variable is not defined"
// *Cause: The HOST variable was not set.
// *Action: Set the variable HOST properly and restart the INTCTL program.
/
00007, 00000, "INTCTL: unknown host"
// *Cause: The pointer HOST is set to an unknown hostname.
// *Action: Set the pointer HOST properly and restart INTCTL program.
/
00008, 00000, "INTCTL: could not contact destination Navigator"
// *Cause: Connection could not be properly established to a Navigator.
// This may be because the Navigator specified is not running or the Navigator
// addresses are incorrect.
// *Action: Check that the Navigator is running by using the STATUS
// command of the Interchange Control Utility; if necessary, start the
// Navigator using the START command of the Interchange Control Utility.
// If it is running and the error persists, contact Oracle Customer
// Support.
/
00009, 00000, "INTCTL: could not contact destination Connection Manager"
// *Cause: Connection could not be properly established to a Connection
// Manager.  This may be because the Connection Manager (Interchange)
// specified is not running or the Connection Manager addresses are incorrect.
// *Action: Make sure the Connection Manager is running by using the STATUS
// command of the Interchange Control Utility; if necessary, start the
// Connection Manager using the START command of the Interchange Control
// Utility. If it is running and the error persists, contact Oracle Customer
// Support.
/
00010, 00000, "Error while flushing NS context"
// *Cause: Internal NS error; connection may be lost.
// *Action: Make sure the connection is properly established.  If the
// error persists, then contact Oracle Customer Support.
/
00011, 00000, "INTCTL: error while starting the Connection Manager"
// *Cause: The Connection Manager could not be started.
// *Action: Assure that the executable can be found in the standard Oracle
// executable area. Check the configuration file INTCHG.ORA for errors and
// confirm that no other process is using the ADDRESS(es) for this
// Connection Manager as specified in TNSNET.ORA.
// Tracing can also be turned on in the Connection Manager and detailed
// information about the reason for the error determined. Consult the
// MultiProtocol Interchange Administrator's Guide and Chapter 2 of this
// manual for how to turn on tracing.
/
00012, 00000, "INTCTL: error while processing Connection Manager request"
// *Cause: An improper command was sent to the Connection Manager or it is not
// responding. Not normally visible to the user.
// *Action: Verify that the correct addresses are listed in the
// TNSNAMES.ORA, TNSNET.ORA, and TNSNAV.ORA configuration files.  Also check
// that the Connection Manager is running by using the STATUS command of
// the Interchange Control Utility. If the error persists, contact
// Oracle Customer Support.
/
00013, 00000, "INTCTL: error while performing NS disconnect command"
// *Cause: Internal NS error. Error in closing down connections.
// *Action: Make sure the networking protocol being used is properly
// installed on the machine.  If  the error persists contact
// Oracle Customer Support.
/
00014, 00000, "INTCTL: error while opening terminal input channel"
// *Cause: Could not open standard terminal input. Internal error.
// *Action: Normally not visible to the user.  Restart the INTCTL program.
// If error persists, contact Oracle Customer Support.
/
00015, 00000, "INTCTL: error while closing terminal input channel"
// *Cause: Could not close terminal input channel. Internal error.
// *Action: Normally not visible to the user.  Restart the INTCTL program.
// If error persists, contact Oracle Customer Support.
/
00016, 00000, "INTCTL: error while performing NS send command"
// *Cause: Internal NS error.  Connection may be lost.
// *Action: If the error persists contact Oracle Customer Support.
/
00017, 00000, "INTCTL: error while performing NS receive command"
// *Cause: Internal NS error.  Connection may be lost.
// *Action: If the error persists contact Oracle Customer Support.
/
00018, 00000, "INTCTL: TNS_ADMIN not defined"
// *Cause: The TNS_ADMIN pointer is improperly set.
// *Action: No action necessary; TNS_ADMIN need only be set if you want to
// use a different network environment.
/
00019, 00000, "INTCTL: error initializing the national language interface"
// *Cause: The message file could not be found.
// *Action: Make sure that the ORACLE environment is set and that the message
// file is in the correct place.
/
00020, 00000, "INTCTL: missing NAVIGATOR_DATA in TNSNAV.ORA"
// *Cause: TNSNAV.ORA does not contain the NAVIGATOR_DATA component.
// *Action: Define the ADDRESS(es) for the Navigator, then restart the INTCTL
// program.
/
00021, 00000, "INTCTL: missing INTERCHANGE_DATA in INTCHG.ORA"
// *Cause: INTCHG.ORA does not contain an INTERCHANGE_DATA component.
// *Action: Define the correct data for the Connection Manager, then restart
// the INTCTL program.
/
00022, 00000, "INTCTL: missing CMANAGER_NAME in INTCHG.ORA"
// *Cause: INTCHG.ORA does not contain a CMANAGER_NAME component.
// *Action: Define the correct name for the CMANAGER_NAME, then restart
// the INTCTL program. 
/
00023, 00000, "INTCTL: missing ADDRESS(es) in config files"
// *Cause: Configuration files do not contain an ADDRESS/ADDRESS_LIST
// component.
// *Action: Define the Connection Manager ADDRESS(es) in the TNSNET.ORA
// file and check the Navigator ADDRESS(es) in the TNSNAV.ORA file,
// then restart the INTCTL program.
/
00024, 00000, "INTCTL: Unable to contact Navigator to obtain Connection Manager address"
// *Cause: The Navigator is not running.
// *Action: Verify that the Navigator is running by doing a status
// request on the Navigator (use the Interchange Control Utility command
// STATUS). If necessaary, start the Navigator using the Interchange
// Control Utility. Verify that the network is properly configured;
// if the error persists, contact Worldwide Customer Support.
/
00025, 00000, "INTCTL: The ORACLE environment is not set up correctly"
// *Cause: The ORACLE environment is incorrectly set up.
// *Action: Refer to the Oracle operating system specific documentation for
// your platform for information on how the ORACLE environment should be set.
// Correct it and rerun INTCTL. Make sure the ORACLE environment includes
// the correct directories.
/
00026, 00000, "INTCTL: TNS_ADMIN directory set, and is being used"
// *Cause: The TNS_ADMIN environment variable is set properly.  INTCTL will
// use the TNS_ADMIN directory.  This is only an informative message.  If
// you do not want it to be used, and want the default directory to be used
// instead, then unset TNS_ADMIN and reexecute.
// *Action: None.
/
00027, 00000, "INTCTL: Could not resolve Navigator's name/address"
// *Cause: The Navigator's name to address definition is missing.
// *Action: Check TNSNAMES.ORA file and make sure to include a definition for
// the name specified.
/
00028, 00000, "INTCTL: Could not resolve Connection Manager's name/address"
// *Cause: The Connection Manager's name does not have a definition that the
// Navigator knows about, nor is the name/address available in the
// TNSNAMES.ORA file. The name may also be incorrect in the INTCHG.ORA
// file.
// *Action: Verify that the Connection Manager's name is in the TNSNET.ORA
// file read by the Navigator or in the TNSNAMES.ORA file. Be sure that
// INTCHG.ORA is correct.
/
00031, 00000, "INTCTL: internal NT error"
// *Cause: Problem interfacing to the protocol adapters installed.
// *Action: Normally not visible to the user. Try starting INTCTL
// again.  If the error persists, check the product installation. If it is
// correct, contact Oracle Customer Support.
/
00032, 00000, "INTCTL: internal NS error"
// *Cause: Problem interfacing with TNS.
// *Action: Normally not visible to the user. Try starting INTCTL
// again.  If the error persists, check the product installation. If it is
// correct, contact Oracle Customer Support.
/
00033, 00000, "INTCTL: internal NL error"
// *Cause: Problem with internal TNS module NL.
// *Action: Normally not visible to the user. Try starting INTCTL
// again.  If the error persists, check the product installation. If it is
// correct, contact Oracle Customer Support.
/
00034, 00000, "INTCTL: internal NR error"
// *Cause: Problem with internal Interchange routines.
// *Action: Normally not visible to the user. Try starting INTCTL
// again.  If the error persists, check the product installation. If it is
// correct, contact Oracle Customer Support.
/
00035, 00000, "INTCTL: error while constructing full file name"
// *Cause: Problem while constructing the full path for a file name because
// the path name to the file or the environment variables are
// incorrect. Files looked up include TNSNAMES.ORA, TNSNAV.ORA, INTCHG.ORA
// and the error files for the Navigator and Connection Manager.
// *Action: Check that all environment variables are defined correctly
// and that all configuration files exist in their correct places.
/
00036, 00000, "INTCTL: error reading from Navigator or Connection Manager error files"
// *Cause: Problem while reading from Navigator or Connection Manager error
// files generated by the Navigator or Connection Manager when they fail
// to start.
// *Action: Check that a standard Network Error directory exists and that all
// privileges on the directory are appropriate.
/
00037, 00000, "INTCTL: error opening Navigator or Connection Manager error files"
// *Cause: Failed to open Navigator or Connection Manager error files when
// they have failed to start.
// *Action: Check that a Network Error directory exists and that all
// privileges on the directory are appropriate.
/
00038, 00000, "INTCTL: Poorly formed address or command string"
// *Cause: An unacceptable string was encountered while attempting
// to send a message to either the Navigator or Connection Manager.
// The addresses provided for either the Navigator or Connection Manager
// may be incorrectly constructed.
// *Action: Check all address strings in configuration files (TNSNAMES.ORA,
// TNSNAV.ORA or TNSNET.ORA) and assure that they are properly formed.
// Regenerate the files, if possible. If
// all is correct, please contact Worldwide Customer Support.
/
00039, 00000, "INTCTL: error while spawning a process"
// *Cause: An error was encountered while spawning a process due to an
// internal operating system dependent problem. Machine resources may be
// limited.
// *Action: Retry command. Check permissions on Interchange
// executables and the current setting of the search path. If necessary,
// terminate other applications to free up machine resources. If the error
// persists, contact Oracle Customer Support.
/
00040, 00000, "INTCTL: failed to initialize trace context-  Continuing anyway"
// *Cause: Problem while opening specified trace file because of errors in
// INTCHG.ORA or because the user has incorrect privileges, or the file does
// not exist.
// *Action: Check the privileges on the configuration files and ensure that
// all of them exist in their proper locations.
/
00041, 00000, "INTCTL: Navigator already running.  Start operation cancelled"
// *Cause: There is a Navigator already running and listening on the same
// addresses.
// *Action: None; the Navigator is already running.
/
00042, 00000, "INTCTL: CMANAGER already running.  Start operation cancelled"
// *Cause: There is a Connection Manager already running and listening on
//  the same addresses.
// *Action: None; the Connection Manager is already running.
/
00043, 00000, "The CMANAGER has active connections, do you still want to stop it (y/n)?"
// *Cause: The CMANAGER that is being stopped has active connections going
//  through.  This is the confirmation message.
// *Action: Respond by pressing y or n. Answering y will cause the active
// database connection to be dropped; this is not generally recommended.
/
00044, 00000, "INTCTL: You must have an INTCHG.ORA file to contact the Connection Manager"
// *Cause: There was an attempt to contact a default Connection Manager
// (Interchange) where there was no INTCHG.ORA present in the correct
// directory.
// *Action: Create an INTCHG.ORA file.
// Make sure it is placed in the correct directory and includes the correct
// name for the Connection Manager you wish to contact.
/
00045, 00000, "INTCTL: Could not contact the Navigator on address"
// *Cause: There was an attempt to contact a Navigator on a specific address
//  which is not responding.
// *Action: Check the TNSNAV.ORA file for that address.  Or check that the
//  Navigator is actually listening on that address.
/
00046, 00000, "INTCTL: Could not contact the CMANAGER on address"
// *Cause: There was an attempt to contact a CMANAGER on a specific address
//  which is not responding.
// *Action: Verify that the TNSNET.ORA file contains that address.  Also check
// that the CMANAGER is actually listening on that address by using the INTCTL
// STATUS command. If necessary, start the Connection Manager using the INTCTL
// START command.
/
00060, 00000, "INTCTL: Bad command: only the STATUS command can be used on remote Interchanges"
// *Cause: The user entered a command that does not exist, or the user
// tried to make a request other than STATUS to a remote Interchange.
// *Action:  Check the MultiProtocol Interchange Administrator's Guide for
// a list of INTCTL commands or type HELP for a list of valid commands.
/
00061, 00000, "INTCTL: Bad command or syntax error: You must specify a trace level"
// *Cause:  The user did not specify a trace level.
// *Action:  Specify a trace level and retry command.
/
00062, 00000, "INTCTL: Bad command or syntax error: For help type help/h/?"
// *Cause:  The user entered an invalid command.
// *Action:  Check the MultiProtocol Interchange Administrator's Guide or type
// HELP for a list of valid commands.
/
00063, 00000, "INTCTL: Failed to allocate memory for buffers"
// *Cause:  INTCTL was unable to allocate memory for internal buffers.
// *Action:  Check the amount of available memory on your machine to ensure
//  that there is enough memory to run this executable. If necessary, free up
// memory by running fewer programs, then try again.
/
00064, 00000, "INTCTL: Failed to find CMANAGER_NAME in INTCHG.ORA"
// *Cause:  INTCTL was unable to find the CMANAGER_NAME parameter in INTCHG.ORA.
// *Action:  Check that the INTCHG.ORA file is properly constructed.
/
00065, 00000, "INTCTL: Command cannot be executed remotely"
// *Cause:  A command other than status and version has been attempted
// remotely.
// *Action:  If you desire execute any command other than status and version,
//  you must run intctl on the interchange machine.
/
/ The range 00070 to 00099 will be reserved for the help messages used by
/ INTCTL program
/
00070, 00000, "INTCTL usage: [intctl] <command> <process_name> [argument]\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00071, 00000, "  where <command> is one of following: \n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00072, 00000, "           * start - start up process_name\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00073, 00000, "           * stop/abort - stop the process_name\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00074, 00000, "           * status - get statistics from the process_name\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00075, 00000, "                    NOTE:  the user may get the status info of a remote\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00076, 00000, "                           component by specifying the component name in\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00077, 00000, "                            the argument field\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00078, 00000, "           * log_on - ask process_name to turn logging on\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00079, 00000, "           * log_off - ask process_name to turn logging off\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00080, 00000, "           * force_log - ask process_name to dump its state\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00081, 00000, "           * trace_on - ask process name to turn tracing on\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00082, 00000, "                      NOTE:  the user MUST specify a trace level\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00083, 00000, "                             (USER or ADMIN) in the argument field\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00084, 00000, "           * trace_off - ask process name to turn tracing off\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00085, 00000, "           * reread - ask the process name to reread parameter files\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00086, 00000, "           * reload - ask the Navigator to reload TNSNET.ORA\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00087, 00000, "           * version - ask the process name to display its version number\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00088, 00000, "           * exit  - quit the Interchange controller\n\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00089, 00000, "         process_name is one of Interchange, CMANAGER, or Navigator\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00090, 00000, "           * Interchange - will ask the Interchange\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00091, 00000, "           * Navigator (or navgatr) - will ask the Navigator only\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00092, 00000, "           * CMANAGER (or intlsnr) - will ask the Cmanager only\n\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00093, 00000, "         argument is only supplied to either status or trace_on\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00094, 00000, "           * to status - argument is considered the remote process_name\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
00095, 00000, "           * to trace_on - argument is considered the trace level\n\n"
// *Cause:  Help message displayed by INTCTL.
// *Action:  None.
/
/
/
/ The range 00100 to 00400 should be reserved for the Multiprotocol Interchange
/ error messages and user visible messages
/
/ Error messages for Interchange start at 100
/ User visible messages start at 200
/
00100, 00000, "Unable to allocate memory"
// *Cause: Out of memory on the machine.
// *Action: Add more memory or run fewer processes.
/
00101, 00000, "File operation error"
// *Cause: Error in accessing reading or writing a particular file.
// *Action: Check existence of or operating system access to the log and trace
// file locations.
/
00102, 00000, "Keyword-Value binding operation error"
// *Cause: Not normally visible to the user. May indicate a shortage of memory.
// *Action: If error persists contact Oracle Customer Support.
/
00103, 00000, "Parameter file load error"
// *Cause: Parameter file process failed.
// *Action: Check to make sure that all parameter files necessary for the
// Interchange are present (TNSNAV.ORA, TNSNET.ORA and INTCHG.ORA). 
// If these files are present and properly configured, turn on tracing and 
// repeat the operation. Turn off tracing when the trace is complete. Look 
// in the trace file for errors in the parameter loading process. 
// If error persists contact Oracle Customer Support. 
/
00104, 00000, "Data stream open/access error"
// *Cause: Unable to open or access data stream for either log or trace files
//         for the Interchange.
// *Action: Check read/write permissions on Oracle files and directories.
/
00105, 00000, "Could not initialize tracing"
// *Cause: The INTCHG.ORA file is improperly configured. Verify the trace
// parameters specified.
// *Action: If error persists contact Oracle Customer Support.
/
00106, 00000, "Failed to open log file"
// *Cause: Unable to access or obtain write permission to create log file.
// *Action: Check existence of or access to log file directory.
/
00107, 00000, "Unable to initialize TNS global data"
// *Cause: Not normally visible to the user.
// *Action: If error persists contact Oracle Customer Support.
/
00108, 00000, "TNS_ADMIN not defined"
// *Cause: TNS_ADMIN pointer is not set.
// *Action: Set the TNS_ADMIN pointer before running application
/
00109, 00000, "Message could not be printed; not enough memory"
// *Cause: Printing of message failed due to lack of memory. Not normally
// visible to user.
// *Action: Increase the resources on your machine. If error persists contact
// Oracle Customer Support.
/
00110, 00000, "Could not initialize network from file TNSNET.ORA"
// *Cause: Poorly formed network information in network file.
// *Action: Fix network configuration data to assure that at least one
// Interchange is defined in TNSNET.ORA.
/
00111, 00000, "Failed to get configuration data from file"
// *Cause: Poorly formed configuration information in network files TNSNET.ORA
// or TNSNAV.ORA.
// *Action: Check TNSNET.ORA and TNSNAV.ORA and confirm that they are correct.
/
00112, 00000, "Failed to find configuration file name"
// *Cause: Name specified for configuration file was incorrect.
// *Action: Check for presence of the configuration file.
/
00113, 00000, "Failed to open error log file"
// *Cause: Could not open log file during startup of Navigator or
// Connection Manager due to read or write permission problems or non-existent
// error directory.
// *Action: Create the standard error directory or assure that if one
// is present the Interchange executables can write to it.
/
00114, 00000, "Internal error- Allocation of addresses not performed"
// *Cause: Internal error. Should not normally occur.
// *Action: Contact Oracle Customer Support.
/
00115, 00000, "Could not allocate pump global buffers"
// *Cause: Not enough memory to allocate pump buffers.
// *Action: Decrease the number of PUMP_BUFFERS in INTCHG.ORA.
/
00116, 00000, "Pump failed during initial bequeath"
// *Cause: Error in assigning connection to a new pump. This error may be 
// caused by insufficient machine resources.
// *Action: Attempt the connection again. The pump should recover from such
// a failure. If machine resources appear to be the problem, add more resources // or shut down some active applications. If problem persists, contact
// Oracle Customer Support.
/
00117, 00000, "Internal error- No data passed through pump"
// *Cause: Internal error. Data expected has not arrived yet.
// *Action: If error persists, contact Oracle Customer Support.
/
00119, 00000, "Missing PUMP_CONNECTIONS in INTCHG.ORA"
// *Cause: No PUMP_CONNECTIONS parameter specified in INTCHG.ORA.
// *Action: Add PUMP_CONNECTIONS parameter to INTCHG.ORA.
/
00120, 00000, "Missing PUMPS in INTCHG.ORA"
// *Cause: No PUMPS parameter specified.
// *Action: Add an appropriate number of PUMPS to INTCHG.ORA.
/
00121, 00000, "Missing CMANAGER_NAME in INTCHG.ORA"
// *Cause: No CMANAGER_NAME parameter specified.
// *Action: Define the CMANAGER_NAME parameter in INTCHG.ORA; it must
// match the CMANAGER_NAME parameter used in TNSNET.ORA for that
// Interchange.
/
00122, 00000, "Missing ADDRESS(es) in TNSNET.ORA file"
// *Cause: No ADDRESS or ADDRESS_LIST parameter specified in TNSNET.ORA.
// *Action: Define a valid set of ADDRESSes for the Connection Manager in
// the TNSNET.ORA file.
/
00123, 00000, "Unable to perform a listen on configured ADDRESS(es)"
// *Cause: Another process is already listening on this address or the
// ADDRESS is incorrectly defined.
// *Action: Check the ADDRESS(es) defined in TNSNET.ORA (for the Connection
//  Manager) for errors. Verify that another program is not using them.
/
00124, 00000, "Internal error - Unable to create empty address"
// *Cause: - Internal error. Should not normally occur.
// *Action: If problem persists contact Oracle Customer Support.
/
00125, 00000, "Failed to get number of Interchanges in TNSNET.ORA"
// *Cause: Error in the TNSNET.ORA file.
// *Action: Check the contents of TNSNET.ORA and eliminate errors. Regenerate
// the configuration files.
/
00126, 00000, "Missing Connection Manager name and address in TNSNET.ORA"
// *Cause: The Interchange name specified in INTCHG.ORA is not defined in
// the TNSNET.ORA file.
// *Action: Define one Connection Manager name and set of addresses for
// each Interchange in the network.  Regenerate the configuration files.
/
00127, 00000, "Missing Connection Manager name in TNSNET.ORA"
// *Cause: One or more Connection Manager names are missing.
// *Action: Ensure that each Connection Manager name is defined in
// TNSNET.ORA. Regenerate TNSNET.ORA.
/
00128, 00000, "Missing COMMUNITY in TNSNET.ORA"
// *Cause: One or more ADDRESSes does not have a COMMUNITY assigned.
// *Action: Ensure that all addresses have a COMMUNITY defined in TNSNET.ORA.
/
00129, 00000, "Internal error - Failed to create new community"
// *Cause: Internal Error. Should not normally occur. There may be a
// resource limitation problem on the machine.
// *Action: Stop and restart Interchange. If possible, make more memory
// available on the machine. If problem persists, contact Oracle
// Customer Support.
/
00130, 00000, "Failed to create Interchange's internal address"
// *Cause: There is an error in one of the addresses listed in TNSNET.ORA.
// *Action: Check the file for errors in defining Interchanges.
/
00131, 00000, "Missing COMMUNITY in COMMUNITY_COST_LIST in TNSNET.ORA"
// *Cause: A COMMUNITY keyword-value pair is missing within the
// COMMUNITY_COST_LIST in TNSNET.ORA.
// *Action: Define the communities with a COMMUNITY name and associated COST
// in COMMUNITY_COST_LIST.
/
00132, 00000, "COST value must be an integer greater than 0"
// *Cause: A community has been defined in TNSNET.ORA with a COST of 0.
// *Action: Assign an alternate value that is greater than 0.
/
00133, 00000, "Missing LOCAL_COMMUNITIES field in TNSNAV.ORA"
// *Cause: Improperly configured TNSNAV.ORA file.
// *Action: Define the LOCAL_COMMUNITIES fields correctly in TNSNAV.ORA.
/
00134, 00000, "Missing COMMUNITY component in addresses for the Navigator in TNSNAV.ORA"
// *Cause: The addresses specified for the Navigator have no COMMUNITY name.
// *Action: Ensure that all addresses in the NAVIGATOR_ADDRESSES field have
// a COMMUNITY entry in the TNSNAV.ORA file.
/
00135, 00000, "Missing TNS error message file"
// *Cause: No error message file present.
// *Action: Ensure that the ORACLE environment is correctly set for your
// platform and that there is a message directory that contains the correct
// error message file.
/
00136, 00000, "Did not register product/facility for TNS error message"
// *Cause: Error message file error.
// *Action: Ensure that the ORACLE environment is correctly set for your
// platform and that there is a message directory that contains the correct
// error message file.
/
00137, 00000, "Failed to get TNS error message file entry"
// *Cause: No TNS error message file present.
// *Action: Ensure that the ORACLE environment is correctly set for your
// platform and that there is a message directory that contains the correct
// error message file.
/
00138, 00000, "Failed to find ORACLE executable directory"
// *Cause: The ORACLE environment is not correctly set.
// *Action: Ensure that the ORACLE environment is correctly set and the
// error messages file is in the correct place.
/
00139, 00000, "Internal - Data passed from the Interchange listener is poorly formed"
// *Cause: Internal error in Interchange.
// *Action: Check that you are using compatible components of the Interchange
// product, using the INTCTL VERSION command. If problem persists call
// Oracle Customer Support.
/
00140, 00000, "Interchange specified was not found in network tables"
// *Cause: Could not find the Interchange specified in a control request.
// *Action: Check that the Interchange specified is indeed in TNSNET.ORA.
/
00141, 00000, "Failed to get file stream information"
// *Cause: Error in the file stream package.
// *Action: None.
/
00142, 00000, "Community mismatch in TNSNAV.ORA"
// *Cause: The communities in the LOCAL_COMMUNITIES entry in TNSNAV.ORA do
//  not correspond with all the communities in the NAVIGATOR_ADDRESSES
//  entry.
// *Action: Assure that all communities in the NAVIGATOR_ADDRESSES correspond
//  to those in the LOCAL_COMMUNITIES component.
/
00143, 00000, "Illegal PREFERRED_CMANAGERS entry in TNSNAV.ORA"
// *Cause: PREFERRED_CMANAGERS entry in the TNSNAV.ORA used by the Connection
// Manager. There should only be a PREFERRED_NAVIGATORS entry in the
// TNSNAV.ORA on an Interchange.
// *Action: Remove the PREFERRED_CMANAGERS entry from TNSNAV.ORA and assure
// that either no PREFERRED_NAVIGATORS entry is present or that it
// is correct.
/
00144, 00000, "PUMP_CONNECTIONS value in INTCHG.ORA is too large."
// *Cause: The number of PUMP_CONNECTIONS specified in INTCHG.ORA is too large
// to be supported on this platform.
// *Action: Consult the Oracle operating system specific manual for the maximum
//  value for the number of PUMP_CONNECTIONS.
/
00145, 00000, "PUMPS value in INTCHG.ORA is too large."
// *Cause: The number of PUMPS specified in INTCHG.ORA is too large 
// to be supported on this platform.
// *Action: Consult the Oracle operating system specific manual for the
//  maximum value for the number of PUMPS.
/
00146, 00000, "Internal-- Retry data request withing pump."
// *Cause: The data space provided in order to receive data from the pump is
// to small.
// *Action:  Operation must be retried with a larger buffer.
/
00147, 00000, "Failed to start a pre-spawned pump."
// *Cause: The Connection Manager was unable to start a pump during startup.
// *Action:  Check all configuration parameters and assure that they are 
//  correct. Turn on tracing to determine the area that the failure ocurred in.
/
/ User Visible messages, starting at 200
/ Log and status messages.
/
00200, 00000, "Unable to do nsanswer on context\nresult=%s\n"
// *Cause: Requester of service may have aborted or options negotiation failed.
// *Action: Try making the connection again. If the problem persists call
// Oracle Customer Support.
/
00201, 00000, "Unable to read answer connection data :%s:\n"
// *Cause: Improperly formed connect data sent to the Interchange listener.
// *Action: If problem persists, check the application using the
// Interchange (it may be closing down or crashing). Call Oracle Customer
// Support if the problem cannot be located.
/
00202, 00000, "Failure in redirecting call : \nOriginal to %s\n\t Redirect to %s\n"
// *Cause: Internal - error could not redirect call to a pump or other
// Interchange listener. The cause may be insufficient network or machine
// resources.
// *Action: Add resources or close some running applications in order to
// free up resources. If error persists, call Oracle Customer Support.
/
00203, 00000, "Unable to start tracing in intlsnr\n"
// *Cause: Failure in setting up tracing for Interchange listener.
// *Action: Check file permissions in Network trace directory also check
// to make sure that if trace file names and directories are specified in
// INTCHG.ORA, they are correct.
/
00204, 00000, "Started tracing in intlsnr\n"
// *Cause: Internal message- Successfully started tracing information.
// *Action: None.
/
00205, 00000, "Turning off tracing in intlsnr\n"
// *Cause: Internal message - Turned off tracing in the Interchange listener.
// *Action: None
/
00206, 00000, "\n\nStatus Information for Interchange %s:\n"
// *Cause: Message sent back by Interchange as header for status request.
// *Action: None
/
00207, 00000, "\tUptime                        : %lu days %lu hr. %lu min. %lu sec\n"
// *Cause: Part of status request.
// *Action: None
/
00208, 00000, "\tLogging                       : %s\n"
// *Cause: Part of status request.
// *Action: None
/
00209, 00000, "\tTracing                       : %s\n"
// *Cause: Part of status request Interchange.
// *Action: None
/
00210, 00000, "\tTotal Pumps Available         : %u\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00211, 00000, "\tTotal Active Pumps            : %u\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00212, 00000, "\tTotal Pumps Started           : %u\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00213, 00000, "\tAvailable Connections         : %lu\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00214, 00000, "\tTotal Connections in Use      : %lu\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00215, 00000, "\tTotal Successful Connections  : %lu\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00216, 00000, "\tTotal Failed Connections      : %lu\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00217, 00000, "\tTotal Bytes of Data           : %lu\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00218, 00000, "\tCurrent Bytes/Sec.            : %.2f\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00219, 00000, "\tPump Strategy                 : %s\n"
// *Cause: Part of status request.
// *Action: None
/
00220, 00000, "\tPump Breakdown\n\t--------------\n"
// *Cause: Part of status request.
// *Action: None
/
00221, 00000, "\tPump          Connections        Total Data          Bytes/Second\n"
// *Cause: Part of status request.
// *Action: None
/
00222, 00000, "\t-------------------------------------------------------------------\n"
// *Cause: Part of status request.
// *Action: None
/
00223, 00000, "\t%5u%12u%26lu%22.2f\n"
// *Cause: Part of status request.
// *Action: None
/
00224, 00000, "No more connections available\n"
// *Cause: More connections were made to the Interchange than are configured
// in INTCHG.ORA.
// *Action: Wait until the Interchange is not as busy or change the number of
// connections allowed in INTCHG.ORA and restart the Interchange.
/
00225, 00000, "Unable to bequeath connection to pump\n"
// *Cause: Unable to start a pump because either the executable cannot be
// found or too many  processes aare currently running on a particular machine.
// *Action: Reduce the number of processes on the machine or increase the
// resources on the machine.
/
00226, 00000, "Unable to contact pump %d to send broadcast message %s\n"
// *Cause: Could not call a particular pump.
// *Action: None, but if the problem persists call Oracle Customer Support.
/
00227, 00000, "Unable to contact pump; Connection Manager declared pump dead\n"
// *Cause: A pump became an orphaned process. A protocol adapter is not
// working properly or machine network resources are being over used.
// *Action: This error is not immediately fatal; the orphaned pump may
// continue to function. Restart the Interchange when convenient. If the
// problem persists, call Oracle Customer Support.
/
00228, 00000, "Failure in finding pump data\n"
// *Cause: Internal problem with data passed back from pump.
// *Action: None.
/
00229, 00000, "Error in call: unable to deliver message\n:%s:\n%s\n%s\n%s\n"
// *Cause: Destination for call is unavailable.
// *Action: None.
/
00230, 00000, "Cannot start new pump process:\n%s\n%s\nProtocol Adapter errors:%u"
// *Cause: Unable to create a new process; possibly there are too many
// processes on the machine.
// *Action: Free machine resources by exiting other applications on the
// Interchange machine. If the problem continues you may need more memory
// on the machine. If you believe there are sufficient resources on the
// machine but the problem persists, contact Oracle Customer Support.
/
00231, 00000, "Pump is alive\n"
// *Cause: Pump log message sent to Interchange listener.
// *Action: None.
/
00232, 00000, "Unable to setup connection\n"
// *Cause: Error log message sent from pump to indicate failure in initiating
// connection because of errors in the call string: network problem or
// resource limitations.
// *Action: None.
/
00233, 00000, "Interchange failed to make contact with destination with errors:\n%s\n%s\n%s\n"
// *Cause: Pump call to destination failed.
// *Action: Check destination.
/
00234, 00000, "Connect data for failed call:\nCALL DATA =\n%s\nRECEIVE DATA = :%s:\n"
// *Cause: Connect data supplied for error 00233.
// *Action: None
/
00235, 00000, "Aborting connection:\nProtocol Apapter errors:\n%s;%u,%u\n%s;%u,%u\n"
// *Cause: Pump aborting connection because connection has been up too long,
//         or some other network error on the connection.
// *Action: None.
/
00236, 00000, "Failed to initialize tracing\n"
// *Cause: Pump failed to initialize tracing.
// *Action: Check that INTCHG.ORA is properly configured.
/
00237, 00000, "Failed to refuse connection\n"
// *Cause: Connection may have aborted before error took place in Pump.
// *Action: None.
/
00238, 00000, "Pump %d @: %s: "
// *Cause: Prepended message to all pump log messages.
// *Action: None.
/
00239, 00000, "Connection Manager has been stopped"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00240, 00000, "Connection Manager: Logging is now ON"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00241, 00000, "Connection Manager: Logging is now OFF"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00242, 00000, "Connection Manager: Tracing is now ON"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00243, 00000, "Connection Manager: Tracing is now OFF"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00244, 00000, "Connection Manager: Request Failed"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00245, 00000, "Connection Manager: Failed to open log file"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00246, 00000, "Connection Manager: Failed to start tracing"
// *Cause: Message sent back to control program from Interchange.
// *Action: None.
/
00247, 00000, "Unable to allocate memory for configuration data from TNSNET.ORA file"
// *Cause: Navigator failed to allocate enough memory for TNSNET.ORA
//  configuration file.
// *Action: Increase machine resources available for running the
// Interchange or remove some other running applications from the machine.
/
00248, 00000, "Unable to get information from file :%s:\nExiting with NR error:%d\n"
// *Cause: TNSNAV.ORA poorly configured or addresses provided are already being
// used by another application.
// *Action: Check the syntax of the TNSNAV.ORA file; if necessary, assign
// new addresses.
/
00249, 00000, "Unable to read network configuration data from file %s\n with error:\n %s\n"
// *Cause: Network configuration file TNSNET.ORA is missing or poorly
//         configured.
// *Action: Check to make sure that TNSNET.ORA is properly configured.
/
00250, 00000, "Navigator has been started\n"
// *Cause: Message to log file on Navigator startup.
// *Action: None.
/
00251, 00000, "Failure in nstest: \n"
// *Cause: NS test operation failed due to internal error.
// *Action: If the problem persists there may be a network problem or
// resource limitations on the machine. If these do not seem to be causing
// the problem, call Oracle Customer Support.
/
00252, 00000, "Unable to handle route request:\n%s\n"
// *Cause: Command requested did not exist.
// *Action: None.
/
00253, 00000, "Error in reading network configuration data from file %s\n with error\n%s\n"
// *Cause: TNSNET.ORA is poorly configured or nonexistent.
// *Action: Check to make sure that TNSNET.ORA is properly configured.
/
00254, 00000, "Navigator has been stopped\n"
// *Cause: Message sent to Interchange control program by Navigator confirming
//         it has been stopped.
// *Action: None.
/
00255, 00000, "Closing down log, stopping Navigator\n"
// *Cause: Log message when Navigator is stopped.
// *Action: None.
/
00256, 00000, "Status of Navigator:\n"
// *Cause: Navigator status message component
// *Action: None.
/
00257, 00000, "\tNumber of Successful Requests : %lu\n"
// *Cause: Navigator status message component
// *Action: None.
/
00258, 00000, "\tNumber of Failed Requests     : %lu\n"
// *Cause: Navigator status message component
// *Action: None.
/
00259, 00000, "\tDisabled Interchange list:\n\t\n"
// *Cause: Navigator status message component
// *Action: None.
/
00260, 00000, "\t-------------------------------------------------------------------\n"
// *Cause: Navigator status message component
// *Action: None.
/
00261, 00000, "\tInterchange Name     Community Link     Down Time Remaining (secs) \n"
// *Cause: Navigator status message component
// *Action: None.
/
00262, 00000, "%20s%20s%30d\n"
// *Cause: Navigator status message component
// *Action: None.
/
00263, 00000, "Navigator: Request Failed"
// *Cause: Response from Navigator when a particular request failed.
// *Action: None.
/
00264, 00000, "Navigator: Failed to reload configuration data"
// *Cause: Message sent to the Interchange control program when reload of
//         network configuration failed. TNSNET.ORA Poorly configured or
//         missing.
// *Action: None.
/
00265, 00000, "Navigator: Reloaded network configuration data"
// *Cause: Message sent to Interchange control program when reload of network
//         is successful.
// *Action: None.
/
00266, 00000, "Navigator: Unknown Request"
// *Cause: Request was made to Navigator that it knows nothing about.
// *Action: None.
/
00267, 00000, "Navigator: Internal Error"
// *Cause: Generated when a request was made to the Navigator it knows nothing
//         about.
// *Action: None.
/
00268, 00000, "ON"
// *Cause: On component of message.
// *Action: None.
/
00269, 00000, "OFF"
// *Cause: Off component of message.
// *Action: None.
/
00270, 00000, "%s: Terminal Error\n%s\n"
// *Cause: Message put out in error file of executable when it fails to start.
// *Action: None.
/
00271, 00000, "Connection Manager"
// *Cause: Name of the Connection Manager.
// *Action: None.
/
00272, 00000, "Navigator"
// *Cause: Name for the Navigator.
// *Action: None.
/
00273, 00000, "Navigator: Logging is now ON"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00274, 00000, "Navigator: Logging is now OFF"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00275, 00000, "Navigator: Tracing is now ON"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00276, 00000, "Navigator: Tracing is now OFF"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00277, 00000, "Navigator: Request Failed"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00278, 00000, "Navigator: Failed to Open Log file"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00279, 00000, "Navigator: Failed to Start Tracing"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00280, 00000, "\tMax Avg Bytes/Sec             : %.2f\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00281, 00000, "Connection Manager: Forced Log output\n"
// *Cause: Message sent back to control program from Connection Manager.
// *Action: None.
/
00282, 00000, "Connection Manager: Failed to force log, logging is off\n"
// *Cause: Message sent back to control program from Connection Manager.
// *Action: None.
/
00283, 00000, "\nListening on the following TNS addresses:\n\n"
// *Cause: Message sent back to control program from Connection Manager.
// *Action: None.
/
00284, 00000, "\tImm Max Avg Bytes/Sec         : %.2f\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00285, 00000, "\tAvg Connect Time (secs)       : %.2f\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00286, 00000, "\tMax Connect Time (secs)       : %.2f\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00287, 00000, "\tMin Connect Time (secs)       : %.2f\n"
// *Cause: Part of status request for Connection Manager.
// *Action: None
/
00288, 00000, "Navigator: Failed to Disable Interchange"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00289, 00000, "Navigator: Disabled Interchange"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00290, 00000, "Navigator: Failed to Enable Interchange"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00291, 00000, "Navigator: Enabled Interchange"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00292, 00000, "\tLog File Name                 :\n\t\t%s\n"
// *Cause: Message sent back to control program showing log file name
// *Action: None.
/
00293, 00000, "\tTrace File Name                 :\n\t\t%s\n"
// *Cause: Message sent back to control program showing trace file name
// *Action: None.
/
00294, 00000, "Connection Manager: Security is enabled, you cannot STOP the Interchange\n"
// *Cause: Message sent back to control program indicating that the connection
//         manager is secure.
// *Action: None.
/
00295, 00000, "Navigator: Security is enabled, you cannot STOP the Navigator\n"
// *Cause: Message sent back to control program indicating that the Navigator
//         is secure.
// *Action: None.
/
00296, 00000, "\tStoppable                     : %s\n"
// *Cause: Message sent back to control program indicating whether program
//         can be stopped.
// *Action: None.
/
00297, 00000, "\tLogging Level                 : %s\n"
// *Cause: Message sent back to control program indicating whether program
//         can be stopped.
// *Action: None.
/
00298, 00000, "Request to Navigator:\n%s\n"
// *Cause: Log entry for request to Navigator.
// *Action: None.
/
00299, 00000, "Response from Navigator:\n%s\n"
// *Cause: Log entry for request to Navigator.
// *Action: None.
/
00300, 00000, "***Disabling Interchange : %s\n"
// *Cause: Log entry for disabling a particular Interchange.
// *Action: None.
/
00301, 00000, "***Enabling Interchange : %s\n"
// *Cause: Log entry for disabling a particular Interchange.
// *Action: None.
/
00302, 00000, "Connection Manager: Unknown Request"
// *Cause: Request sent by Interchange control program is unknown.
// *Action: None.
/
00303, 00000, "Connection Manager: Reread parameter data"
// *Cause: Request sent by control manager to control programming indicating
//         that parameter data was read.
// *Action: None.
/
00304, 00000, "Status Information for Connection Manager:\n"
// *Cause: Message sent back by Interchange as header for status request.
// *Action: None
/
00305, 00000, "The Navigator encountered an invalid/unknown trace level\n"
// *Cause: Message sent back by the Navigator indicating an invalid trace level.
// *Action: Reattempt the request with a correct trace level.
/
00306, 00000, "Connection Manager encountered an invalid/unknown trace level\n"
// *Cause: Message sent back by the Connection Manager indicating an
// invalid trace level.
// *Action: Reattempt the request with a correct trace level.
/
00307, 00000, "Navigator: Reread parameter data"
// *Cause: Request sent by the Navigator to control program indicating
//         that parameter data was read.
// *Action: None.
/
00308, 00000, "Navigator: Failed to open log while rereading parameter data"
// *Cause: Request sent by the Navigator to control program indicating
//         that it could not reopen log file after rereading parameter data.
// *Action: None.
/
00309, 00000, "Connection Manager: Failed to open log while re-reading parameter data"
// *Cause: Request sent by the Connection Manager to control program
//         indicating that it could not reopen log file after rereading
//         parameter data.
// *Action: None.
/
00310, 00000, "Navigator: Failed to start tracing after rereading parameter data"
// *Cause: Message sent back to control program from Navigator.
// *Action: None.
/
00311, 00000, "Connection Manager: Failed to start tracing after rereading parameter data"
// *Cause: Message sent back to control program from Connection Manager.
// *Action: None.
/
00312, 00000, "Connection Manager: Failed to get version information"
// *Cause: Message sent back to control program from Connection Manager.
// *Action: None.
/
00313, 00000, "Navigator: Failed to get version information"
// *Cause: Message sent back to control program from Connection Manager.
// *Action: None.
/
00314, 00000, "Protocol Adapter Errors: %u,%u\n"
// *Cause: Protocol Adapter errors which go with message 233
// *Action: None.
/
00315, 00000, "Failed to allocate larger connect data area for getting pump data: %u\n"
// *Cause: Could not allocate a large enough area to get pump statistics;
// continue without them.
// *Action: None.
/
00316, 00000, "Ran out of data buffers in the pump\n"
// *Cause: The Interchange is resource limited by having too few data buffers
//  in the pump.
// *Action: If the problem persists (that is, there are a lot of log messages),
//  increase the number of pump buffers by increasing the value of
//  the parameter PUMP_BUFFERS in INTCHG.ORA. Then shutdown and restart the
//  Interchange to make the changes take effect.
/
00317, 00000, "Failed to contact Connection Manager"
// *Cause: Connection Manager is not running.
// *Action: Start the Connection Manager and retry
/

///////////////////////////////////////////////////////////////////////////
/
/ 00501 - 00999 NT errors
/
///////////////////////////////////////////////////////////////////////////
00501, 00000, "Cannot allocate memory"
// *Cause:  Sufficient memory could not be allocated to perform the desired
// activity.
// *Action:  Either free some resource for TNS or add more memory to the
// machine. For further details, turn on tracing and reexecute the operation.
/
00502, 00000, "Invalid argument"
// *Cause:  An internal function received an invalid parameter.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
00503, 00000, "Illegal ADDRESS parameters"
// *Cause: An illegal set of protocol adapter parameters was specified.
// *Action: Check the parameters within the ADDRESS section of the
// TNSNAMES.ORA file. It may be helpful to turn on tracing and look at
// the addresses specified in the trace file, checking for spelling or
// other errors. Be sure to turn tracing off when the trace is complete.
/
00504, 00000, "Operation not supported"
// *Cause:  An internal function received a request to perform an
// operation that is not supported (on this machine).
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
00505, 00000, "Operation timed out"
// *Cause: The requested operation could not be completed within the timeout
// period.
// *Action: For further details, turn on tracing and reexecute the operation.
/
00506, 00000, "Operation would block"
// *Cause: An internal operation did not commence because to do so would
// block the current process and the user has requested that operations be
// non-blocking.
// *Action:  None needed; this is an information message.
/
00507, 00000, "Connection closed"
// *Cause: Normal "end of file" condition has been reached; partner has
// disconnected.
// *Action: None needed; this is an information message.
/
00508, 00000, "No such protocol adapter"
// *Cause: The protocol adapter requested for this connection does not exist.
// *Action: Install the protocol adapter or use one that is available. Be
// sure that the correct protocols are listed in the configuration files.
/
00509, 00000, "Buffer overflow"
// *Cause: Too much data for buffer.
// *Action: Reexecute with larger receive buffer or smaller send buffer.
/
00510, 00000, "Internal limit restriction exceeded"
// *Cause: Too many files or sockets open simultaneously (or some other
// resource has been depleted).
// *Action: For further details, trace the operation for protocol
// details.
/
00511, 00000, "No listener"
// *Cause: The connect request could not be completed because no application
// is listening on the address specified, or the application is unable to
// service the connect request in a sufficiently timely manner.
// *Action: Ensure that the supplied destination address matches one of
// the addresses used by the listener - compare the TNSNAMES.ORA entry with
// appropriate LISTENER.ORA file (or TNSNAV.ORA if the connection is to go
// by way of an Interchange. Start the listener on the remote machine.
/
00512, 00000, "Address already in use"
// *Cause: Specified listener address is already being used.
// *Action: Start your listener with an unused address.
/
00513, 00000, "Destination host unreachable"
// *Cause: Contact cannot be made with remote party.
// *Action: Make sure the network driver is functioning and the network is up.
/
00514, 00000, "Contexts have different wait/test functions"
// *Cause: Two protocol adapters have conflicting wait/test functions.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
00515, 00000, "Connect failed because target host or object does not exist"
// *Cause: The address specified is not valid, or the program being 
// connected to does not exist.
// *Action: Ensure the ADDRESS parameters have been entered correctly; the
// most likely incorrect parameter is the node name.  Ensure that the 
// executable for the server exists (perhaps "oracle" is missing.)
/
00516, 00000, "Permission denied"
// *Cause: User has insufficient privileges to perform the requested operation.
// *Action: Acquire necessary privileges and try again.
/
00517, 00000, "Lost contact"
// *Cause: Partner has unexpectedly gone away.
// *Action: Investigate partner application for abnormal termination.
/
00518, 00000, "Incomplete read or write"
// *Cause: A data send or receive failed.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
00519, 00000, "Operating system resource quota exceeded"
// *Cause: The current user has exceeded the allotted resource assigned in the
// operating system.
// *Action: Acquire more operating system resource, or perform a different
// function.
/
00520, 00000, "Syntax error"
// *Cause: The supplied connect descriptor contains illegal syntax.
// *Action: Check the syntax of the connect descriptor for correct syntax.
/
00521, 00000, "Missing keyword"
// *Cause: The supplied connect descriptor is missing one or more TNS
// keywords.
// *Action: Check the syntax, and ensure all required keywords are present.
/
00522, 00000, "Operation was interrupted"
// *Cause: An internal operation was interrupted and could not complete.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
00523, 00000, "Previous operation was busy"
// *Cause:  Operation tried could not be successfully completed because
// the requested resource was busy.
// *Action: Attempt the operation again. If error persists, contact
// Oracle Customer Support.
/
00524, 00000, "Current operation is still in progress"
// *Cause:  Internal operation is still in progress but will complete.
// *Action: None; wait for operation to complete.
/
00525, 00000, "Insufficient privilege for operation"
// *Cause:  Operating system failed to complete operation because user
// lacked sufficient privileges.
// *Action: Check your platform-specific privileges.
/
00526, 00000, "No caller (false async event)"
// *Cause:  Internal error.
// *Action: For further details, turn on tracing and reexecute the operation.
/
00527, 00000, "Protocol Adapter not loadable"
// *Cause:  On some platforms (for example OS/2) protocol adapters are loaded at
// run-time. If the shared library (or DLL) for the protocol adapter
// is missing or one of its supporting libraries is missing, then this
// error is returned.
// *Action: For further details, turn on tracing and reexecute the operation.
// The trace file will have the name of the shared library (or DLL) that
// could not be loaded.
/
00528, 00000, "Protocol Adapter not loaded"
// *Cause:  On some platforms (for example OS/2) protocol adapters are loaded at
// run-time. If the shared library (or DLL) for the protocol adapter has not
// been loaded, then this error is returned.
// *Action: For further details, turn on tracing and reexecute the operation.
// The trace file will have the name of the shared library (or DLL) that has
// not been loaded.
/
00530, 00000, "Protocol adapter error"
// *Cause: A generic protocol adapter error occurred.
// *Action: For further details, turn on tracing and reexecute the operation.
/
00532, 00000, "No previous async operation to wait on"
// *Cause:  Internal protocol adapter error.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
00533, 00000, "Connection dissolved or not yet made"
// *Cause:  Internal protocol adapter error.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
00534, 00000, "Failed to grant connection ownership to child"
// *Cause:  Internal protocol adapter error.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
00535, 00000, "Failed to send or receive disconnect message"
// *Cause:  Internal protocol adapter error.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
00536, 00000, "Connection entered inappropriate state"
// *Cause:  Internal protocol adapter error.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
00537, 00000, "Index into protocol adapter table is out of legal range"
// *Cause:  Internal protocol adapter error.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
00539, 00000, "Network or Protocol services are down"
// *Cause:  The Network services on or from your node are not running
// or have stopped running.
// *Action: Restart your network or protocol services on this platform.
// If error persists, contact Oracle Customer Support.
/
/ Reserved for NTZ/SSL errors: 540 - 579
00540, 00000, "SSL protocol adapter failure"
// *Cause:  The SSL protocol adapter encountered an error.
// *Action: In most cases, this error should only be pair with a more
//          meaningful ORA- error.
/
00541, 00000, "underlying transport does not exist."
// *Cause:  The SSL protocol adapter was unable to locate an adapter
//          for the protocol that it is going to use as the data transport.
// *Action: In most cases, the underlying transport is TCP. Make sure that 
//          the Oracle Net TCP/IP adapter was installed.
/
00542, 00000, "SSL Handshake failed"
// *Cause:  The SSL protocol adapter was unable to connect to another
//          process.
// *Action: This error can be caused by a variety of problems including
//          the termination of the peer process. Enable Oracle Net tracing and
//          attempt the connection again. The trace file should give some
//          clues as to what the exact problem is.
/
00543, 00000, "internal error"
// *Cause:  The SSL protocol adapter encountered an unexpected error.
// *Action: This error is not normally visible to users.
//          Enable Oracle Net tracing and attempt to reproduce the error. 
//          If it occurs, contact Oracle customer support.
/
00544, 00000, "unsupported operation"
// *Cause:  The SSL adapter could not perform a given command.
// *Action: This error is not normally visible to users.
//          Enable Oracle Net tracing and attempt to reproduce the error. 
//          If it occurs, contact Oracle customer support.
/
00545, 00000, "parameter retrieval failure"
// *Cause:  The SSL protocol adapter was not able to retrieve a configuration
//          parameter for some reason.
// *Action: This error is not normally visible to users.
//          Enable Oracle Net tracing and attempt to reproduce the error. 
//          If it occurs, contact Oracle customer support.
/
00546, 00000, "control failure"
// *Cause:  The SSL protocol adapter was unable to perform a command.
// *Action: This error is not normally visible to users.
//          Enable Oracle Net tracing and attempt to reproduce the error. 
//          If it occurs, contact Oracle customer support.
/
00547, 00000, "user information retrieval failed"
// *Cause:  The SSL protocol adapter was unable to retrieve information about
//          the remote user.
// *Action: Examine the first error in the error stack. It should describe
//          the error in more detail.
/
00548, 00000, "value specified for client authentication parameter is not boolean"
// *Cause:  The value specified for the parameter that specifies that SSL
//          client authentication is to be used was not boolean.
// *Action: Specify a correct value for the parameter.
/
00549, 00000, "value specified for the SSL version is not valid"
// *Cause:  The value specified for the SSL version is not valid.
// *Action: Specify a valid value for the SSL version.
//          
/
00550, 00000, "disconnection error"
// *Cause:  The SSL protocol adapter encountered an error when the underlying
//          transport disconnected.
// *Action: This error is not normally visible to users.
//          Enable Oracle Net tracing and attempt to reproduce the error. 
//          If it occurs, contact Oracle customer support.
/
00551, 00000, "underlying transport connection failed"
// *Cause:  The underlying transport adapter used by the SSL adapter failed
//          to connect.
// *Action: Enable Oracle Net tracing and try the connection again. If the
//          connection fails, examine the trace file to determine the cause.
/
00552, 00000, "no valid cipher suites were specified"
// *Cause:  SSL cipher specs were specified, but none were valid.
// *Action: Specify correct cipher suites.
/
00553, 00000, "read failed"
// *Cause:  The SSL adapter failed to read data from its connection.
// *Action: Examine the contents of sqlnet.log for more information. Enable
//          Oracle Net tracing and try the connection again. If the
//          connection fails, examine the trace file to determine the cause.
/
00554, 00000, "write failed"
// *Cause:  The SSL adapter failed to send data over its connection.
// *Action: Examine the contents of sqlnet.log for more information. Enable
//          Oracle Net tracing and try the connection again. If the
//          connection fails, examine the trace file to determine the cause.
/
00555, 00000, "no directory specified for wallet resource locator"
// *Cause:  It was specified that a file was to be used from which to retrieve
//          a wallet, but no directory was specified for the wallet.
// *Action: Specify the directory where the wallet is located.
/
00556, 00000, "no method specified for wallet retrieval"
// *Cause:  A wallet resource locator was specified, but no method was
//          given for the retrieval of the wallet.
// *Action: Specify the method by which the method is to be retrieved.
/
00557, 00000, "unsupported wallet retrieval method"
// *Cause:  The method specified for wallet retrieval is not supported.
//          Currently, only files are supported for wallet retrieval.
// *Action: Specify "FILE" as the wallet retrieval method.
/
00558, 00000, "Entrust login failed"
// *Cause:  Entrust failed to authenticate the username, password, and/or
//          profile name that was presented.
// *Action: Specify correct values for the username, password or profile name.
//          If no data was prompted for, contact Oracle support.
/
00559, 00000, "load of Entrust certificate failed"
// *Cause:  An error occurred while attempting to validate the provided Entrust
//          certificate.
// *Action: This error is not normally visible to users. Enable Oracle Net
//          tracing and attempt to reproduce the error. If it occurs, contact
//          Oracle customer support.
/
00560, 00000, "extraction of name from Entrust certificate failed"
// *Cause:  An error occurred while attempting to extract a name
//          from an Entrust certificate.
// *Action: This error is not normally visible to users. Enable Oracle Net 
//          tracing and attempt to reproduce the error. If it occurs, contact 
//          Oracle customer support.
/
00580, 00000, "Read failed due to closed or invalid transport connection"
// *Cause:  Read attempt was made on a transport connection which was
//          previously terminated or is somehow deemed to be invalid.
// *Action: Indicates a substantial transport level failure. Check the
//          O/S configuration for the particular transport or contact the
//          transport provider. For further details, turn on tracing and
//          reexecute the operation.
/
00581, 00000, "Send failed due to timeout"
// *Cause:  The send operation did not complete within the allowed time
//          interval.
// *Action: Error is informational. Note, repeated receipt of this error 
//          could indicate an attempted Denial-Of-Service attack. Also,
//          if the receipt of this error interferes w/ a customer's normal
//          operations, the customer may wish to lengthen the timeout.
/
00582, 00000, "Receive failed due to timeout"
// *Cause:  The receive operation did not complete within the allowed time
//          interval.
// *Action: Error is informational. Note, repeated receipt of this error 
//          could indicate an attempted Denial-Of-Service attack. Also,
//          if the receipt of this error interferes w/ a customer's normal
//          operations, the customer may wish to lengthen the timeout.
/
00583, 00000, "Valid node checking: unable to parse configuration parameters"
// *Cause:  Valid node checking was unable to parse the configuration due to
//          syntactical errors.
// *Action: Ensure that the configuration syntax matches the Oracle
//          reference manual documented syntax. 
//          For further details, turn on tracing and reexecute the operation.
/
00584, 00000, "Valid node checking configuration error"
// *Cause:  Valid node checking specific Oracle Net configuration is invalid.
// *Action: Ensure the hosts specified in the "invited_nodes" and 
//          "excluded_nodes" are valid. 
//          For further details, turn on tracing and reexecute the operation.
/
///////////////////////////////////////////////////////////////////////////
/
/ 01000 - 02500 NSG errors
/
// NLS_DO_NOT_TRANSLATE [01000,01019]
01000, 00000, "spawn [<listener_name>] <spawn_alias> [<(ARGUMENTS='arg0, arg1,...')>]\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01001, 00000, "start [<listener_name>] : start listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01002, 00000, "stop [<listener_name>] : stop listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01003, 00000, "status [<listener_name>] : get the status of listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01004, 00000, "reload [<listener_name>] : reload the parameter files and SIDs\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01005, 00000, "trace OFF | USER | ADMIN | SUPPORT [<listener_name>] : set tracing to the specified level\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01006, 00000, "set password : set the password for subsequent calls\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01007, 00000, "quit | exit : exit LSNRCTL\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01008, 00000, "version [<listener_name>] : get the version information of the listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01009, 00000, "service [<listener_name>] : get the service information of the listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01013, 00000,"set|show trc_{ } [<value>]: set|show trace parameters of current listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01014, 00000, "set|show log_{ } [<value>]: set|show log parameters of current listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01015, 00000, "set|show parm_name [<value>]: sets|shows current listener parm values\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01016, 00000, "change_password [<listener_name>]: changes the password of the listener\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01017, 00000, "set|show current_listener [<listener_name>]: sets|shows current listener\n" 
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01018, 00000, "save_config [<listener_name>]: saves configuration changes to parameter file\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01019, 00000, "set rawmode ON | OFF: set output mode for services and status commands\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
01020, 00000, "STATUS of the LISTENER\n"
// *Cause:  Control program status message.
// *Action: None.
/
01021, 00000, "------------------------\n"
// *Cause:  Control program status message.
// *Action: None.
/
01022, 00000, "Alias                     %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01023, 00000, "Version                   %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01024, 00000, "Trace Level               %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01025, 00000, "Security                  %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01026, 00000, "Start Date                %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01027, 00000, "Listener Trace File       %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01028, 00000, "Listener Log File         %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01029, 00000, "Services Summary...\n"
// *Cause:  Control program status message.
// *Action: None.
/
01030, 00000, "The listener supports no services\n"
// *Cause:  Control program status message.
// *Action: None.
/
01033, 00000, "Listener Parameter File   %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01034, 00000, "Uptime                    %lu days %lu hr. %lu min. %lu sec\n"
// *Cause:  Control program status message.
// *Action: None.
/
01036, 00000, "%s established:%s refused:%s"
// *Cause:  Control program status message.
// *Action: None.
/
01037, 00000, "\"%s\" established:%s refused:%s"
// *Cause:  Control program status message.
// *Action: None.
/
01038, 00000, "%s established:%s refused:%s current:%s max:%s state:%s"
// *Cause:  Control program status message.
// *Action: None.
/
01039, 00000, "%s\t\thas %s service handler(s)"
// *Cause:  Control program status message.
// *Action: None.
/
01040, 00000, "SNMP                      %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01041, 00000, "%s parameter \"%s\" set to %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01042, 00000, "Current Listener is %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01043, 00000, "Password changed for %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01044, 00000, "%s(Registered)\t\thas %s service handler(s)"
// *Cause:  Control program status message.
// *Action: None.
/
01045, 00000, "%s(Not Registered)\t\thas %s service handler(s)"
// *Cause:  Control program status message.
// *Action: None.
/
01046, 00000, "Saved %s configuration parameters.\n"
// *Cause:  Control program status message.
// *Action: None.
/
01047, 00000, "Old Parameter File   %s\n"
// *Cause:  Control program status message.
// *Action: None.
/
01048, 00000, "No changes to save for %s.\n"
// *Cause:  Control program status message.
// *Action: None.
/
01049, 00000, "%s (%s)\t\thas %s service handler(s)"
// *Cause:  Control program status message.
// *Action: None.
/

01050, 00000, "%s"
// *Cause:  Control program general message.
// *Action: None.
/
01052, 00000, "The command completed successfully\n"
// *Cause:  Control program general message.
// *Action: None.
/
01053, 00000, "Connecting to %s\n"
// *Cause:  Control program general message.
// *Action: None.
/
01054, 00000, "Contacted the listener successfully\n"
// *Cause:  Control program general message.
// *Action: None.
/
01055, 00000, "Successfully stopped the listener\n"
// *Cause:  Control program general message.
// *Action: None.
/
01057, 00000, "Program name: %s\n"
// *Cause:  Control program general message.
// *Action: None.
/
01058, 00000, "Arguments   : %s\n"
// *Cause:  Control program general message.
// *Action: None.
/
01059, 00000, "Environment : %s\n"
// *Cause:  Control program general message.
// *Action: None.
/
01060, 00000, "The password has has been set to: %s\n"
// *Cause:  Control program general message.
// *Action: None.
/
01061, 00000, "The password has not been set\n"
// *Cause:  Control program general message.
// *Action: None.
/
01062, 00000, "The db subagent is already running.\n"
// *Cause:  Control program general message.
// *Action: None.
/
01063, 00000, "The db subagent is not started.\n"
// *Cause:  Control program general message.
// *Action: None.
/
01064, 00000, "Listener configuration changes will not be persistent\n"
// *Cause:  Configuration changes to the listener will not be 
// visible when the listener starts up again as the check-pointing
// has been turned off in listener.ora
// *Action: Edit LISTENER.ORA setting USE_CKPFILE_LISTENER=true
/
01065, 00000, "Raw mode is %s\n"
// *Cause:  Control program general message.
// *Action: None.
/
01066, 00000, "Presentation: %s"
// *Cause:  Listener starting message.
// *Action: None.
/
01067, 00000, "Service display mode is %s\n"
// *Cause:  Control program general message.
// *Action: None.
/
01070, 00000, "Starting %s: please wait...\n\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01071, 00000, "%s is set to %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01072, 00000, "Started at %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01073, 00000, "Listening on: %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01074, 00000, "Error listening on: %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01075, 00000, "Opened log file: %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01076, 00000, "Opened trace file: %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01077, 00000, "Opened parameter file: %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01078, 00000, "Opened name lookup file: %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01079, 00000, "Attempted to bequeath: %s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01080, 00000, "Listener failed to start. See the error message(s) above...\n\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01081, 00000, "Started with pid=%s\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01082, 00000, "Running in PROXY mode\n"
// *Cause:  Listener starting message.
// *Action: None.
/
01090, 00000, "No longer listening on: %s\n"
// *Cause:  Listener logging message.
// *Action: None.
/
01093, 00000, "%s * %s * %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01094, 00000, "%s * %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01095, 00000, "%s * %s * %s * %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01096, 00000, "%s * %s * %s * %s * %s * %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01097, 00000, "\nTIMESTAMP * CONNECT DATA [* PROTOCOL INFO] * EVENT [* SID] * RETURN CODE"
// *Cause:  Listener logging message.
// *Action: None.
/
01098, 00000, "TIMESTAMP *  CONNECT  DATA *   ADDRESS *  [PRESENTATION *] COMMAND * ERROR\nTIMESTAMP * [INSTANCE NAME *] [ADDRESS *] [PRESENTATION *] COMMAND * ERROR\n-------------------------------------------------------------------------------"
// *Cause:  Listener logging message.
// *Action: None.
/
01099, 00000, "%s * %s * %s * %s * %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01100, 00000, "TNS returned error %d when attempting to start the listener"
// *Cause: The bequeath (BEQ) mechanism that LSNRCTL uses to start the listener
// failed.
// *Action: If NS error code 12538 is also returned then the BEQ driver
// is not installed; call Oracle Worldwide Support as the BEQ driver should
// always be installed. If this is not the problem then the error is probably
// caused by the fact that the TNSLSNR executable cannot be found in the place
// expected in your platform's ORACLE environment. Verify that the full
// pathname of the TNSLSNR executable as displayed by LSNRCTL is correct.
/
01101, 00000, "Could not find service name %s"
// *Cause:  The ervice name could not be resolved by name-lookup.
// *Action: Verify that the listener name or service name specified to
// LSNRCTL has the correct name and address defined in LISTENER.ORA or in
// TNSNAMES.ORA.
/
01102, 00000, "TNS application contacted was not the listener"
// *Cause:  Another TNS application such as the Interchange was listening
// at the address contacted. There may be another TNS application listening
// at the address contacted and the data returned is not in the appropriate
// format.
// *Action: Verify that the listener name or service name specified to
// LSNRCTL has the correct name and address defined in LISTENER.ORA or in
// TNSNAMES.ORA.
/
01103, 00000, "Protocol specific component of the address is incorrectly specified"
// *Cause:  The ADDRESS used to contact the listener is not correctly specified.
// This error occurs because the address fails to specify the destination
// of the listener. The address is well formed (for example, there are no
// missing parentheses) but it is missing a protocol specific component. For
// example, this is the error returned when the HOST component is missing from
// a TCP/IP address string.
// *Action: Edit the ADDRESS in LISTENER.ORA to include the required
// protocol-specific keywords.  For more information about the keywords
// required by different protocol adapters, see the Oracle operating system
// specific documentation for your platform.
/
01106, 00000, "Listener using listener name %s has already been started"
// *Cause:  Another listener is already listening on one of the ADDRESSes
// specified.
// *Action: Shutdown the previous listener specified by the listener name
// before starting this one.
/
01107, 00000, "A valid trace level was not specified"
// *Cause:  Failed to specify a valid trace level for the LSNRCTL trace command.
// *Action: Specify one of OFF, USER, ADMIN, or SUPPORT.
// Type "LSNRCTL help trace" for more information or consult Chapter 2 of
// this manual for an introduction to the concepts of tracing.
/
01108, 00000, "Listener password prompt failed"
// *Cause:  Password not entered via tty
// *Action: Enter the listener password on a tty device
/
01109, 00000, "Listener password encryption failed"
// *Cause:  Possibly garbled password entered
// *Action: Re-enter the listener password, using valid ASCII characters. If
// problem persists, contact Oracle Customer Support.
/
01110, 00000, "Mismatch - password unchanged"
// *Cause:  New password and reentered new password are different"
// *Action: Re-enter the listener password, make sure that New password
// and reentered new password are the same
/
01111, 00000, "Log status can either be ON or OFF"
// *Cause:  Failed to specify a log status value for the LSNRCTL log_status command.
// *Action: Specify one of ON or OFF.
// Type "LSNRCTL help set log_status" for more information or consult Chapter 2 of
// this manual for an introduction to the concepts of logging.
01112, 00000, "Plug and play can either be ON or OFF"
// *Cause:  Failed to specify a valid value for the LSNRCTL use_plugandplay command.
// *Action: Specify one of ON or OFF.
// Type "LSNRCTL help set use_plugandplay" for more information.
/
01113, 00000, "save_config_on_stop can either be ON or OFF"
// *Cause:  Failed to specify a valid value for the LSNRCTL save_config_on_stop command.
// *Action: Specify one of ON or OFF.
// Type "LSNRCTL help set save_config_on_stop" for more information.
/
01114, 00000, "LSNRCTL could not perform local OS authentication with the listener"
// *Cause:  LSNRCTL failed to obtain system resources (heap memory, or shared 
// memory) needed to perform local OS authentication with the listener.
// *Action: Make sure that system resources like shared memory and heap memory
// are available for LSNRCTL tool to execute properly.
/
01115, 00000, "OS error %s creating shared memory segment of %s bytes with key %s"
// *Cause:  The shared memory segment could not be created as requested. For 
// example, a segment with the provided key may already exist, or the size may
// be outside of system allowed range.
// *Action: Use the error code to determine the exact cause of the problem. In
// certain cases the problem may be resolved by adjusting the system-imposed 
// limits such as the maximum number of allowed shared memory segments, or 
// their maximum and minimum sizes. In other cases, resources need to be freed
// up first for the operation to succeed.
/
01116, 00000, "Listener alias name given as connect identifier is too long"
// *Cause: The listener alias name you were attempting to resolve was too long. 
// *Action: The maximum length of a listener alias name is 255 bytes; this 
//          limit has been exceeded. Use a smaller listener alias name. 
/
01150, 00000, "The address of the specified listener name is incorrect"
// *Cause:  The address on which the listener attempted to listen contains a
// syntax error.
// *Action: For the listener name or service name specified to LSNRCTL, check
// that the address or connect descriptor is well-formed. You can find the
// listener name in LISTENER.ORA, or you can access the listener through
// the service name is TNSNAMES.ORA.
/
01151, 00000, "Missing listener name, %s, in LISTENER.ORA"
// *Cause:  The listener could not find the listener name specified.
// *Action: Make sure valid addresses on which to listen are specified for the
// listener name in LISTENER.ORA.
/
01152, 00000, "All addresses specified for the listener name, %s, failed"
// *Cause:  The listener failed to listen on any of the specified addresses.
// *Action: Make sure that another application is not listening on the addresses
// specified or check that the appropriate protocol adapters are installed.
// Turn on tracing and execute again for more information.
/
01153, 00000, "Failed to process string: %s"
// *Cause:  The string specified is not well-formed.
// *Action: Not normally visible to the user. For further details,
// turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
// *Comment: Do not include in error manual.
/
01154, 00000, "SID detected in old format that is no longer supported"
// *Cause:  One of the SIDs was specified in an obsolete format.
// *Action: Check LISTENER.ORA for a line of the form:
// <sid> = (SID=(ORACLE_HOME=<oracle_home>))        OR
// <sid> = (SID_DESC=(ORACLE_HOME=<oracle_home>))
// The above format is no longer supported and SID_LIST_<listener_name>
// format described in the Oracle9i Net Services Reference Guide should be used.
// For example,
// SID_LIST_LISTENER = (SID_LIST=(SID_DESC=(SID_NAME=<sid>)(ORACLE_HOME=<oracle_home>)))
/
01155, 00000, "Incorrectly specified SID_LIST_%s parameter in LISTENER.ORA"
// *Cause:  SID_LIST_<listener_name> in LISTENER.ORA has an error in it.
// *Action: Be sure this parameter is specified as described in the
// Oracle9i Net Services Reference Guide. For example,
// SID_LIST_LISTENER = (SID_LIST=(SID_DESC=(SID_NAME=<sid>)(ORACLE_HOME=<oracle_home>)))
/
01156, 00000, "Missing or inappropriate PROTOCOL, TIMEOUT or POOL_SIZE parameter from PRESPAWN_DESC"
// *Cause:  PRESPAWN_DESC in each SID_DESC does not have required fields.
// *Action: Be sure the parameters required for PRESPAWN_DESC are specified
// in each SID_DESC. For example,
// SID_LIST_LISTENER = (SID_LIST=(SID_DESC=(SID_NAME=<sid>)(PRESPAWN_MAX=5)(ORACLE_HOME=<oracle_home>)(PRESPAWN_DESC=(PROTOCOL=tcp)(POOL_SIZE=10)(TIMEOUT=30))))
// Add or correct these parameters in the LISTENER.ORA file
/
01157, 00000, "Can only listen on %d addresses - ignoring %s"
// *Cause:  Too many addresses were given to listen on.
// *Action: Reduce the number of addresses to listen on and use another
// listener to listen on the remaining addresses.
/
01158, 00000, "Internal connection limit reached, preventing dispatcher from connecting"
// *Cause:  The internal Oracle Net connection list is full. Too many
// dispatchers are connected to the listener; therefore, no more dispatchers
// are allowed to connect.
// *Action: For further details, turn on tracing and reexecute the
// operation. If error persists, contact Oracle Customer Support.
/
01159, 00000, "Internal connection limit has been reached; listener has shut down"
// *Cause:  The internal Oracle Net connection list is full. The listener is
// configured to use too many Oracle Net connections.
// *Action: Reduce the number of listen addresses or services connected to
// the listener. For further details, turn on tracing and reexecute the
// operation. If error persists, contact Oracle Customer Support.
/
01160, 00000, "Trace level was not specified"
// *Cause:  Failed to specify a trace level for the trace command.
// *Action: Specify one of OFF, USER, ADMIN, or SUPPORT.
// Users should not see this error if LSNRCTL is being used.
// *Comment: Do not include in error manual.
/
01161, 00000, "Spawn alias %s was not found. Check listener parameter file"
// *Cause:  The alias specified to spawn a program was not found in LISTENER.ORA.
// *Action: This is not seen in normal use of Oracle Net.
// *Comment: See the porting notes or internal documentation on how to have
// the listener spawn a process.
// Do not include in error manual.
/
01162, 00000, "Syntax error in the address resolved from the spawn alias: %s"
// *Cause:  The alias specified to spawn a program was not a valid NVstring.
// *Action: This is not seen in normal use of Oracle Net.
// *Comment: See the porting notes or internal documentation on how to have
// the listener spawn a process.
// Do not include in error manual.
/
01163, 00000, "Failed to spawn process: %s"
// *Cause:  The process failed to start correctly.
// *Action: This is not seen in normal use of Oracle Net.
// *Comment: Turn on tracing in the listener and execute again. This problem is
// most often caused by the executable specified to be missing from the PATH
// in the listener's environment. See the porting notes or internal documentation
// on how to have the listener spawn a process.
// Do not include in error manual.
/
01164, 00000, "No spawn alias sent to listener"
// *Cause:  The spawn command was issued without an alias.
// *Action: This is not seen in normal use of Oracle Net.
// *Comment: See the porting notes or internal documentation on how to have
// the listener spawn a process. Users should not see this error if LSNRCTL
// is being used.
// Do not include in error manual.
/
01165, 00000, "Spawn alias has no program name set in it"
// *Cause:  The spawn alias in LISTENER.ORA is incorrectly specified.
// *Action: This is not seen in normal use of Oracle Net.
// *Comment: Make sure the NAME component of the PROCESS description is set.
// Do not include in error manual.
/
01167, 00000, "The command %s is not supported by the listener contacted"
// *Cause:  The listener does not recognize the command.
// *Action: This is caused when a newer version of LSNRCTL contacts an old
// listener. Upgrade listener if executing this command is important.
/
01168, 00000, "Cannot allocate memory"
// *Cause:  Sufficient memory could not be allocated to perform the desired
// activity.
// *Action:  Either free some resource for TNS, or add more memory to the
// machine. For further details, turn on tracing and reexecute the operation.
/
01169, 00000, "The listener has not recognized the password"
// *Cause: The listener has the password security mechanism enabled and 
// requires the correct password to execute any command other than VERSION.
// The user attempted to issue one of the privileged administrative commands, 
// but could not be successfully authenticated with the password provided.
// *Action: If an authorized user is attempting the command, then use the 
// SET PASSWORD command at the LSNRCTL prompt with the listener password. 
// If you do not know the password, then you are trying to execute 
// an inappropriate command. 
/
01170, 00000, "Event detection broke for address: %s"
// *Cause:  The event detection mechanism for the address specified returned
// an error.
// *Action: Future attempts to detect events on this address will fail.
// The listener will deallocate the listen address and connections will no
// long be accepted for this address. This error is not normally visible
// to the user. For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
01171, 00000, "Event detection broke for dispatcher: %s"
// *Cause:  The event detection mechanism for the dispatcher specified returned
// an error.
// *Action: Future attempts to detect events on this dispatcher will fail.
// The listener will deallocate the dispatcher and connections will no
// long be redirected to this dispatcher. This error is not normally visible
// to the user. For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
01172, 00000, "Listener has shut down since all listen addresses have been deallocated"
// *Cause:  The event detection mechanism broke and caused all listen addresses
// to be removed.
// *Action: Error 1170 has occured and caused all the listen addresses to be
// deallocated. Since all the listen addresses have been removed,
// no more connections can be established to this listener so it shuts itself
// down. This error is not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
01173, 00000, "Missing or inappropriate PRESPAWN_MAX parameter from SID_DESC"
// *Cause:  PRESPAWN_MAX in each SID_DESC does not have required fields.
// *Action: Be sure the parameters required for PRESPAWN_DESC are specified
// in each SID_DESC. For example,
// SID_LIST_LISTENER = (SID_LIST=(SID_DESC=(SID_NAME=<sid>)(PRESPAWN_MAX=15)(ORACLE_HOME=<oracle_home>)(PRESPAWN_DESC=(PROTOCOL=tcp)(POOL_SIZE=10)(TIMEOUT=30))))
// Add or correct these parameters in the LISTENER.ORA file
/
01174, 00000, "The sum of the POOL_SIZEs from each PRESPAWN_DESC is greater than the PRESPAWN_MAX"
// *Cause:  The minimum value for PRESPAWN_MAX should be the sum of the POOL_SIZEs.
// *Action: Be sure the parameters required for PRESPAWN_DESC are specified
// in each SID_DESC. For example,
// SID_LIST_LISTENER = (SID_LIST=(SID_DESC=(SID_NAME=<sid>)(PRESPAWN_MAX=15)(ORACLE_HOME=<oracle_home>)(PRESPAWN_DESC=(PROTOCOL=tcp)(POOL_SIZE=10)(TIMEOUT=30))(PRESPAWN_DESC=(PROTOCOL=ipc)(POOL_SIZE=5)(TIMEOUT=15))))
// Add or correct these parameters in the LISTENER.ORA file
01175, 00000, "Password unchanged\n"
// *Cause:  Unable to set the new password
// *Action: Be sure to see that the new password has legal ASCII 
// characters. Try to set the password again.
/
01176, 00000, "Error in loading the new parameter value\n"
// *Cause:  Illegal values given for the parameters 
// *Action: Make sure that the parameter values are valid
// refer to the manual for the legal values for paramters
/
01177, 00000, "Log Status is OFF. Log file/directory unchanged\n"
// *Cause:  Log status needs to be set ON  for changing the log file 
// *Action: use command set log_status ON to set the log status of the 
// listener ON. 
/
01178, 00000, "Trace Level is 0. Trace file/directory unchanged\n"
// *Cause:  Trace Level needs to be set for changing the trace file/directory 
// *Action: use command set trc_level ON to set the trace level 
/
01179, 00000, "Listener cannot load instance class \"%s\"\n"
// *Cause:  Instance tried to register as a class unknown to listener.
// *Action: check LISTENER.ORA and/or instance configuration, and reference
//  platform documentation to find the instance classes available for the
//  listener on this platform.
/
01180, 00000, "Missing listener object %s in Directory Server"
// *Cause:  The listener could not find the listener object specified.
// *Action: Make sure the listener object is present in the Directory
// Server.
/
01181, 00000, "Internal registration connection limit reached"
// *Cause:  The number of registration connections has reached the maximum.
// No more registrations are allowed until some of the existing registration
// connections are completed.
// *Action: Disconnect existing registration connections if they are no longer
// needed.
/
01182, 00000, "Listener rejected registration of service \"%s\""
// *Cause: Received registration information could not be processed because it
// was invalid, or an internal error occurred.
// *Action: Not normally visible to the user. For further details, turn on 
// tracing and restart the instance. If error persists, contact Oracle 
// Customer Support.
// *Comment: Do not include in error manual.
/
01183, 00000, "Listener rejected registration or update of instance \"%s\""
// *Cause: Received registration or update information could not be processed 
// because it was invalid, or an internal error occurred.
// *Action: Not normally visible to the user. For further details, turn on 
// tracing and restart the instance. If error persists, contact Oracle 
// Customer Support.
// *Comment: Do not include in error manual.
/
01184, 00000, "Listener rejected registration or update of service handler \"%s\""
// *Cause: Received registration or update information could not be processed 
// because it was invalid, or an internal error occurred.
// *Action: Not normally visible to the user. For further details, turn on 
// tracing and restart the instance. If error persists, contact Oracle 
// Customer Support.
// *Comment: Do not include in error manual.
/
01185, 00000, "Registration attempted from a remote node"
// *Cause: It was determined that the registering instance is not located on
// the same node as the listener. It is required that the instance be colocated
// with the listener for this type of service registration.
// *Action: Check the configuration of the registering instance. Ensure that
// local_listener parameter specifies only local listeners. Use 
// remote_listener parameter to specify remote listeners.
/
01186, 00000, "Client connection was dropped based on a filtering rule"
// *Cause: Listener was configured with a filtering rule which explicitly
// specified that the client connection should be terminated without returning 
// an error to the client.
// *Action: Modify the filtering rules if the client should be allowed access
// to the requested service.
/
01187, 00000, "No proxy service handler available"
// *Cause: One of the following conditions has occurred:
//         - the proxy service was not registered
//         - the proxy service was registered, but was blocking new connections
//         - all of the registered proxy service handlers were blocking new
//           connections
// *Action: If the proxy service is not registered it may need to be 
// restarted. If the proxy service handlers are busy and not accepting new 
// connections more of them may need to be started to handle the load.
/
01188, 00000, "Listener cannot operate with incompatible transport protocols"
// *Cause: Listener was configured with multiple listening addresses with 
// different and incompatible transport protocols. Listener cannot operate 
// efficiently in such configuration.
// *Action: Modify the existing listener configuration by removing the 
// listening address that caused the error. Configure a separate listener to 
// listen on this address.
/
01189, 00000, "The listener could not authenticate the user"
// *Cause: The user attempted to issue a privileged administrative command, but
// could not be successfully authenticated by the listener using the local OS 
// authentication mechanism. This may occur due to one of the following 
// reasons:
// 1. The user is running a version of LSNRCTL that is lower than the version
//    of the listener.
// 2. The user is attempting to administer the listener from a remote node.
// 3. The listener could not obtain the system resources needed to perform the 
//    authentication.
// 4. The local network connection between the listener and LSNRCTL was 
//    terminated unexpectedly during authentication message exchange, such as 
//    if LSNRCTL program was suddenly aborted.
// 5. The communication between the listener and LSNRCTL is being intercepted
//    by a malicious user.
// 6. The software that the user is running is not following the authentication
//    protocol, indicating a malicious user.
// *Action: Make sure that administrative commands are issued using the LSNRCTL
// tool that is of a version equal or greater than the version of the listener,
// and that the tool and the listener are running on the same node. You can 
// issue the VERSION command to find out the version of the listener. 
// If a malicious user is suspected, use the information provided in 
// the listener log file to determine the source and nature of the requests. 
// Enable listener tracing for more information. If the error persists, 
// contact Oracle Support Services.
/
01190, 00000, "The user is not authorized to execute the requested listener command"
// *Cause: Most of the listener administrative commands are only intended to 
// be issued by privileged users, for example DBAs or system administrators. 
// If the listener password is not set, then the listener only accepts 
// administrative requests from LSNRCTL running with the same OS credentials, 
// or running as a local administrator (also referred to as super user).
// *Action: If an authorized user is attempting the command, then make sure 
// that LSNRCTL is executed with the same OS user credentials as the running 
// listener, or as a local administrator.
/
01191, 00000, "Failed to initialize the local OS authentication subsystem"
// *Cause: Initialization of the security subsystem failed during listener 
// startup or reload. The listener could not obtain system resources (memory,
// or file descriptors) needed for local OS authentication security mechanism.
// *Action: Make sure that system resources like shared memory and heap memory
// are available for listener to execute properly. For further details, turn
// on tracing and execute the operation again. If the error persists, contact
// Oracle Support Services.
/
01192, 00000, "Missing SID_LIST_ value left of equation for SID description in LISTENER.ORA"
// *Cause: SID description in LISTENER.ORA had an error in it.
// *Action: Make sure the lines of code in LISTENER.ORA containing SID_DESC or 
// SID begin with SID_LIST_<listener_name> on the left side of the equation.
// For example,
// SID_LIST_LISTENER =(SID_LIST=(SID_DESC=(SID_NAME=<sid>)(ORACLE_HOME=<oracle_home>)))
/
01193, 00000, "Listener cannot operate with specified secure transport"
// *Cause: Listener was configured with transport protocols which are either
// invalid or none of the secure transport protocols are present in listening
// addresses.
// *Action: Modify the existing listener configuration by specifying a valid
// tranport protocol in secure transport list. 
/
01194, 00000, "The listener command did not arrive in a secure transport"
// *Cause: Most of the listener administrative commands are only intended to 
// be issued in a secure transport, which are configured in 
// secure_control_ parameter. If the parameter is set, then the listener
// accepts administrative requests only on those secure transports.
// *Action: Make sure the command is issued using a transport specified 
// in secure transport list.
/
01200, 00000, "The listener must be suid root"
// *Cause:  The ownership privileges of the TNSLSNR executable are incorrect.
// *Action: Contact your DBA or system administrator to change the ownership
// of the file to be suid root and restart the listener. This action is
// necessary because the user that started the process should claim
// ownership.
// *Comment: This error is reported only on Trusted Oracle platforms.
/
01201, 00000, "Listener cannot find executable %s for SID %s"
// *Cause:  The executable for the Oracle dedicated server process cannot be
// found.
// *Action: Check the appropriate SID_DESC in LISTENER.ORA to make sure that
// the ORACLE_HOME component is pointing to a valid location. If this component
// is not set, then check the value of the ORACLE_HOME environment variable.
// *Comment: This error is reported only on UNIX platforms.
/
01202, 00000, "Missing the dba group (%s) specified by DBA_GROUP in SID_DESC"
// *Cause:  The dba group specified is missing from /ETC/GROUP.
// *Action: Check the DBA_GROUP parameter in the SID_DESC in LISTENER.ORA
// and verify it has a valid entry in /ETC/GROUP.
// *Comment: This error is reported only on UNIX platforms.
/
01203, 00000, "Missing the account (%s) specified by DEFAULT_USER_ACCOUNT in SID_DESC"
// *Cause:  The unprivileged OS account is missing from /etc/passwd.
// *Action: Check the DEFAULT_USER_ACCOUNT parameter in the SID_DESC in
// LISTENER.ORA and verify it has a valid entry in /etc/passwd. This is
// the account that the  Oracle shadow process will be started with if the
// the connecting client has database  privileges or does not exist on this
// machine.
// *Comment: This error is reported only on UNIX platforms.
/
01204, 00000, "Unprivileged account (%s) is in dba group (%s)"
// *Cause:  The unprivileged account has DBA privileges. The unprivileged
// account specified by DEFAULT_USER_ACCOUNT in the SID_DESC in
// LISTENER.ORA is a member of the dba group specified  by DBA_GROUP in
// SID_DESC. The unprivileged account cannot belong to the dba group
// because this would be a security violation with OPS$ logins.
// *Action: Remove the unprivileged account from the dba group.
// *Comment: This error is only reported on UNIX platforms.
/
01300, 00000, "\nERROR at %s\n"
// *Cause:  Listener logging message.
// *Action: None.
/
01301, 00000, "TNS error structure:"
// *Cause:  Listener logging message.
// *Action: None.
/
01302, 00000, "nr err code: %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01303, 00000, "ns main err code: %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01304, 00000, "ns secondary err code: %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01305, 00000, "nt main err code: %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01306, 00000, "nt secondary err code: %d"
// *Cause:  Listener logging message.
// *Action: None.
/
01307, 00000, "nt OS err code: %d"
// *Cause:  Listener logging message.
// *Action: None.
/

01400, 00000, "Instance \"%s\"\t\t has %d handlers."
// *Cause:  Control program status message.
// *Action: None.
/
01401, 00000, "Class: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01402, 00000, "TYPE: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01403, 00000, "Load: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01404, 00000, "Max Load: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01405, 00000, "Host: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01406, 00000, "ID: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01407, 00000, "Status: %s  Total handlers: %s  Relevant handlers: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01408, 00000, "Instance \"%s\", status %s, has %s handler(s) for this service..."
// *Cause:  Control program status message.
// *Action: None.
/
01409, 00000, "Instance \"%s\""
// *Cause:  Control program status message.
// *Action: None.
/

01410, 00000, "Service \"%s\"\t\thas %d instances."
// *Cause:  Control program status message.
// *Action: None.
/

01411, 00000, "Service \"%s\" has %d instance(s)."
// *Cause:  Control program status message.
// *Action: None.
/

01412, 00000, "Handler(s):"
// *Cause:  Control program status message.
// *Action: None.
/

01413, 00000, "\"%s\" established:%s refused:%s current:%s max:%s state:%s"
// *Cause:  Control program status message.
// *Action: None.
/

01414, 00000, "\"%s\", state %s, established %s, refused %s, current %s, max %s"
// *Cause:  Control program status message.
// *Action: None.
/

01415, 00000, "Listening Endpoints Summary...\n"
// *Cause:  Control program status message.
// *Action: None.
/

01416, 00000, "Process ID                %s\n"
// *Cause:  Control program status message.
// *Action: None.
/

01417, 00000, "\"%s\" established:%s refused:%s state:%s"
// *Cause:  Control program status message.
// *Action: None.
/

01418, 00000, "Proxy service \"%s\" has %d instance(s)."
// *Cause:  Control program status message.
// *Action: None.
/

01420, 00000, "Presentation: %s"
// *Cause:  Control program status message.
// *Action: None.
/
01421, 00000, "Session: %s"
// *Cause:  Control program status message.
// *Action: None.
/


01441, 00000, "Number of filtering rules currently in effect: %d"
// *Cause:  Control program status message
// *Action: None
01442, 00000, "No filtering rules currently in effect."
// *Cause:  Control program status message
// *Action: None


// NLS_DO_NOT_TRANSLATE [02020,02022]
02020, 00000, "set displaymode RAW | COMPAT | NORMAL | VERBOSE: output mode for lsnrctl display\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
02021, 00000, "DIRECT_HANDOFF can be either ON or OFF.\n"
// *Cause:  Invalid value for the LSNRCTL direct_handoff parameter.
// *Action: Specify one of ON or OFF.
// *Comment: This is a help message - do not translate.
/
02022, 00000, "show rules: Show rules that are currently in effect\n"
// *Cause:  Control program usage message.
// *Action: None.
// *Comment: This is a help message - do not translate.
/
/ --------SNSGUM:Connection Load Balancer Errors 2401-2500----------------
/
02401, 00000, "gbname %s too long, allowed %d characters"
// *Cause: gbname or domain name too long.
// *Action: Check the gbname parameter in listener.ora, shorten it.
/
02402, 00000, "Bad CLBGNAMES parameter in tnsnames.ora"
// *Cause: CLBGNAMES parameter in tnsnames.ora is bad.
// *Action: Check the CLBGNAMES parameter format and correct it. Make sure
//          that the tnsnames.ora file is there.
/
02403, 00000, "Bad alias %s or alias not present in tnsnames.ora"
// *Cause: An alias was expected in tnsnames.ora but was not found or was not
//         correctly formed.
// *Action: Check the tnsnames.ora for the alias and make sure it is correctly
//          formed.
/
02404, 00000, "Service %s contains no local handlers"
// *Cause: The listener found no suitable handler to redirect to.
// *Action: Make sure that there is at least one handler for this node.
/
02405, 00000, "GMS call failed, check GMS logs."
// *Cause: A GMS call made by the listener failed.
// *Action: Check if the GMS is up and running. See GMS-client trace files
//          for more information.
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ ----------------------- NA internal errors ------------------------------
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/ Reserved for NAtive service errors: 2501 - 3500
02501, 00000, "Authentication: no more roles"
// *Cause:  When a process attempted to retrieve a role from the authentication
//          service, no more were available.
// *Action: None. This error is used internally and occurs in the normal course
//          of events.
/
02502, 00000, "Authentication: unable to find initialization function"
// *Cause:  The native authentication service was unable to call the
//          initialization function for the specified service because
//          it does not exist.
// *Action: If this service adaptor came directly from Oracle, contact
//          Oracle Customer Support, as this error should never
//          happen. Otherwise, add an initialization function for the
//          service being used.
/
02503, 00000, "Parameter retrieval failed"
// *Cause:  The native service layer was unable to retrieve a parameter from a
//          configuration file.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02504, 00000, "Parameter count retrieval failed"
// *Cause:  The native service layer was unable to determine the number of
//          arguments given for a configuration parameter.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02505, 00000, "Authentication: null context pointer provided"
// *Cause:  The function nau_ini() was passed a null pointer as the pointer to
//          the context that it is supposed to use.
// *Action: Call nau_ini() with a pointer to a context structure.
/
02506, 00000, "Authentication: no type string"
// *Cause:  An authentication context structure does not contain a string that
//          describes the authentication service being used.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02507, 00000, "Encryption: algorithm not installed"
// *Cause:  After picking an algorithm, the server was unable to find
//          an index for it in its table of algorithms.  This should
//          be impossible because the algorithm was chosen
//          (indirectly) from that list.
// *Action: Not normally visible to the user.  For further details,
//          turn on tracing and reexecute the operation.  If error
//          persists, contact Oracle Customer Support.
/
02508, 00000, "Encryption: server negotiation response in error"
// *Cause:  The server's response in negotiation was in error.
// *Action: Not normally visible to the user.  For further details,
//          turn on tracing and reexecute the operation.  If error
//          persists, contact Oracle Customer Support.
/
02509, 00000, "Authentication: invalid process state"
// *Cause:  The state in which a process is running does not correspond to any
//          of the values which are valid.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02510, 00000, "Invalid numeric data type"
// *Cause:  The type of a piece of numeric data that was received does not
//          correspond to one of the valid values.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02511, 00000, "Invalid data type"
// *Cause:  The type of a piece of data that was received or to be transmitted
//          did not correspond to any of the correct values.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02512, 00000, "Invalid status received"
// *Cause:  A process received a value as a status flag which was unknown.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02513, 00000, "Requested data type does not match retrieved type"
// *Cause:  A service requested data whose type does not match that of the segment
//          which was sent from the other process.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02514, 00000, "Invalid packet received"
// *Cause:  A process received a data packet which was not meant for the native
//          services layer.
// *Action: If it is possible, enable tracing and attempt to reproduce the
//          problem.
//          In any event, contact Oracle Customer Support.
/
02515, 00000, "Encryption/crypto-checksumming: unknown control type"
// *Cause:  An encryption or crypto-checksumming algorithm "control"
//          function was called, but did not recognize the "type"
//          argument it was given.
// *Action: Not normally visible to the user.  For further details,
//          turn on tracing and reexecute the operation.  If error
//          persists, contact Oracle Customer Support.
/
02516, 00000, "No data available"
// *Cause:  A native service attempted to retrieve data but no data was
//          available to be received.
// *Action: The error is not normally visible as it usually is only used to
//          signal the end of a data stream. If the error becomes visible,
//          enable tracing to reproduce the problem and contact
//          Oracle Customer Support.
/
02517, 00000, "key smaller than requested size"
// *Cause:  The key returned by negotiation was smaller than
//          the size requested by some service (either encryption or
//          crypto-checksumming).
// *Action: The error is not normally visible.  If the error persists,
//          enable tracing to reproduce the problem and contact
//          Oracle Customer Support.
/
02518, 00000, "key negotiation error"
// *Cause:  An error occurred while the two sides of the connection
//          were negotiating an encryption or crypto-checksumming key.
// *Action: The error is not normally visible.  If the error persists,
//          enable tracing to reproduce the problem and contact
//          Oracle Customer Support.
/
02519, 00000, "no appropriate key-negotiation parameters"
// *Cause:  No appopriate key-negotiation parameters are available for
//          the key size requested either by encryption or by crypto-
//          checksumming.
// *Action: The error is not normally visible.  Enable tracing to
//          reproduce the problem and contact Oracle Customer
//          Support.
/
02520, 00000, "encryption/crypto-checksumming: no Diffie-Hellman seed"
// *Cause:  The "sqlnet.crypto_seed" parameter is missing from the
//          SQLNET.ORA parameters file for Oracle Advanced Security.
// *Action: Add this line to SQLNET.ORA:
//	      sqlnet.crypto_seed = "randomly-chosen text"
/
02521, 00000, "encryption/crypto-checksumming: Diffie-Hellman seed too small"
// *Cause:  The "sqlnet.crypto_seed" parameter in the SQLNET.ORA
//          parameter file for Oracle Net is too small.
// *Action: Add more randomly-chosen text to it.
/
02524, 00000, "Authentication: privilege check failed"
// *Cause:  An error occurred when the Oracle Advanced Security authentication service attempted
//          to verify that a user had a specific database privilege.
// *Action: This error should not happen normally. Enable tracing and attempt
//          to repeat the error. Contact Customer Support.
/
02525, 00000, "encryption/crypto-checksumming: self test failed"
// *Cause:  The Oracle Advanced Security encryption/crypto-checksumming service detected an error
//          while running tests on the active encryption or checksumming
//          algorithm.
// *Action: Contact Customer Support.
/
02526, 00000, "server proxy type does not match client type"
// *Cause:  The authentication type selected by the server does not match that
//          picked by the client.
// *Action: Contact Oracle Customer Support
/
///////////////////////////////////////////////////////////////////////////
/
/ 03501 - 03600   NSPING (not reportable to OSN) - NS ping utility
/
03501, 00000, "OK"
// *Cause:  The operation succeeded.
// *Action: No action necessary.
/
03502, 00000, "Insufficient arguments.  Usage:  tnsping <address> [<count>]"
// *Cause:  Some required command-line arguments are missing.
// *Action: Re-enter the command using the correct arguments.
/
03503, 00000, "Could not initialize NL"
// *Cause:  The network library could not be initialized.
// *Action: This is an internal error which should not normally be visible.
//          Ensure that memory is available to run the application and that
//          there are no other operating system problems, and then attempt
//          the command again.
/
03504, 00000, "Service name too long"
// *Cause:  The service name you are attempting to ping is too long.
// *Action: Re-enter the command using the correct service name.
/
03505, 00000, "Failed to resolve name"
// *Cause:  The service name you provided could not be found in TNSNAMES.ORA,
//          an Oracle Names server, or a native naming service.
// *Action: Verify that you entered the service name correctly.  You may need
//          to ensure that the name was entered correctly into the network
//          configuration.
/
03506, 00000, "Failed to create address binding"
// *Cause:  The TNSPING utility found the requested address or service name, 
//          but received an internal error when trying to use it.
// *Action: This is an internal error which should not normally be visible.
//          Ensure that memory is available to run the application and that
//          there are no other operating system problems, and then attempt
//          the command again.
/
03507, 00000, "Failure looking for ADDRESS keyword"
// *Cause:  The TNS address did not contain an ADDRESS keyword.
// *Action: If you entered the TNS address on the command line, be sure that
//          the syntax is correct.  If you entered a service name on the 
//          command line, the address contains the wrong information.  You 
//          should verify that the information was entered correctly.
/
03508, 00000, "Failed to create address string"
// *Cause:  The TNSPING utility received an internal error when generating
//          an address.
// *Action: This is an internal error which should not normally be visible.
//          Ensure that memory is available to run the application and that
//          there are no other operating system problems, and then attempt
//          the command again.
/
03509, 00000, "OK (%d msec)"
// *Cause:  The operation succeeded, in this amount of time.
// *Action: No action necessary.
/
03510, 00000, "Failed due to I/O error"
// *Cause:  An I/O operation failed, perhaps due to a resource failure
//          or premature window termination.
// *Action: This is an internal error which should not normally be visible.
//          Do not close the TNSPING window before all I/O operations have
//          completed.
/
03511, 00000, "Used parameter files:\n%s\n"
// *Cause:  Prints out the path of the parameter files(sqlnet.ora,tnsnames.ora)
//          used in the process of resolving the NAME.
// *Action: NONE 
/
03512, 00000, "Used %s adapter to resolve the alias\n"
// *Cause:  Prints out the name of the adapter which resolved the TNS alias.
// *Action: NONE
/
///////////////////////////////////////////////////////////////////////////
/
/ 03601 - 03700   NSUT (not reportable to OSN) - NS trace route utility
/
03601, 00000, "Failed in route information collection"
// *Cause:  The route could either not connect, or encountered an
//          unsupported version of Oracle Net.
// *Action: Check if Oracle Net along all nodes is version 2.3 or
//          greater.
/
03602, 00000, "Insufficient arguments.  Usage:  trcroute <address> "
// *Cause:  Some required command-line arguments are missing.
// *Action: Re-enter the command using the correct arguments.
/
03603, 00000, "Encountered a node with a version eariler than SQL*Net 2.3"
// *Cause:  Versions of SQL*Net before 2.3 do not support
//          trcroute.
// *Action: Find the node that isn't responding to trcroute.
/
///////////////////////////////////////////////////////////////////////////
/
/ 04001 - 04200 NFP errors
/
///////////////////////////////////////////////////////////////////////////
/
/ The range 04001 to 04200 should be reserved for the Connection Manager. 
/ The messages will include status messages
/ as well as error messages.
/
/ Start with error messages first.
/
// UI[04001,04200]
/
04001, 00000, "%s"
// *Cause:   CMCTL general message.
// *Action:  None.
04002, 00000, "The command completed successfully."
// *Cause:   Not applicable.
// *Action:  None
04003, 00000, "Syntax Error."
// *Cause:   The command issued has a wrong syntax.
// *Action:  Check for the command issue syntax, and correct the problem.
04004, 00000, "Unable to encrypt the supplied password."
// *Cause:   The password that was supplied to the ADMINISTER command
//           could not be encrypted.
// *Action:  Change the password to something acceptable. See Oracle Net
//           Services documentation for valid password values.
04005, 00000, "Unable to resolve address for %s."
// *Cause:   The alias name supplied with the ADMINISTER command could not
//           be resolved to an Oracle Connection Manager address.
// *Action:  Check if your an entry for the alias is present in either 
//           CMAN.ORA file or in TNSNAMES.ORA file.
04006, 00000, "Invalid password"
// *Cause:   The password given with the ADMINISTER command could not
//           be verified by the Oracle Connection Manager instance.
// *Action:  Retry with the correct password.
04007, 00000, "Internal error %d."
// *Cause:   Not normally visible to the user.
// *Action:  If error persists, contact Oracle Support Services.
04008, 00000, "%-25s | %5s"
// *Cause:   String parameter value.
// *Action:  None.
04009, 00000, "%-25s | %5d"
// *Cause:   Integer parameter value.
// *Action:  None.
04010, 00000, "Command cannot be issued before the ADMINISTER command."
// *Cause:   A command was issued before administering the Oracle 
//           Connection Manager instance.
// *Action:  Enter the ADMINISTER command before retrying this command.
04011, 00000, "Oracle Connection Manager instance not yet started."
// *Cause:   A command was issued when Oracle Connection Manager was not
//           yet started or already shutdown.
// *Action:  Start Oracle Connection Manager.
04012, 00000, "Unable to start Oracle Connection Manager instance."
// *Cause:   CMCTL was unable to start the Oracle Connection Manager
//           instance. Some of the possible reasons include: cmadmin not
//           present in ORACLE_HOME/bin, Invalid parameter in configuration
//           repository, wrong parameter values, or log directory not present.
// *Action:  1. Check whether log directory is present, and is writable.
//              Log directory can be found at ORACLE_HOME/network/log, or
//              as specified by the LOG_DIRECTORY parameter in CMAN.ORA.
//           2. Turn on logging or tracing to get more information 
//              about this error.
//           3. Correct any parameter errors (or mismatched paranthesis), 
//              and retry starting Oracle Connection Manager.
//           4. If the problem persists, contact Oracle Support Services.
04013, 00000, "CMCTL timed out waiting for Oracle Connection Manager to start"
// *Cause:   Oracle Connection Manager internal registrations have not
//           been completed.
// *Action:  Turn on logging or tracing to get more information about this 
//           error. If the problem persists, contact Oracle Support 
//           Services.
04014, 00000, "Current instance %s is already started"
// *Cause:   An ADMINISTER command was issued to administer an Oracle
//           Connection Manager instance that is already started.
// *Action:  None
04015, 00000, "Current instance %s is not yet started"
// *Cause:   An ADMINISTER command was issued to an instance that has
//           not yet been started.
// *Action:  None
04016, 00000, "Connecting to %s"
// *Cause:   CMCTL is connecting to the the specified Oracle Connection
//           Manager address.
// *Action:  None
04017, 00000, "Please wait. Shutdown in progress."
// *Cause:   A command which cannot be used while Oracle Connection Manager
//           is shutting down was issued.
// *Action:  Wait for some time before retrying the command.
04018, 00000, "Instance already started"
// *Cause:   The STARTUP command was issued to an instance which was already
//           started.
// *Action:  None
04019, 00000, "Starting Oracle Connection Manager instance %s. Please wait..."
// *Cause:   The STARTUP command was issued for an Oracle Connection 
//           Manager instance. CMCTL is waiting for the instance to start.
// *Action:  None
04020, 00000, "CMCTL Version: %u.%u.%u.%u.%u"
// *Cause:   None.
// *Action:  None.
04021, 00000, "The SET command is unsuccessful for parameter %s."
// *Cause:   The value set for the parameter was out of range.
// *Action:  See Oracle Net Services documentation for value ranges for
//           the parameters.
04022, 00000, "%s parameter %s set to %s."
// *Cause:   Parameter value was successfully set.
// *Action:  None
04023, 00000, "Command failed."
// *Cause:   The command issued failed to complete successfully.
// *Action:  Retry command. If problem persists, contact Oracle
//           Support Services.
04024, 00000, "Status of the Instance"
04025, 00000, "----------------------"
04026, 00000, "Instance name             %s"
04027, 00000, "Version                   %s"
04028, 00000, "Start date                %s"
04029, 00000, "Uptime                    %u days %u hr. %u min. %u sec"
04030, 00000, "Num of gateways started   %u"
04031, 00000, "Average Load level        %u"
04032, 00000, "Log Level                 %s"
04033, 00000, "Trace Level               %s"
04034, 00000, "Instance Config file      %s"
04035, 00000, "Instance Log directory    %s"
04036, 00000, "Instance Trace directory  %s"
04037, 00000, "Connections refer to %s."
// *Cause:   The ADMINISTER command resolved to the address in the specified
//           message string.
// *Action:  None
04038, 00000, "Gateway ID                     %u"
04039, 00000, "Gateway state                  %s"
04040, 00000, "Number of active connections   %u"
04041, 00000, "Peak active connections        %u"
04042, 00000, "Total connections              %u"
04043, 00000, "Total connections refused      %u"
04044, 00000, "Specified gateways do not exist."
// *Cause:   One or more specified gateway IDs do not exist.
// *Action:  Specify correct gateway IDs.
04045, 00000, "Invalid specification of time"
// *Cause:   The time specified with the GT (greater than) option was invalid.
// *Action:  Check Oracle Net Services documentation for valid time
//           specification.
04046, 00000, "Invalid specification for source"
// *Cause:   The source specified with the FROM option was invalid.
// *Action:  Check Oracle Net Services documentation for valid 
//           source specification.
04047, 00000, "Invalid specification for destination"
// *Cause:   The destination specified with the TO option was invalid.
// *Action:  Check Oracle Net Services documentation for valid destination
//           specification.
04048, 00000, "Specified service does not exist."
// *Cause:   The service specified with the FOR option did not exist.
// *Action:  None
04049, 00000, "Specified connections do not exist"
// *Cause:   One or more connection IDs do not exist.
// *Action:  None
04050, 00000, "Invalid specification for gateway ID."
// *Cause:   The gateway ID specified is invalid.
// *Action:  Check Oracle Net Services documentation for a valid gateway 
//           ID specification.
04051, 00000, "Connection ID                 %u"
04052, 00000, "Gateway ID                    %u"
04053, 00000, "Source                        %s"
04054, 00000, "Destination                   %s"
04055, 00000, "Service                       %s"
04056, 00000, "State                         %s"
04057, 00000, "Idle time                     %u"
04058, 00000, "Connected time                %u"
04059, 00000, "Bytes Received [IN]           %u"
04060, 00000, "Bytes Sent     [IN]           %u"
04061, 00000, "Bytes Received [OUT]          %u"
04062, 00000, "Bytes Sent     [OUT]          %u"
04063, 00000, "Remote administration disabled in the Oracle Connection Manager instance."
// *Cause:   CMCTL attempted to connect to a remote Oracle Connection
//           Manager instance in which remote administration was disabled.
// *Action:  Set parameter remote_admin=on in the remote instance before
//           starting it.
04064, 00000, "The number of CMCTL sessions exceeds MAX_CMCTL_SESSIONS."
// *Cause:   The Oracle Connection Manager instance already has 
//           MAX_CMCTL_SESSIONS number of CMCTLs connected to it. 
// *Action:  Use an already connected CMCTL, or, use a higher value for
//           the parameter MAX_CMCTL_SESSIONS in the CMAN.ORA file.
04065, 00000, "The number of remote CMCTL sessions exceeds (MAX_CMCTL_SESSIONS-1)"
// *Cause:   The Oracle Connection Manager instance already has 
//           (MAX_CMCTL_SESSIONS-1) number of remote CMCTL sessions connected
//           to it.
// *Action:  Use an already connected CMCTL, or, use a higher value for
//           the parameter MAX_CMCTL_SESSIONS in the CMAN.ORA file.
04066, 00000, "The following log events can be enabled or disabled:"
// *Cause:   None
// *Action:  None
04067, 00000, "Number of connections: %u."
// * Cause:  Either no information qualifier (COUNT/DETAIL) was present
//           in SHOW CONNECTIONS command, or, COUNT was used as the
//           information qualifier.
// * Action: None
04068, 00000, "Cannot start an Oracle Connection Manager instance remotely."
// *Cause:   CMCTL was used to start Oracle Connection Manager instance
//           in a remote host.
// *Action:  Use a local CMCTL to start the Oracle Connection Manager.
04069, 00000, "Sleeping for %u seconds..."
// *Cause:   CMCTL is idle for specified seconds. This feature is only
//           provided for testing purposes.
// *Action:  None
04070, 00000, "Cannot administer a remote Oracle Connection Manager instance which is not yet started."
// *Cause:   An attempt was made to administer a remote Oracle Connection 
//           Manager instance which is not yet started.
// *Action:  Use a local CMCTL session to start the Oracle Connection 
//           Manager instance before trying to administer it remotely.
04071, 00000, "Connections closed successfully. Number closed: %d."
// *Cause:   The specified connections were closed successfully.
// *Action:  None
04072, 00000, "Unable to suspend atleast one of the gateways."
// *Cause:   CMCTL was unable to suspend one or more gateways. Possible
//           reason could be suspending a gateway that was already suspended
//           or suspending a gateway that was not present.
// *Action:  Turn on tracing and logging, retry operation. Information in 
//           the log files would help.
04073, 00000, "Passwords do not match."
// *Cause:   The new password and its confirmation do not match
// *Action:  Use SET PASSWORD again.
04074, 00000, "Invalid value for the parameter %s."
// *Cause:   The parameter value set using the SET command is invalid.
// *Action:  See Oracle Net Services documentation for the valid values
//           of the parameter.
04075, 00000, "Cannot use ADMINISTER directly from the command line."
// *Cause:   ADMINISTER can only be issued from the CMCTL> prompt.
// *Action:  Use the -c option with any command instead of ADMINISTER. 
04076, 00000, "Invalid specification for state."
// *Cause:   The state specified with "in" option is invalid.
// *Action:  Check Oracle Net Services documentation for valid state
//           specification.
04077, 00000, "WARNING: No password set for the Oracle Connection Manager instance."
// *Cause:   A connection to the Oracle Connection Manager instance was
//           made with no password from the user.
// *Action:  Ignore the warning if the Oracle Connection Manager is
//           secure enough. Otherwise, use SET PASSWORD command to set
//           a new password for the instance.
04078, 00000, "Unable to resume atleast one of the gateways."
// *Cause:   CMCTL was unable to resume one or more gateways. Possible
//           reason could be resuming a gateway that was ready for connections,
//           or resuming a gateway that was not present.
// *Action:  Turn on tracing and logging, retry operation. Information in 
//           the log files would help.
04079, 00000, "Cannot administer Oracle Connection Manager with no CMAN.ORA, and port = %d."
// *Cause:   CMAN.ORA is not present or address not configured in CMAN.ORA,
//           and the net service name in the TNSNAMES.ORA contains a 
//           nondefault Oracle Connection Manager port.
// *Action:  Either change the TNSNAMES.ORA entry to use the default port,
//           or configure the CMAN.ORA file with the Oracle Connection
//           Manager's address.
04080, 00000, "Failed to reload"
// *Cause:   Oracle Connection Manager failed to reload the new configuration
//           due to errors in the configuration file.
// *Action:  Set log_level to support and retry operation. Error encountered
//           will be logged in the log file of CMADMIN.
04081, 00000, "Event groups:"
// *Cause:   None
// *Action:  None
04082, 00000, "%s event %s set to %s."
// *Cause:   Event value was successfully set.
// *Action:  None
04083, 00000, "Failed to save password"
// *Cause:   Oracle Connection Manager failed to save the password in the 
//           configuration file.
// *Action:  Check for the permissions on the configuration file. The
//           file should have WRITE permissions.
04084, 00000, "WARNING: Non-reloadable parameters have retained their values."
// *Cause:   Values of non-reloadable parameters were changed, or, one
//           or more non-reloadable parameters having non-default values
//           were added to the parameter file.
// *Action:  See Oracle Net Services documentation for a list of 
//           non-reloadable parameters.
04085, 00000, "Password not changed since last save."
// *Cause:   Password has not been changed since it was last saved.
// *Action:  None
04086, 00000, "Invalid value for the event %s."
// *Cause:   The event value set using the SET EVENT command is invalid.
// *Action:  See Oracle Net Services documentation for the valid values
//           of the event.
04087, 00000, "Unable to shutdown atleast one of the gateways."
// *Cause:   CMCTL was unable to shutdown one or more gateways. Possible
//           reason could be shutting down a gateway that was not present.
// *Action:  Turn on tracing and logging, retry operation. Information in 
//           the log files would help.
04088, 00000, "Unable to close atleast one of the connections."
// *Cause:   CMCTL was unable to close one or more connections. Possible
//           reason could be closing a connection that was not present.
// *Action:  Turn on tracing and logging, retry operation. Information in 
//           the log files would help.
04089, 00000, "Alias name too long."
// *Cause:   User entered an alias name that exceeded 64 characters.
// *Action:  Retry with a shorter alias name. Alias names have to be less 
//           than 65 characters.
/
/ --------------------- CMMIGR Messages -------------------------
/
04140, 00000, "Migration completed successfully."
// *Cause:   CMMIGR has successfully completed the migration of the old
//           CMAN.ORA file to the new format.
// *Action:  None
04141, 00000, "Unable to find CMAN.ORA file."
// *Cause:   CMMIGR was not able to find CMAN.ORA file.
// *Action:  Check whether CMAN.ORA file is present in $TNS_NAME/admin, 
//           or in $ORACLE_HOME/network/admin, or in the path specified in 
//           the command line.
04142, 00000, "CMAN.ORA file has an invalid format."
// *Cause:   CMMIGR was unable to recognize the format of CMAN.ORA file.
// *Action:  Check for the syntax errors in CMAN.ORA file, and correct them.
04143, 00000, "Unable to write the new CMAN.ORA file."
// *Cause:   CMMIGR was unable to create the new CMAN.ORA file due to 
//           insufficient perimissions.
// *Action:  Set WRITE permissions to the directory in which CMAN.ORA file 
//           is to be written.
04144, 00000, "Nothing to migrate"
// *Cause:   CMMIGR did not find anything in the old CMAN.ORA file 
//           that has an equivalent in the new format.
// *Action:  None
/
/ ----------------- Help strings in CMCTL 10i -------------------
/
04150, 00000, "close connections {[in <state>][gt <[[hh:]mm:]ss>][from <source>][to <destination>][for <service>][using <gw_id>]} | [<id_list>] - Closes selected connections"
04151, 00000, "show connections [detail | count] {[in <state>][gt <[[hh:]mm:]ss>][from <source>][to <destination>][for <service>][using <gw_id>]} | [<id_list>] - Shows statistics of selected connections"
04152, 00000, "show gateways [<id_list>] - Shows statistics of selected gateways"
04153, 00000, "reload - Reload parameters and rules from the configuration repository"
04154, 00000, ""
04155, 00000, "resume gateways [<id_list>] - Resumes the gateways"
04156, 00000, "suspend gateways [<id_list>] - Suspends the gateways"
04157, 00000, "administer [<cman instance>] [using <password>] - Sets up a context for administering the given Oracle Connection Manager instance"
04158, 00000, "set <parameter> <value> - Sets the value for the said parameter in the Oracle Connection Manager instance presently being administered"
04159, 00000, "exit - Quits CMCTL"
04160, 00000, ""
04161, 00000, ""
04162, 00000, "show parameters - Shows the present values of the parameters"
04163, 00000, "show rules - Shows the list of rules currently in effect"
04164, 00000, ""
04165, 00000, "shutdown [gateways [<id_list>]] [normal | abort] - Shutsdown the administered Oracle Connection Manager instance / specified gateways"
04166, 00000, "startup - Starts the administered Oracle Connection Manager instance"
04167, 00000, "show status - Shows the status of the Oracle Connection Manager instance"
04168, 00000, ""
04169, 00000, ""
04170, 00000, ""
04171, 00000, "show version - Shows the version of the Oracle Connection Manager being administered"
04172, 00000, "quit - Quits CMCTL"
04173, 00000, "show defaults - Shows the default values of the parameters"
04174, 00000, "sleep <seconds> - Sleeps for the said seconds (does nothing for the said seconds)"
04175, 00000, "set password - Sets the password for administering the Oracle Connection Manager"
04176, 00000, "show services - Shows a list of services currently registered with the Oracle Connection Manager"
04177, 00000, "show all - Shows parameters and rules currently in effect"
04178, 00000, "show events - Shows events that are currently turned on"
04179, 00000, "set event <name> <on/off> - Sets specified event on or off"
04180, 00000, "save_passwd - Saves password in the configuration file"

/
///////////////////////////////////////////////////////////////////////////
/
/ 04201 - 04300 NU errors
/
///////////////////////////////////////////////////////////////////////////
/
/ The range 04201 to 04300 should be reserved for the NU component. 
/ The messages will include status messages as well as error messages.
/
04201, 00000, "Trace Assistant Usage ERROR: Missing File name\n"
// *Cause:   Trace file name argument is missing 
// *Action:  Put the trace file name as the last command line argument for
//           for this tool.
/
04202, 00000, "Trace Assistant Usage ERROR: Not enough arguments \n"
// *Cause:   The <file name> and/or the <options> arguments are missing
// *Action:  Put the right number of command line arguments.
/
04203, 00000, "Trace Assistant Usage ERROR: Invalid options \n"
// *Cause:   The options provided are not valid
// *Action:  Check the valid options for this tool.
/
04204, 00000, "Trace Assistant Internal ERROR: Couldn't Open trace file\n"
// *Cause:   The trace file name given doesn't exist or it is not
//           accessible for this user.
// *Action:  Check the spelling, and permissions of the trace file.
/
04205, 00000, "Trace Assistant Internal ERROR: Memory\n"
// *Cause:   Possible memory problem
// *Action:  Verify the amount of available memory on the system.
/
04206, 00000, "Trace Assistant Internal ERROR: Packet Type\n"
// *Cause:   The packet type read by trcAsst is not valid.
// *Action:  Verify that your trace file is not corrupted. If trace file
//           looks OK, with not strange characters in it, contact World
//           Wide Support and provide trace file to them.
/
04207, 00000, "Trace Assistant Internal ERROR: Packet Length\n"
// *Cause:   The packet being decode is corrupted.
// *Action:  Verify that your trace file is not corrupted. If trace file
//           looks OK, with not strange characters in it, contact World
//           Wide Support and provide trace file to them.
/
04208, 00000, "Trace Assistant Internal ERROR: Fatal\n"
// *Cause:   Fatal internal error
// *Action:  Contact World Wide Support.
/
04209, 00000, "Trace Assistant Internal ERROR: Type Error \n"
// *Cause:   Internal type error,
// *Action:  Contact World Wide Support.
/
04210, 00000, "Trace Assistant Internal ERROR: End of File\n"
// *Cause:   Reaching End of File to soon. Not able to decode trace file.
//           Your trace file appears to be truncated.
// *Action:  Generate another trace file. This trace file can not be decoded.
/
04211, 00000, "Trace Assistant Internal ERROR: CORE\n"
// *Cause:   Internal System Error
// *Action:  Contact World Wide Support.
/
04212, 00000, "Trace Assistant Internal ERROR: NACOM Type Error \n"
// *Cause:   Not able to decode Network Authentication information
// *Action:  Contact World Wide Support.
/

04231, 00000, "Trace Assistant WARNING: Assuming Oracle trace format\n"
// *Cause:   This trace file may not be a Network trace file. The default
//           format (Oracle Trace) will be assumed.
// *Action:  None.
/
04232, 00000, "Trace Assistant WARNING: Not retrieving all rows \n"
// *Cause:   Trace Assitante won't retrieve all the rows data.
// *Action:  None.
/
04233, 00000, "Trace Assistant WARNING: Going beyond Packet length\n"
// *Cause:   Trying to read beyond packet length. The trace file may be
//           corrupted
// *Action:  None.
/
04234, 00000, "Trace Assistant WARNING: won't decode TTC \n"
// *Cause:   Trace assistant does not have enough information to decode TTC
//           data. This maybe an old trace file or from a platform that
//           trace assistant does not understand. 
// *Action:  None.
/
04235, 00000, "Trace Assistant WARNING: Unknown TTC protocol\n"
// *Cause:   Trace Assistant has reached a point in which the TTC protocol
//           can not be understood.
// *Action:  None.
/
/
/
///////////////////////////////////////////////////////////////////////////
/ 04301 - 06000   Reserved for Oracle Network Java Products.
///////////////////////////////////////////////////////////////////////////
/
/
/
/
///////////////////////////////////////////////////////////////////////////
/
/ ---------------------------- unassigned ---------------------------------
/
///////////////////////////////////////////////////////////////////////////
/ Copyright (c) 1991, 1996, 1997, 2001 by the Oracle Corporation.  All rights reserved.
/
/
/ $Header: net12150.msg 06-dec-2002.07:12:56 mclose Exp $
/
/
/ NAME
/   net12150.msg - Oracle Net external message file starting from 12150 -
/   U.S. english version
/
/
/ FUNCTION
/   Network error message file, American English version.
/
/
/ NOTES
/       Only external errors are to be put into this file. Internal
/       messages are to put into netius.msg.
/
/       This file, along with netius.msg and net12500.msg, forms tnsus.msg. As a
/       result, the errors in this file may not overlap with the errors in
/       those files. Otherwise, errors will result when generating tnsus.msb.
/
/       Message text should be limited to a maximum of 76 characters.
/       Messages containing embedded % directives should not overrun
/       the 76 character limit unless they signal unusual errors
/       which do not occur as part of user applications.  For example,
/       startup errors and system dependent errors can probably get
/       away with longer message text.
/
/
/       '/' at beginning-of-line for comments.
/       '//' at beginning-of-line for *Cause: and *Action: fields.
/
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/////////////////////////// Please maintain this map //////////////////////
/
// 00001 - 04200  See netius.msg
/       .
/       .
/ 12150 - 12195	  Reserved for OSN (Not to be used by TNS)
/ 12196 - 12285   NR errors reportable by OSN (returned by nricall())
/ 12286 - 12499   ---(Reserved)---
/ 12500 - 12699   See net12500.msg
/       .
/       .
/       .
/
/////////////////////////// Please maintain this map //////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/
/
/
/ OWNER
/   Network and Management Products - Server Technologies
/
/ MODIFIED
/    cozhang    10/30/02 - Modify msg text 12170 to include STO and RTO.
/    mclose     10/01/02 - Improve key error messages
/    cozhang    03/07/02 - Change CONNECT_TIMEOUT to INBOUND_CONNECT_TIMEOUT.
/    cozhang    12/12/01 - Add message for connect time-out (12170 NIQECTO).
/    bnanjund   04/16/01 - 1714563_bugfix
/    tmlee      08/06/97 - modify 12204
/    rwessman   03/16/97 - split from netus.msg to correct bug in building
/                          oraus.msg.
/
12150, 00000, "TNS:unable to send data"
// *Cause:  Unable to send data. Connection probably disconnected.
// *Action: Reestablish connection. If the error is persistent, turn
// on tracing and reexecute the operation.
/
12151, 00000, "TNS:received bad packet type from network layer"
// *Cause:  Internal error.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Worldwide Customer Support.
/
12152, 00000, "TNS:unable to send break message"
// *Cause:  Unable to send break message. Connection probably disconnected.
// *Action: Reestablish connection. If the error is persistent, turn
// on tracing and reexecute the operation.
/
12153, 00000, "TNS:not connected"
// *Cause:  Not currently connected to a remote host.
// *Action: Reestablish connection.
/
12154, 00000, "TNS:could not resolve the connect identifier specified"
// *Cause:  A connection to a database or other service was requested using
// a connect identifier, and the connect identifier specified could not
// be resolved into a connect descriptor using one of the naming methods
// configured. For example, if the type of connect identifier used was a
// net service name then the net service name could not be found in a 
// naming method repository, or the repository could not be
// located or reached.
// *Action:
//   - If you are using local naming (TNSNAMES.ORA file):
//      - Make sure that "TNSNAMES" is listed as one of the values of the
//        NAMES.DIRECTORY_PATH parameter in the Oracle Net profile
//        (SQLNET.ORA)
//      - Verify that a TNSNAMES.ORA file exists and is in the proper
//        directory and is accessible.
//      - Check that the net service name used as the connect identifier
//        exists in the TNSNAMES.ORA file.
//      - Make sure there are no syntax errors anywhere in the TNSNAMES.ORA
//        file.  Look for unmatched parentheses or stray characters. Errors
//        in a TNSNAMES.ORA file may make it unusable.
//   - If you are using directory naming:
//      - Verify that "LDAP" is listed as one of the values of the
//        NAMES.DIRETORY_PATH parameter in the Oracle Net profile
//        (SQLNET.ORA).
//      - Verify that the LDAP directory server is up and that it is
//        accessible.
//      - Verify that the net service name or database name used as the
//        connect identifier is configured in the directory.
//      - Verify that the default context being used is correct by
//        specifying a fully qualified net service name or a full LDAP DN
//        as the connect identifier
//   - If you are using easy connect naming:
//      - Verify that "EZCONNECT" is listed as one of the values of the
//        NAMES.DIRETORY_PATH parameter in the Oracle Net profile
//        (SQLNET.ORA).
//      - Make sure the host, port and service name specified
//        are correct.
//      - Try enclosing the connect identifier in quote marks.
// 
//   See the Oracle Net Services Administrators Guide or the Oracle
//   operating system specific guide for more information on naming.
/
12155, 00000, "TNS:received bad datatype in NSWMARKER packet"
// *Cause:  Internal error during break handling.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Worldwide Customer Support.
/
12156, 00000, "TNS:tried to reset line from incorrect state"
// *Cause:  Internal error during break handling.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Worldwide Customer Support.
/
12157, 00000, "TNS:internal network communication error"
// *Cause:  Internal error during network communication.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Worldwide Customer Support.
/
12158, 00000, "TNS:could not initialize parameter subsystem"
// *Cause:  Unable to locate parameter file.
// *Action: Verify that a valid parameter file exists, and is readable.
/
12159, 00000, "TNS:trace file not writeable"
// *Cause:  The trace file to be generated is not writeable by this user.
// *Action: If the user does not have write permissions in the directory
// to which the trace file will be written, contact an administrator to
// get the proper permissions or set the TRACE_DIRECTORY_CLIENT
// parameter in the net profile (SQLNET.ORA file) to a directory the
// user can write to.
/
12160, 00000, "TNS:internal error: Bad error number"
// *Cause:  Corrupt error reporting subsystem.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Worldwide Customer Support.
/
12161, 00000, "TNS:internal error: partial data received"
// *Cause:  The connection may be terminated.
// *Action: Reconnect and try again. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Worldwide Customer Support.
/
12162, 00000, "TNS:net service name is incorrectly specified"
// *Cause:  The connect descriptor corresponding to the net service name in
// TNSNAMES.ORA or in the directory server (Oracle Internet Directory) is
// incorrectly specified.
// *Action: If using local naming make sure there are no syntax errors in
// the corresponding connect descriptor in the TNSNAMES.ORA file. If using
// directory naming check the information provided through the administration
// used for directory naming.
/
12163, 00000, "TNS:connect descriptor is too long"
// *Cause:  The connect descriptor corresponding to the net service name
// specified as the connect identifier is too long. The maximum length for
// a connect descriptor is 512 bytes and this limit has been exceeded.
// *Action: Check the net service name's connect descriptor in the local
// naming file (TNSNAMES.ORA) or in the directory server (Oracle Internet
// Directory). Use a smaller connect descriptor. If this is not possible,
// contact Worldwide Customer Support.
/
12164, 00000, "TNS:Sqlnet.fdf file not present"
// *Cause:  The sqlnet.fdf file doesn't exist in $ORACLE_HOME/network/admin.
// *Action: The sqlnet.fdf file is required for Oracle Tracing to occur.
// Either install the sqlnet.fdf file in $ORACLE_HOME/network/admin or
// turn off tracing in your ORA file.
/
12165, 00000, "TNS:Trying to write trace file into swap space."
// *Cause:  Oracle Trace doesn't allow writing trace information into your
// swap space.
// *Action: Oracle Trace cannot write trace information into swap space
// so either disable tracing or redirect trace files to be written to another
// area of your disk.
/
12166, 00000, "TNS:Client can not connect to HO agent."
// *Cause:  NVstring contained DESCRIPTION/HO.
// *Action: Call HO agent from integrating server.
/
12168, 00000, "TNS:Unable to contact LDAP Directory Server"
// *Cause:  Cannot contact LDAP directory server to get Oracle Net configuration.
// *Action: Verify that the directory server is up and accessible from the network.
//          Verify that directory access configuration is correct.  For more
//          information see the Oracle Internet Directory Administrators Guide or
//          the Oracle Net Administrators Guide.
/
12169, 00000, "TNS:Net service name given as connect identifier is too long"
// *Cause: The net service name you are attempting to resolve is too long.
// *Action: The maximum length of a net service name is 255 bytes; this limit
//          has been exceeded. Use a smaller net service name. If this
//          is not possible, contact Worldwide Customer Support.
/
12170, 00000, "TNS:Connect timeout occurred"
// *Cause:  The server shut down because connection establishment or
// communication with a client failed to complete within the allotted time
// interval. This may be a result of network or system delays; or this may
// indicate that a malicious client is trying to cause a Denial of Service
// attack on the server.
// *Action: If the error occurred because of a slow network or system,
// reconfigure one or all of the parameters SQLNET.INBOUND_CONNECT_TIMEOUT,
// SQLNET.SEND_TIMEOUT, SQLNET.RECV_TIMEOUT in sqlnet.ora to larger values.
// If a malicious client is suspected, use the address in sqlnet.log to
// identify the source and restrict access. Note that logged addresses may
// not be reliable as they can be forged (e.g. in TCP/IP).
/
12171, 00000, "TNS:could not resolve connect identifier: %s"
// *Cause:  A connection to a database or other service was requested using
// a connect identifier, and the connect identifier specified could not
// be resolved into a connect descriptor using one of the naming methods
// configured. For example, if the type of connect identifier used was a
// net service name then the net service name could not be found in a
// naming method repository, or the repository could not be
// located or reached.
// *Action:
//   - If you are using local naming (TNSNAMES.ORA file):
//      - Make sure that "TNSNAMES" is listed as one of the values of the
//        NAMES.DIRECTORY_PATH parameter in the Oracle Net profile
//        (SQLNET.ORA)
//      - Verify that a TNSNAMES.ORA file exists and is in the proper
//        directory and is accessible.
//      - Check that the net service name used as the connect identifier
//        exists in the TNSNAMES.ORA file.
//      - Make sure there are no syntax errors anywhere in the TNSNAMES.ORA
//        file.  Look for unmatched parentheses or stray characters. Errors
//        in a TNSNAMES.ORA file may make it unusable.
//   - If you are using directory naming:
//      - Verify that "LDAP" is listed as one of the values of the
//        NAMES.DIRETORY_PATH parameter in the Oracle Net profile
//        (SQLNET.ORA).
//      - Verify that the LDAP directory server is up and that it is
//        accessible.
//      - Verify that the net service name or database name used as the
//        connect identifier is configured in the directory.
//      - Verify that the default context being used is correct by
//        specifying a fully qualified net service name or a full LDAP DN
//        as the connect identifier
//   - If you are using easy connect naming:
//      - Verify that "EZCONNECT" is listed as one of the values of the
//        NAMES.DIRETORY_PATH parameter in the Oracle Net profile
//        (SQLNET.ORA).
//      - Make sure the host, port and service name specified
//        are correct.
//      - Try enclosing the connect identifier in quote marks.
//
//   See the Oracle Net Services Administrators Guide or the Oracle
//   operating system specific guide for more information on naming.
/
/ This line is an OSN Magic Cookie. Don't eat it. Last OSN error in 2.0.9.
/
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ 12196 - 12285 NR errors reportable to OSN.
/
12196, 00000, "TNS:received an error from TNS"
// *Cause:  The navigation layer received an error from TNS.
// *Action: See the error log file for the specific TNS error.
/
12197, 00000, "TNS:keyword-value resolution error"
// *Cause:  The navigation layer received an error while trying to look up a
//  value for a keyword.
// *Action: Check the syntax of the connect descriptor.
/
12198, 00000, "TNS:could not find path to destination"
// *Cause:  Could not navigate a path through Interchanges to the destination.
// This error occurs if an invalid community is in the address string, or
// the address includes a protocol that is not available or the
// TNSNAV.ORA file does not have a correct CMANAGER address specified or
// the Interchange is down.
// *Action: Assure that Interchanges necessary to get to the desired
// destination are up and have available capacity for an additional
// connection. Also check that the correct community and protocol have been
// specified in the CMANAGER address used.
/
12200, 00000, "TNS:could not allocate memory"
// *Cause:  Out of memory on machine.
// *Action: Reconfigure machine to have more storage or run fewer applications
//  while the Interchange is running.
/
12201, 00000, "TNS:encountered too small a connection buffer"
// *Cause: TNS connection buffer supplied by the application was too small
// to retrieve the data sent back.
// *Action: Supply a larger connection buffer. If problem persists, call
// Worldwide Customer Support.
/
12202, 00000, "TNS:internal navigation error"
// *Cause: Internal navigation error.
// *Action: Not normally visible to the user. For further details contact
// Worldwide Customer Support.
/
12203, 00000, "TNS:unable to connect to destination"
// *Cause: Invalid address specified or destination is not listening.
// This error can also occur because of underlying network or network
// transport problems.
// *Action: Verify that the net service name you entered was correct.
// Verify that the ADDRESS portion of the connect descriptor which
// corresponds to the net service name is correct.  Ensure that the
// destination process (for example the listener) is running at the
// remote node.
/
12204, 00000, "TNS:received data refused from an application"
// *Cause: The application using Connection Manager refused the
// connection at the listener.
// *Action: Make sure that the application listener at the destination is
// functioning correctly. If it is and the problem persists, contact
// Worldwide Customer Support.
/
12205, 00000, "TNS:could not get failed addresses"
// *Cause: Internal navigation error.
// *Action: Not normally visible to the user. For further details contact
// Worldwide Customer Support.
/
12206, 00000, "TNS:received a TNS error during navigation"
// *Cause: Internal navigation error because of an unexpected TNS error.
// *Action: Look at the log file to find the TNS error. If necessary, turn
// on tracing and repeat the operation.
/
12207, 00000, "TNS:unable to perform navigation"
// *Cause: Improperly configured navigation file TNSNAV.ORA.
// *Action: Check the syntax of the TNSNAV.ORA file on the application`s
// machine, and verify that it lists the correct communities.
/
12208, 00000, "TNS:could not find the TNSNAV.ORA file"
// *Cause: Either the ORACLE environment is not set up correctly, or the
// TNSNAV.ORA file is not present.
// *Action: Ensure that the ORACLE environment is set up appropriately
// on your platform and that a TNSNAV.ORA file is present.
/
12209, 00000, "TNS:encountered uninitialized global"
// *Cause: Application calling navigation routine has not properly configured
// the global variables. There are no TNSNAV.ORA files available, or they
// are defective.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Worldwide Customer Support.
/
12210, 00000, "TNS:error in finding Navigator data"
// *Cause: Application calling navigation routine has not properly configured
// the TNSNAV.ORA file.
// *Action: Check the syntax of the TNSNAV.ORA file.
/
12211, 00000, "TNS:needs PREFERRED_CMANAGERS entry in TNSNAV.ORA"
// *Cause: TNSNAV.ORA does not have a PREFERRED_CMANAGERS defined.
// *Action: Add a PREFERRED_CMANAGERS entry to the TNSNAV.ORA file.
/
12212, 00000, "TNS:incomplete PREFERRED_CMANAGERS binding in TNSNAV.ORA"
// *Cause: The PREFERRED_CMANAGERS binding in the client's TNSNAV.ORA file
// does not have a CMANAGER_NAME specified.
// *Action: Define the CMANAGER_NAME as part of the PREFERRED_CMANAGERS
// binding. Use of the Oracle Network Manager should eliminate this
// error.
/
12213, 00000, "TNS:incomplete PREFERRED_CMANAGERS binding in TNSNAV.ORA"
// *Cause: The PREFERRED_CMANAGERS binding in the client's TNSNAV.ORA file
// does not have an ADDRESS specified.
// *Action: Define the ADDRESS as part of the PREFERRED_CMANAGERS binding.
/
12214, 00000, "TNS:missing local communities entry in TNSNAV.ORA"
// *Cause: There is no LOCAL_COMMUNITIES  entry in TNSNAV.ORA.
// *Action: Define the LOCAL_COMMUNITIES for this node in the TNSNAV.ORA
// file.
/
12215, 00000, "TNS:poorly formed PREFERRED_NAVIGATORS Addresses in TNSNAV.ORA"
// *Cause: Address binding for PREFERRED_NAVIGATORS entry is improperly entered.
// entry.
// *Action: Check your PREFERRED_NAVIGATORS entry and fix it in TNSNAV.ORA
//
/
12216, 00000, "TNS:poorly formed PREFERRED_CMANAGERS addresses in TNSNAV.ORA"
// *Cause: Address binding for the PREFERRED_CMANAGERS entry in the client's
// TNSNAV.ORA file is improperly entered.
// *Action: Define the ADDRESS as part of the PREFERRED_CMANAGERS binding.
/
12217, 00000, "TNS:could not contact PREFERRED_CMANAGERS in TNSNAV.ORA"
// *Cause: There is a syntax error in the PREFERRED_CMANAGERS entry, or
// addresses specified are wrong, or the intended Connection Managers are
// unavailable.
// *Action: Check the PREFERRED_CMANAGERS entries in the client's
// TNSNAV.ORA file and correct them or talk with your network administrator
// to determine if the specified Connection Managers are available.
// Verify that the Interchanges are active by using the INTCTL STATUS
// command.
/
12218, 00000, "TNS:unacceptable network configuration data"
// *Cause: Poorly formed network configuration data. For example, a
// PREFERRED_CMANAGERS entry may have an incorrect CMANAGER_NAME in the
// client's TNSNAV.ORA file. Or an Interchange downtime parameter
// (TIMEOUT_INTERVAL) on the Navigator may be set to zero in INTCHG.ORA.
// *Action: Check the entries in TNSNAV.ORA and the Interchange
// configuration files and correct them. If necessary, talk with your
// network administrator to determine if the specified Interchanges
// (Connection Managers) are available and properly configured.
// Use the Oracle Network Manager to generate the configuration files
// if necessary.
/
12219, 00000, "TNS:missing community name from address in ADDRESS_LIST"
// *Cause: This error occurs when an ADDRESS_LIST has some ADDRESSes in it
// that have no COMMUNITY component and others that do have a COMMUNITY
// component.
// *Action: Check that in the connect descriptors you are using either
// all the ADDRESSes have a COMMUNITY component or all do not.
/
/ All succeeding errors are a remap of NS errors in NR
/
12221, 00000, "TNS:illegal ADDRESS parameters"
// *Cause: An illegal set of protocol adapter parameters was specified. In
// some cases, this error is returned when a connection cannot be made to the
// protocol transport.
// *Action: Verify that the destination can be reached using the specified
// protocol. Check the parameters within the ADDRESS section of
// TNSNAMES.ORA or in the directory.  Legal ADDRESS parameter formats may
// be found in the Oracle operating system specific documentation or the
// Oracle Net Administrator's Guide. Protocols that resolve names at the
// transport layer are vulnerable to this error if not properly configured
// or names are misspelled.
/
12222, 00000, "TNS:no support is available for the protocol indicated"
// *Cause: The protocol requested in the ADDRESS portion of the connect
// descriptor identified through the net service name is not available.
// If the supplied ADDRESS is typographically correct then support for
// that protocol is not installed.
// *Action: Install support for the protocol or correct typographical error,
// as appropriate.  Note: if the supplied address was derived from
// resolving the net service name, check the address in the appropriate file
// (TNSNAMES.ORA, LISTENER.ORA) or in the directory server.
/
12223, 00000, "TNS:internal limit restriction exceeded"
// *Cause: Too many TNS connections open simultaneously.
// *Action: Wait for connections to close and re-try.
/
12224, 00000, "TNS:no listener"
// *Cause: The connection request could not be completed because the listener
// is not running.
// *Action: Ensure that the supplied destination address matches one of
// the addresses used by the listener - compare the TNSNAMES.ORA entry with
// the appropriate LISTENER.ORA file (or TNSNAV.ORA if the connection is to
// go by way of an Interchange). Start the listener on the remote machine.
/
12225, 00000, "TNS:destination host unreachable"
// *Cause: Contact can not be made with remote party.
// *Action: Make sure the network driver is functioning and the network is up.
/
12226, 00000, "TNS:operating system resource quota exceeded"
// *Cause: The current user has exceeded the allotted resource assigned in the
// operating system.
// *Action: Acquire more operating system resource, or perform a different
// function.
/
12227, 00000, "TNS:syntax error"
// *Cause: The supplied connect descriptor contains illegal syntax.
// *Action: Check the syntax of the connect descriptor in TNSNAMES.ORA.
/
12228, 00000, "TNS:protocol adapter not loadable"
// *Cause:  On some platforms (such as Windows) protocol support is loaded at
// run-time. If the shared library (or DLL) for the protocol adapter is
// missing or one of its supporting libraries is missing then this error is
// returned.
// *Action: For further details, turn on tracing and reexecute the operation.
// The trace file will include the name of the shared library (or DLL) that
// could not be loaded.
/
12229, 00000, "TNS:Interchange has no more free connections"
// *Cause:  One or more Interchanges along the path to the destination
// desired has no more free connections available to be used for this
// call.
// *Action: Try again later when the Interchanges are less busy, or contact
// your network administrator to have him determine which interchange it is,
// and increase the number of connections available on that interchange.
/
12230, 00000, "TNS:Severe Network error occurred in making this connection"
// *Cause: This error is reported by an interchange which fails to make
// contact with the destination due to a physical network error while calling
// a destination.
// *Action: Try again later when the network service may have been fixed
// or report the problem to your Network Administrator so that he may fix
// the problem.
/
12231, 00000, "TNS:No connection possible to destination"
// *Cause: This error is reported by an interchange which fails to find a
// possible connection along the path to the destination.
// *Action: Report the problem to your Network Administrator so that he may
// fix the problem.
/
12232, 00000, "TNS:No path available to destination"
// *Cause: This error is reported by an interchange which fails to find a
// possible path to the destination.
// *Action: Report the problem to your Network Administrator so that he may
// fix the problem.
/
12233, 00000, "TNS:Failure to accept a connection"
// *Cause: This error is reported by an interchange which fails to accept 
// a connection due to a redirect failure.
// *Action: Report the problem to your Network Administrator so that he may
// isolate the interchange problem.
/
12234, 00000, "TNS:Redirect to destination"
// *Cause: This error is reported by an interchange which determines that this
// interchange is not the right gateway and needs to redirect the connection
// to another gateway along the path to the destination.
// *Action: None.
/
12235, 00000, "TNS:Failure to redirect to destination"
// *Cause: This error is reported by an interchange which fails to redirect 
// a connection to another interchange along the path to the destination.
// *Action: Report the problem to your Network Administrator so that he may
// fix the problem.
/
12236, 00000, "TNS:protocol support not loaded"
// *Cause:  On some platforms (such as Windows) protocol support is loaded at
// run-time. If the shared library (or DLL) for the protocol adapter has not
// been loaded, then this error is returned.
// *Action: For further details, turn on tracing and reexecute the operation.
// The trace file will have the name of the shared library (or DLL) that has
// not been loaded.
/
/ This line is an OSN Magic Cookie. Don't eat it. Last NR error in 2.0.9.
/
/

/ Copyright (c) 1991, 1996, 1997, 1998, 1999, 2000, 2001 by the Oracle Corporation.  All rights reserved.
/
/
/ $Header: net12500.msg 12-dec-2002.20:37:04 jpullokk Exp $
/
/
/ NAME
/   net12500.msg - Oracle Net external message file starting from 12500 -
/   U.S. english version
/
/
/ FUNCTION
/   Network error message file, American English version.
/
/
/ NOTES
/       Only external errors are to be put into this file. Internal
/       messages are to put into netius.msg.
/
/       This file, along with netius.msg and net12150.msg, forms tnsus.msg. As a
/       result, the errors in this file may not overlap with the errors in
/       those files. Otherwise, errors will result when generating tnsus.msb.
/
/       Message text should be limited to a maximum of 76 characters.
/       Messages containing embedded % directives should not overrun
/       the 76 character limit unless they signal unusual errors
/       which do not occur as part of user applications.  For example,
/       startup errors and system-dependent errors can probably get
/       away with longer message text.
/
/
/       '/' at beginning-of-line for comments.
/       '//' at beginning-of-line for *Cause: and *Action: fields.
/
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/////////////////////////// Please maintain this map //////////////////////
/
// 00001 - 04200  See netius.msg
/       .
/       .
/ 12150 - 12285   See net12150.msg
/ 12286 - 12499   ---(Reserved)---
/ 12500 - 12530   NSG errors reportable by OSN (returned in cndo).
/ 12531 - 12629   NS (and NT errors reported as NS errors) reportable by OSN
/ 12630 - 12699   NA errors (returned by native services)
/       .
/       .
/       .
/
/////////////////////////// Please maintain this map //////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/
/
/
/ OWNER
/   Network and Management Products - Server Technologies
/
/ MODIFIED
/    jpullokk   12/10/02 - Change documentation for 12535
/    ppovinec   11/21/02 - 12526-12528 updated
/    ppovinec   10/08/02 - Add listener messages for RESTRICTED instance
/    mclose     10/03/02 - Improve messages
/    cozhang    07/24/02 - Msgs for 12607 NSECONNTIMEOUT, 12608 NSESENDTIMEOUT
/                          & 12609 NSERECVTIMEOUT. Move NSEAPPTIMEOUT to 12606.
/    vle        07/16/02 - Modify NA error messages
/    cozhang    03/15/02 - Add msg for lsnr connect timeout (12525 NSGMOCTO).
/    cozhang    12/11/01 - Add message for app timeout (12604 NSEAPPTIMEOUT).
/    rachacos   04/04/01 - Define message for 12602 (NSECPLIMIT).
/    ppovinec   02/08/01 - Net8 --> Oracle Net rename.
/    ppovinec   07/18/00 - Listener's 8.2 error messages.
/    tclarke    02/25/00 - umcomment lost messages for oerr
/    ppovinec   07/16/99 - Make 12510 more meaningful.
/    vle        04/29/99 - fix misspelling
/    emalasky   11/10/98 - add catch-all handler error
/    emalasky   11/04/98 - add new direct handoff failure error
/    skanjila   09/04/98 - Add NAE Double Encryption Error Message.
/    emalasky   04/05/98 - add 8.1 service naming messsages
/    emalasky   12/09/97 - add NSG messages
/    emalasky   05/07/97 - 12505: no args, better cause
/    emalasky   05/01/97 - rollback 12505
/    smckinle   04/21/97 - Change 12505 to take an SID parameter.
/    rwessman   03/19/97 - Eliminated references to Secure Network Services. It
/    rwessman   03/09/97 - split from netus.msg to correct bug in building
/                          oraus.msg.
/
/ Some error messages are obsolete (no longer used).  They have been removed
/ from this file and their error numbers can at some point distant point
/ in the future be reused. In order to track there error numbers they are
/ listed below by what release they were removed for and the date they
/ were removed.
/
/   Removed beginning with release 10.0.0.X on 10/03/2002:
/        12501,12506,12507,12512,12517
/
/ 12500 - 12530 Reserved for NSG errors reportable to OSN.
/
/ tnslsnr errors...
12500, 00000, "TNS:listener failed to start a dedicated server process"
// *Cause:  The process of starting up a dedicated server process failed.
// The executable could not be found or the environment may be set up
// incorrectly.
// *Action: Turn on tracing at the ADMIN level and reexecute the operation.
// Verify that the ORACLE Server executable is present and has execute
// permissions enabled. Ensure that the ORACLE environment is specified
// correctly in LISTENER.ORA. The Oracle Protocol Adapter that is being 
// called may not be installed on the local hard drive.  Please check that
// the correct Protocol Adapter are successfully linked.
// If error persists, contact Oracle Customer Support.
/
12502, 00000, "TNS:listener received no CONNECT_DATA from client"
// *Cause:  No CONNECT_DATA was passed to the listener.
// *Action: Check that the service name resolved from TNSNAMES.ORA has
// the CONNECT_DATA component of the connect descriptor.
/
12504, 00000, "TNS:listener was not given the SID in CONNECT_DATA"
// *Cause:  The SID was missing from the CONNECT_DATA.
// *Action: Check that the connect descriptor corresponding to the service
// name in TNSNAMES.ORA has an SID component in the CONNECT_DATA.
/
12505, 00000, "TNS:listener does not currently know of SID given in connect descriptor"
// *Cause:  The listener received a request to establish a connection to a
// database or other service. The connect descriptor received by the listener
// specified a SID for an instance (usually a database instance) that either
// has not yet dynamically registered with the listener or has not been
// statically configured for the listener. This may be a temporary condition
// such as after the listener has started, but before the database instance
// has registered with the listener.
// *Action: 
//  - Wait a moment and try to connect a second time.
//  - Check which instances are currently known by the listener by executing:
//    lsnrctl services <listener name>
//  - Check that the SID parameter in the connect descriptor specifies
//    an instance known by the listener.
//  - Check for an event in the listener.log file.
/
12508, 00000, "TNS:listener could not resolve the COMMAND given"
// *Cause:  The COMMAND given to listener is not supported.
// *Action: This is not seen in normal use of Oracle Net.
// *Comment: Check the COMMAND given to listener. This error is probably
// caused by incompatible Oracle Net or Net8 versions.
// Do not include in error manual.
/
12509, 00000, "TNS:listener failed to redirect client to service handler"
// *Cause:  The dispatcher terminated unexpectedly
// *Action: Attempt to connect again and if the same error occurs,
// contact the DBA to check the state of the dispatchers for this SID.
// If the problem persists, turn on tracing in the listener to determine
// the TNS error caused by the redirect.
/
12510, 00000, "TNS:database temporarily lacks resources to handle the request"
// *Cause:  The dispatchers appear to be busy handling other requests.
// *Action: Attempt the connection again. If error persists, ask
// the DBA to increase the number of dispatchers and/or dispatchers' limit on 
// number of connections/sessions that they can accept.
/
12511, 00000, "TNS:service handler found but it is not accepting connections"
// *Cause:  The dispatchers notified the listener that they temporarily 
// do not accept new connections. 
// *Action: Attempt the connection again. If error persists, contact the DBA
// to check the state of the dispatchers and/or ask him to increase the number
// of dispatchers.
/
12513, 00000, "TNS:service handler found but it has registered for a different protocol"
// *Cause:  The dispatchers registered for this service are connected to
// the listener by way of a different network protocol than that of the client.
// *Action: Contact the DBA to register a dispatcher on your protocol.
/
12514, 00000, "TNS:listener does not currently know of service requested in connect descriptor"
// *Cause:  The listener received a request to establish a connection to a
// database or other service. The connect descriptor received by the listener
// specified a service name for a service (usually a database service)
// that either has not yet dynamically registered with the listener or has
// not been statically configured for the listener.  This may be a temporary
// condition such as after the listener has started, but before the database
// instance has registered with the listener.
// *Action: 
//  - Wait a moment and try to connect a second time.
//  - Check which services are currently known by the listener by executing:
//    lsnrctl services <listener name>
//  - Check that the SERVICE_NAME parameter in the connect descriptor of the
//    net service name used specifies a service known by the listener.
//  - If an easy connect naming connect identifier was used, check that
//    the service name specified is a service known by the listener.
//  - Check for an event in the listener.log file.
/
12515, 00000, "TNS:listener could not find a handler for this presentation"
// *Cause:  None of the listener's known service handlers are registered
// as supporting the presentation protocol required by the connecting client.
// *Action: Check that the destination service is configured to accept the
// presentation protocol.
/
12516, 00000, "TNS:listener could not find available handler with matching protocol stack"
// *Cause: None of the known and available service handlers for the given 
// SERVICE_NAME support the client's protocol stack: transport, session, 
// and presentation protocols.
// *Action: Check to make sure that the service handlers (e.g. dispatchers) 
// for the given SERVICE_NAME are registered with the listener, are accepting 
// connections, and that they are properly configured to support the desired 
// protocols.
/
12518, 00000, "TNS:listener could not hand off client connection"
// *Cause: The process of handing off a client connection to another process
// failed.
// *Action: Turn on listener tracing and re-execute the operation. Verify
// that the listener and database instance are properly configured for
// direct handoff.  If problem persists, call Oracle Support.
// *Comment: The problem can be worked around by configuring dispatcher(s)
// to specifically handle the desired presentation(s), and connecting
// directly to the dispatcher, bypassing the listener.
/
12519, 00000, "TNS:no appropriate service handler found"
// *Cause: The listener could not find any available service handlers that
// are appropriate for the client connection.
// *Action: Run "lsnrctl services" to ensure that the instance(s) have
// registered with the listener, and are accepting connections.
/
12520, 00000, "TNS:listener could not find available handler for requested type of server"
// *Cause: None of the known and available service handlers for requested type 
// of server (dedicated or shared) are appropriate for the client connection.
// *Action: Run "lsnrctl services" to ensure that the instance(s) have
// registered with the listener and that the appropriate handlers are 
// accepting connections. 
/
12521, 00000, "TNS:listener does not currently know of instance requested in connect descriptor"
// *Cause:  The listener received a request to establish a connection to a
// database or other service. The connect descriptor received by the listener
// specified in addition to the service name an instance name for an instance
// (usually a database instance) that either has not yet dynamically registered
// with the listener or has not been statically configured for the listener.
// This may be a temporary condition such as after the listener has started,
// but before the database instance has registered with the listener.
// *Action: 
//  - Wait a moment and try to connect a second time.
//  - Check which instances are currently known by the listener by executing:
//    lsnrctl services <listener name>
//  - Check that the INSTANCE_NAME parameter in the connect descriptor specifies
//    an instance name known by the listener.
//  - Check for an event in the listener.log file.
/
12522, 00000, "TNS:listener could not find available instance with given INSTANCE_ROLE"
// *Cause: There are not any available and appropriate database instances 
// registered with the listener, that are part of the service identified by 
// SERVICE_NAME given in the connect descriptor and that have the specified 
// INSTANCE_ROLE (and INSTANCE_NAME, if specified). 
// *Action: Check to make sure that the INSTANCE_ROLE specified is correct. 
// Run "lsnrctl services" to ensure that the instance(s) have registered with 
// the listener and that they are ready to accept connections.
/
12523, 00000, "TNS:listener could not find instance appropriate for the client connection"
// *Cause:  The listener could not find any available (database) instances, 
// that are appropriate for the client connection.
// *Action: Run "lsnrctl services" to ensure that the instance(s) are
// registered with the listener, and have status READY.
/
12524, 00000, "TNS:listener could not resolve HANDLER_NAME given in connect descriptor"
// *Cause: The HANDLER_NAME in the CONNECT_DATA was not found in the listener's
// tables for the specified SERVICE_NAME and INSTANCE_NAME.
// *Action: Check to make sure that the HANDLER_NAME specified is correct.
// *Comment: This error will be returned if the database instance and/or its
// service handlers have not been registered with the listener or they have
// been registered for different service; the instance may need to be started.
/
12525, 00000, "TNS:listener has not received client's request in time allowed"
// *Cause: The listener disconnected the client because the client failed to
// provide the necessary connect information within the allowed time interval.
// This may be a result of network or system delays; or this may indicate that a
// malicious client is trying to cause a Denial of Service attack on the
// listener.
// *Action: If the error occurred because of a slow network or system,
// reconfigure INBOUND_CONNECT_TIMEOUT to a larger value. If a malicious
// client is suspected, use the address in listener.log to identify the
// source and restrict access. Turn on tracing for more information.
// *Comment: The logged address in listener.ora may not be reliable as it
// can be forged at the lower networking layers (e.g. in the case of TCP/IP).
/
12526, 00000, "TNS:listener: all appropriate instances are in restricted mode"
// *Cause:  Database instances supporting the service requested by the client
// were in restricted mode. The Listener does not allow connections to 
// instances in restricted mode. This condition may be temporary, such as 
// during periods when database administration is performed.
// *Action: Attempt the connection again. If error persists, then contact
// the database administrator to change the mode of the instance, 
// if appropriate.
/
12527, 00000, "TNS:listener: all instances are in restricted mode or blocking new connections"
// *Cause:  All appropriate database instances supporting the service requested
// by the client reported that they either were in restricted mode or were 
// blocking the new connections. The Listener does not allow connections to 
// such instances. This condition may be temporary, such as at instance 
// startup.
// *Action: Attempt the connection again. If error persists, then contact the 
// database administrator to check the status of the instances. 
/
12528, 00000, "TNS:listener: all appropriate instances are blocking new connections"
// *Cause:  All instances supporting the service requested by the client 
// reported that they were blocking the new connections. This condition may be
// temporary, such as at instance startup. 
// *Action: Attempt the connection again. If error persists, then contact the
// administrator to check the status of the instances.
/
12529, 00000, "TNS:connect request rejected based on current filtering rules"
// *Cause: Connection Manager and its listener were configured with filtering 
// rules specifying that the connect request be rejected.
// *Action: If this connect request should be allowed, then contact the 
// administrator to modify the filtering rules.
/
/ This line is an OSN Magic Cookie. Don't eat it. Last NSG error in 2.0.9.
/
/
////////////////////////////////////////////////////////////////////
/
/ 12531 - 12629 ns errors reportable to osn:
/
/               12531 - 15609 ns primary errors
/               12610 - 12629 ns secondary errors
/
/               A primary may (optionally) be qualified by a secondary
/               error.  For example: 12531 ("invalid argument") might
/               be qualified by 12617 ("bad 'what' value").
/
12531, 00000, "TNS:cannot allocate memory"
// *Cause:  Sufficient memory could not be allocated to perform the desired
// activity.
// *Action:  Either free some resource for TNS, or add more memory to the
// machine. For further details, turn on tracing and reexecute the operation.
/
12532, 00000, "TNS:invalid argument"
// *Cause:  An internal function received an invalid parameter.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12533, 00000, "TNS:illegal ADDRESS parameters"
// *Cause: An illegal set of protocol adapter parameters was specified. In
// some cases, this error is returned when a connection cannot be made to the
// protocol transport.
// *Action: Verify that the destination can be reached using the specified
// protocol. Check the parameters within the ADDRESS section of
// TNSNAMES.ORA.  Legal ADDRESS parameter formats may be found in the
// Oracle operating system specific documentation for your platform.
// Protocols that resolve names at the transport layer (such as DECnet object
// names) are vulnerable to this error if not properly configured or names are
// misspelled.
/
12534, 00000, "TNS:operation not supported"
// *Cause:  An internal function received a request to perform an
// operation that is not supported (on this machine).
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12535, 00000, "TNS:operation timed out"
// *Cause: The requested operation could not be completed within the time out
// period.
// *Action: Look at the documentation on the secondary errors for possible
// remedy. See SQLNET.LOG to find secondary error if not provided explicitly.
// Turn on tracing to gather more information.
/
12536, 00000, "TNS:operation would block"
// *Cause: An internal operation did not commence because to do so would
// block the current process and the user has requested that operations be
// non-blocking.
// *Action:  None needed; this is an information message.
/
12537, 00000, "TNS:connection closed"
// *Cause: "End of file" condition has been reached; partner has disconnected.
// *Action: None needed; this is an information message.
/
12538, 00000, "TNS:no such protocol adapter"
// *Cause: The protocol adapter requested (by way of the "(PROTOCOL=..)"
// keyword-value pair in a TNS address) is unknown. If the supplied address
// is typographically correct then the protocol adapter is not installed.
// *Action: Install the protocol adapter or correct typographically error,
// as appropriate.  Note: if the supplied address was derived from
// resolving the service name, check the address in the appropriate file
// (TNSNAMES.ORA, LISTENER.ORA or SQLNET.ORA).
/
12539, 00000, "TNS:buffer over- or under-flow"
// *Cause: Buffer too small for incoming data or too large for outgoing data.
// *Action:  This restriction (which is associated with CONNECT DATA) is not
// normally visible to the user. For further details, turn on tracing and
// reexecute the operation; contact Oracle Customer Support.
/
12540, 00000, "TNS:internal limit restriction exceeded"
// *Cause: Too many TNS connections open simultaneously.
// *Action: Wait for connections to close and re-try.
/
12541, 00000, "TNS:no listener"
// *Cause: The connection request could not be completed because the listener
// is not running.
// *Action: Ensure that the supplied destination address matches one of
// the addresses used by the listener - compare the TNSNAMES.ORA entry with
// the appropriate LISTENER.ORA file (or TNSNAV.ORA if the connection is to
// go by way of an Interchange). Start the listener on the remote machine.
/
12542, 00000, "TNS:address already in use"
// *Cause: Specified listener address is already being used.
// *Action: Start your listener with a unique address.
/
12543, 00000, "TNS:destination host unreachable"
// *Cause: Contact can not be made with remote party.
// *Action: Make sure the network driver is functioning and the network is up.
/
12544, 00000, "TNS:contexts have different wait/test functions"
// *Cause: Two protocol adapters have conflicting wait/test functions.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12545, 00000, "Connect failed because target host or object does not exist"
// *Cause: The address specified is not valid, or the program being 
// connected to does not exist.
// *Action: Ensure the ADDRESS parameters have been entered correctly; the
// most likely incorrect parameter is the node name.  Ensure that the 
// executable for the server exists (perhaps "oracle" is missing.)
// If the protocol is TCP/IP, edit the TNSNAMES.ORA file to change the
// host name to a numeric IP address and try again.
/
12546, 00000, "TNS:permission denied"
// *Cause: User has insufficient privileges to perform the requested operation.
// *Action: Acquire necessary privileges and try again.
/
12547, 00000, "TNS:lost contact"
// *Cause: Partner has unexpectedly gone away, usually during process
// startup.
// *Action: Investigate partner application for abnormal termination. On an
// Interchange, this can happen if the machine is overloaded.
/
12548, 00000, "TNS:incomplete read or write"
// *Cause: A data send or receive failed.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12549, 00000, "TNS:operating system resource quota exceeded"
// *Cause: The current user has exceeded the allotted resource assigned in the
// operating system.
// *Action: Acquire more operating system resource, or perform a different
// function.
/
12550, 00000, "TNS:syntax error"
// *Cause: The supplied connect descriptor contains illegal syntax.
// *Action: Check the syntax of the connect descriptor in TNSNAMES.ORA.
/
12551, 00000, "TNS:missing keyword"
// *Cause: The supplied connect descriptor is missing one or more TNS
// keywords.
// *Action: Check the syntax, and ensure all required keywords are present.
/
12552, 00000, "TNS:operation was interrupted"
// *Cause: An internal operation was interrupted and could not complete.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12554, 00000, "TNS:current operation is still in progress"
// *Cause: An internal operation is still in progress.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12555, 00000, "TNS:permission denied"
// *Cause: User has insufficient privileges to perform the requested operation.
// *Action: Acquire necessary privileges and try again.
/
12556, 00000, "TNS:no caller"
// *Cause: TNS detected an incoming connect request but there was no caller.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact 
// Oracle Customer Support.
/
12557, 00000, "TNS:protocol adapter not loadable"
// *Cause:  On some platforms (such as OS/2) protocol adapters are loaded at
// run-time. If the shared library (or DLL) for the protocol adapter is
// missing or one of its supporting libraries is missing then this error is
// returned.
// *Action: For further details, turn on tracing and reexecute the operation.
// The trace file will include the name of the shared library (or DLL) that
// could not be loaded.
/
12558, 00000, "TNS:protocol adapter not loaded"
// *Cause:  On some platforms (such as OS/2) protocol adapters are loaded at
// run-time. If the shared library (or DLL) for the protocol adapter has not
// been loaded, then this error is returned.
// *Action: For further details, turn on tracing and reexecute the operation.
// The trace file will have the name of the shared library (or DLL) that has
// not been loaded.
/
12560, 00000, "TNS:protocol adapter error"
// *Cause: A generic protocol adapter error occurred.
// *Action: Check addresses used for proper protocol specification. Before
// reporting this error, look at the error stack and check for lower level
// transport errors. For further details, turn on tracing and reexecute the
// operation. Turn off tracing when the operation is complete.
/
12561, 00000, "TNS:unknown error"
// *Cause: A generic protocol error occurred.
// *Action: For further details, turn on tracing and reexecute the operation.
/
12562, 00000, "TNS:bad global handle"
// *Cause: Internal error - bad 'gbh' argument passed to TNS from caller.
// System may have been linked with old libraries.
// *Action: Not normally visible to the user, contact Oracle Customer
// Support.
/
12564, 00000, "TNS:connection refused"
// *Cause: The connect request was denied by the remote user (or TNS software).
// *Action: Not normally visible to the user.  For further details, turn on
// tracing and reexecute the operation.
/
12566, 00000, "TNS:protocol error"
// *Cause: An unexpected TNS protocol error has occurred.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
12569, 00000, "TNS:packet checksum failure"
// *Cause: The data received is not the same as the data sent.
// *Action: Attempt the transaction again. If the error is persistent, turn
// on tracing and reexecute the operation.
/
12570, 00000, "TNS:packet reader failure"
// *Cause: An error occurred during a data receive.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12571, 00000, "TNS:packet writer failure"
// *Cause: An error occurred during a data send.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12574, 00000, "TNS:redirection denied"
// *Cause: The connect request failed because it would have required
// redirection and the caller has requested no redirections.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12582, 00000, "TNS:invalid operation"
// *Cause:  An internal function received an invalid request.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12583, 00000, "TNS:no reader"
// *Cause:  A send operation has been requested but partner has already
// disconnected.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12585, 00000, "TNS:data truncation"
// *Cause:  A receive operation has completed with insufficient data
// to satisfy the user's request.
// *Action: Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12589, 00000, "TNS:connection not bequeathable"
// *Cause: An attempt to hand-off a connection from one process to another
// has failed because the protocol provider does not support it.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12590, 00000, "TNS:no I/O buffer"
// *Cause: An attempt to perform an I/O operation failed because no buffer
// was available.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12591, 00000, "TNS:event signal failure"
// *Cause: The TNS software is unable to signal an event occurrence.
// *Action: For further details, turn on tracing and reexecute the operation.
// If error persists, contact Oracle Customer Support.
/
12592, 00000, "TNS:bad packet"
// *Cause: An ill-formed packet has been detected by the TNS software.
// *Action: For further details, turn on tracing and reexecute the
// operation. If error persists, contact Oracle Customer Support.
/
12593, 00000, "TNS:no registered connection"
// *Cause: An attempt to solicit network event activity has failed because
// no connections are registered for event notification.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12595, 00000, "TNS:no confirmation"
// *Cause: TNS is unable to get requested confirmation acknowledgment from
// remote partner.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12596, 00000, "TNS:internal inconsistency"
// *Cause: TNS has detected an internal inconsistency.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation and contact Oracle Customer
// Support.
/
12597, 00000, "TNS:connect descriptor already in use"
// *Cause:  Internal error - illegal use of connect descriptor.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12598, 00000, "TNS:banner registration failed"
// *Cause:  The registration of a product banner with the Oracle server failed.
// *Action: This is an error which is not normally visible externally. Enable
//          tracing and attempt to repeat the error. If it occurs
//          again, contact Oracle Customer Support.
/
12599, 00000, "TNS:cryptographic checksum mismatch"
// *Cause: The data received is not the same as the data sent.
// *Action: Attempt the transaction again. If error persists, check
// (and correct) the integrity of your physical connection.
/
12600, 00000, "TNS: string open failed"
// *Cause:  The creation of a string in ORACLE NLS format failed.
// *Action: This is an internal error, enable tracing and attempt to repeat the
//          error. If it occurs again, contact Oracle Customer Support.
/
12601, 00000, "TNS:information flags check failed"
// *Cause:  The TNS information flags set by the process prior to connection
//          negotiation were not present after the negotiation was
//          finished.
// *Action: This is an internal error. Enable tracing and attempt to repeat the
//          error. If it occurs again, contact Oracle Customer
//          Support.
/
12602, 00000, "TNS: Connection Pooling limit reached"
// *Cause:  The operation failed because maximum active current connections has
//          been reached. It may not be a real error when the Connection
//          Pooling feature is enabled. It is possible that the application
//          later reissues the operation and successfully grabs the connection
//          pool slot and proceeds.
// *Action: This is an internal error. Enable tracing and attempt to repeat the
//          error. If it occurs again, contact Oracle Customer
//          Support.
/
/ 12606 - 12629 ns secondary errors
/
12606, 00000, "TNS: Application timeout occurred"
// *Cause:  A network session did not reach an application-defined stage
//          within the allowed time interval.
// *Action: This is an error which does not normally appear at the high level.
//          The action to take is application specific, and is detailed in the
//          higher level error description.
/
12607, 00000, "TNS: Connect timeout occurred"
// *Cause:  A network session did not reach a predefined connect stage
//          within the allowed time interval.
// *Action: This is an error which does not normally appear at the high level.
//          The action to take is application specific, and is detailed in the
//          higher level error description.
/
12608, 00000, "TNS: Send timeout occurred"
// *Cause:  The send or write operation did not complete within the allowed
//          time interval.
// *Action: Check if the peer host is available. Increase the send timeout
//          value if necessary.
/
12609, 00000, "TNS: Receive timeout occurred"
// *Cause:  The receive or read operation did not complete within the allowed
//          time interval.
// *Action: Check if the peer host is available. Increase the receive timeout
//          value if necessary.
/
12611, 00000, "TNS:operation is not portable"
// *Cause: Attempted operation is not portable.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12612, 00000, "TNS:connection is busy"
// *Cause: Attempted operation failed because it conflicts with an ongoing
// action or status of the connection.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12615, 00000, "TNS:preempt error"
// *Cause: A request to service an event failed because no event notification
// has yet been posted.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12616, 00000, "TNS:no event signals"
// *Cause: The TNS software is unable to enable event signals.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
/12617, 00000, "TNS:bad 'what' type"
// *Cause: The operation failed because the type of data specified is unknown.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12618, 00000, "TNS:versions are incompatible"
// *Cause: The two machines are running incompatible versions of TNS.
// *Action: Check the version numbers, and upgrade the machine with the
// smaller one.
/
12619, 00000, "TNS:unable to grant requested service"
// *Cause: The connect request failed because requested service could not be
// provided by the local TNS software.
// *Action: If appropriate, reexecute with reduced service requirements.
/
12620, 00000, "TNS:requested characteristic not available"
// *Cause: The connect request failed because a requested transport
// characteristic could not be supported by the remote TNS software.
// *Action: If appropriate, reexecute with reduced requirements.
/
12622, 00000, "TNS:event notifications are not homogeneous"
// *Cause: An attempt to register a connection for event notification failed
// because the event notification type conflicts with existing registrations.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation and contact Oracle Customer
// Support.
/
12623, 00000, "TNS:operation is illegal in this state"
// *Cause: Connection is half-duplex and a full-duplex operation was
// attempted.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation. If error persists, contact
// Oracle Customer Support.
/
12624, 00000, "TNS:connection is already registered"
// *Cause: An attempt to register a connection for event notification failed
// because the connection is already registered.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation and contact Oracle Customer
// Support.
/
12625, 00000, "TNS:missing argument"
// *Cause: An operation failed because an argument was missing"
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation and contact Oracle Customer
// Support.
/
12626, 00000, "TNS:bad event type"
// *Cause: An attempt to register a connection for event notification failed
// because the event type is unknown.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation and contact Oracle Customer
// Support.
/
12628, 00000, "TNS:no event callbacks"
// *Cause: An attempt to register a connection for event notification failed
// because asynchronous callbacks are not available.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation and contact Oracle Customer
// Support.
/
12629, 00000, "TNS:no event test"
// *Cause: An attempt to register a connection for event notification failed
// because the ability to test for events is not available.
// *Action:  Not normally visible to the user. For further details, turn
// on tracing and reexecute the operation and contact Oracle Customer
// Support.
/
/ 12630 - 12699 Reserved for NA errors.
/
12630, 00000, "Native service operation not supported"
// *Cause:  An operation requested by a user is not supported by the native
//          services component.
// *Action: This may be an internal error if the operation should have been
//          supported.
/
12631, 00000, "Username retrieval failed"
// *Cause:  The authentication service failed to retrieve the name of a user.
// *Action: Enable tracing to determine which routine is failing.
/
12632, 00000, "Role fetch failed"
// *Cause:  The authentication service failed to retrieve one of the user's
//          roles.
// *Action: Enable tracing to determine which routine is failing.
/
12633, 00000, "No shared authentication services"
// *Cause:  The list of authentication services specified by the user does not
//          match those supported by the process.
// *Action: Either specify another list or relink the executable with the
//          desired services.
/
12634, 00000, "Memory allocation failed"
// *Cause:  Process was unable to allocate memory.
// *Action: Terminate other processes in order to reclaim needed memory.
/
12635, 00000, "No authentication adapters available"
// *Cause:  The executable was not linked with any authentication service
//          adapters but the sqlnet.ora parameter that determines whether or
//          not authentication is required was set to true.
// *Action: Either disable the parameter or relink the executable with service
//          adapters.
/
12636, 00000, "Packet send failed"
// *Cause:  A process was unable to send a packet to another process.
//          Possible causes are:
//          1. The other process was terminated.
//          2. The machine on which the other process is running went down.
//          3. Some other communications error occurred.
// *Action: If the cause is not obvious, contact Oracle Customer Support.
/
12637, 00000, "Packet receive failed"
// *Cause:  A process was unable to receive a packet from another process.
//          Possible causes are:
//          1. The other process was terminated.
//          2. The machine on which the other process is running went down.
//          3. Some other communications error occurred.
// *Action: If the cause is not obvious, contact Oracle Customer Support.
/
12638, 00000, "Credential retrieval failed"
// *Cause:  The authentication service failed to retrieve the credentials of a
//          user.
// *Action: Enable tracing to determine the exact error.
/
12639, 00000, "Authentication service negotiation failed"
// *Cause:  No match was found between the types of authentication services
//          that the client supports and those that the server is using.
// *Action: Possible solutions:
//          1. Change the entry in sqlnet.ora that determines which services
//             are to be used.
//          2. Relink the client with at least one of the authentication
//             service adapters that the server supports.
//          3. Relink the server with at least one of the authentication
//             service adapters that the client supports.
//          4. Disable authentication on both the client and server.
/
12640, 00000, "Authentication adapter initialization failed"
// *Cause:  The function specified in the authentication table entry for the
//          service failed.
// *Action: Enable tracing to determine the exact error.
/
12641, 00000, "Authentication service failed to initialize"
// *Cause:  The authentication service failed during initialization.
// *Action: Enable tracing to determine the exact error.
/
12642, 00000, "No session key"
// *Cause:  A process has no session key associated with it because the
//          authentication service being used does not use one.
// *Action: If a session key is required, use another authentication service.
/
12643, 00000, "Client received internal error from server"
// *Cause:  The client process received an error from the server that indicated
//          that an internal Oracle Net native services error had occurred.
// *Action: Enable tracing on both processes and attempt to recreate the
//          problem. If successful in recreating the problem, contact Oracle
//          Customer Support.
/
12645, 00000, "Parameter does not exist."
// *Cause:  A sqlnet.ora parameter from which a value was needed does not
//          exist.
// *Action: Set the parameter in the parameter file.
/
12646, 00000, "Invalid value specified for boolean parameter"
// *Cause:  The value specified for a parameter was set to a value other than
//          true/false or on/off.
// *Action: Correct the value of the parameter.
/
12647, 00000, "Authentication required"
// *Cause:  The parameter that controls whether authentication is required was
//          set to true, but the executable does not have an
//          authentication service linked in.
// *Action: Either re-link the executable with an authentication service
//          adapter or disable the parameter.
/
12648, 00000, "Encryption or data integrity algorithm list empty"
// *Cause:  An Oracle Advanced Security list-of-algorithms parameter was empty, e.g.
//          "()".
// *Action: Change the list to contain the name of at least one
//          installed algorithm, or remove the list entirely if every
//          installed algorithm is acceptable.
/
12649, 00000, "Unknown encryption or data integrity algorithm"
// *Cause:  An Oracle Advanced Security list-of-algorithms parameter included an
//          algorithm name that was not recognized.
// *Action: Either remove that algorithm name, correct it if it was
//          misspelled, or install the driver for the missing
//          algorithm.
/
12650, 00000, "No common encryption or data integrity algorithm"
// *Cause:  The client and server have no algorithm in common for
//          either encryption or data integrity or both.
// *Action: Choose sets of algorithms that overlap.  In other words,
//          add one of the client's algorithm choices to the server's
//          list or vice versa.
/
12651, 00000, "Encryption or data integrity algorithm unacceptable"
// *Cause:  The algorithm the server chose to use for encryption or
//          data integrity was not one of the choices acceptable to
//          the client.  This is either the result of an internal
//          error, of a network data transmission error, or of
//          deliberate tampering with the transmitted data.
// *Action: For further details, turn on tracing, re-execute the
//          operation, and contact Oracle Customer Support.
/
12652, 00000, "String truncated"
// *Cause:  Not enough memory was allocated for a string so it had to be
//          truncated
// *Action: If it is OK that the string is truncated, then it is not an
//          error. Otherwise, call the routine that reported the error
//          again with a larger string buffer.
/
12653, 00000, "Authentication control function failed"
// *Cause:  The control function utilized by the authentication service driver
//          failed.
// *Action: Enable tracing to determine the exact error.
/
12654, 00000, "Authentication conversion failed"
// *Cause:  The authentication service was unable to convert the credentials
//          of a user from the format specific to the format into the
//          ORACLE format.
// *Action: Enable tracing to determine the exact error.
/
12655, 00000, "Password check failed"
// *Cause:  The authentication service being used was unable to verify the
//          provided password.
// *Action: Enable tracing to determine the exact error.
/
12656, 00000, "Cryptographic checksum mismatch"
// *Cause:  The cryptographic checksum received with a packet of
// 	    incoming data didn't match the checksum computed by the
// 	    receiving end.  This indicates that the packet was
// 	    tampered with or otherwise corrupted in transit.
// *Action: Look for sources of data corruption, perhaps including
// 	    deliberate tampering.
/
12657, 00000, "No algorithms installed"
// *Cause:  The near side of the connection required the use of a
// 	    service (either encryption or checksumming) when no
// 	    algorithms for that service were installed.
// *Action: Remove the "ON" requirement for that service.
/
12658, 00000, "ANO service required but TNS version is incompatible"
// *Cause:  A client process that is running an earlier version of TNS
//          attempted to connect but the connection failed because the server
//          process required that an ANO service (authentication, encryption,
//          etc.) be used.
// *Action: Relink the calling executable and retry the connection or eliminate
//          the requirement that the service be used on the server side.
/
12659, 00000, "Error received from other process"
// *Cause:  An error was received by one or more services from the process on
//          the other side of the connection.
// *Action: Enable tracing to determine the exact error(s).
//          The error(s) is (are) not returned directly because an error
//          generated by a server may not make sense on the client side and
//          vice-versa.
/
12660, 00000, "Encryption or crypto-checksumming parameters incompatible"
// *Cause:  One side of the connection specified "REQUIRED" for encryption
//	    or crypto-checksumming, while the other side specified "REJECTED".
// *Action: Change the "REQUIRED" side to "REQUESTED" if the
//	    you want encryption or crypto-checksumming to be optional, or
//	    change the "REJECTED" side to "ACCEPTED" if you do not
//	    want the service to be optional.
/
12661, 00000, "Protocol authentication to be used"
// *Cause:  The Oracle Advanced Security authentication service has determined
//          that the Oracle Net transport protocol in use is to be utilized to
//          authenticate a user's identity.
// *Action: This error is used solely to communicate information between the
//          authentication service and the Oracle Net session layer and should not
//          normally be visible.
//          If the error is seen, contact Oracle Worldwide Support.
/
12662, 00000, "proxy ticket retrieval failed"
// *Cause:  The authentication adapter used by Oracle Net failed to retrieve the
//          credentials needed to authenticate a database link.
// *Action: Enable tracing to determine the exact error.
/
12663, 00000, "Services required by client not available on the server"
// *Cause:  Service(s) that was (were) required by the client process were not
//          available on the server process.
// *Action: Configure the server with the services required by the client (best
//          solution) or delete the requirement from the configuration
//          file of the client (least secure).
/
12664, 00000, "Services required by server not available on the client"
// *Cause:  Service(s) that was (were) required by the server process were not
//          available on the client process.
// *Action: Configure the client with the services required by the server (best
//          solution) or delete the requirement from the configuration
//          file of the server (least secure).
/
12665, 00000, "NLS string open failed"
// *Cause:  A native service was unable to make a string available for use by
//          the National Language Support component.
// *Action: Make sure the National Language Support component has been
//          properly. If it has, enable tracing and report the problem
//          to Customer Support.
/
12666, 00000, "Dedicated server: outbound transport protocol different from inbound"
// *Cause:  The protocol specified for an externally-identified outbound
//          connection from a dedicated server (database link) was not the same
//          as that used for the inbound connection. It is not possible for
//          Oracle Net to authenticate a proxy connection that uses a protocol
//          that is different from that which was used for the connection to
//          the dedicated server.
// *Action: Specify the same protocol in the Oracle Net connect descriptor
//          for the outbound connection as that used for the inbound
//          connection.
/
12667, 00000, "Shared server: outbound transport protocol different from inbound"
// *Cause:  The protocol specified for an externally-identified outbound
//          connection from a shared server (database link) was not the same as
//          as that used for the inbound connection. It is not possible for
//          Oracle Net to authenticate a proxy connection that uses a protocol
//          that is different from that which was used for the connection to
//          the shared server.
// *Action: Specify the same protocol in the Oracle Net connect descriptor
//          for the outbound connection as that used for the inbound
//          connection
/
12668, 00000, "Dedicated server: outbound protocol does not support proxies"
// *Cause:  The protocol specified to perform an externally-identified proxy
//          connection (database link) from a dedicated server does
//          not support proxy connections.
// *Action: Specify a protocol in the Oracle Net connect descriptor used for
//          the connection that does support externally-authenticated proxy 
//          connections.
//          NOTE: Because of a limitation in Oracle Net, the protocol used for
//                the proxy connection must the same as that used for the
//                connection from the client to the server.
/
12669, 00000, "Shared server: outbound protocol does not support proxies"
// *Cause:  The protocol specified to perform an externally-identified proxy
//          connection (database link) from a shared server does not support
//          proxy connections.
// *Action: Specify a protocol in the Oracle Net connect descriptor used for
//          the connection that does support externally-authenticated proxy 
//          connections.
//          NOTE: Because of a limitation in  Oracle Net, the protocol used for
//                the proxy connection must the same as that used for the
//                connection from the client to the server.
/
12670, 00000, "Incorrect role password"
// *Cause:  A password supplied for a role could not be validated by the
//          authentication service.
// *Action: Supply the correct password.
/
12671, 00000, "Shared server: adapter failed to save context"
// *Cause:  The adapter for the authentication service failed when it tried to
//          save the data needed for proxy connections (database
//          links) through the shared server.
// *Action: Enable tracing to determine the exact error. Contact Oracle
//          Customer Support if the reason is not obvious.
/
12672, 00000, "Database logon failure"
// *Cause:  The authentication service adapter in use encountered an error
//          it attempted to validate the logon attempt of a user.
// *Action: Enable tracing to determine the exact error encountered by the
//          adapter.
/
12673, 00000, "Dedicated server: context not saved"
// *Cause:  A connection was marked as being a proxy connection (database link)
//          from a dedicated server but no inbound context was present.
// *Action: This error should not normally be visible to the user. Contact
//          Oracle Customer Support.
/
12674, 00000, "Shared server: proxy context not saved"
// *Cause:  A connection was marked as being a proxy connection (database link)
//          from a shared server but no inbound context was present.
// *Action: This error should not normally be visible to the user. Contact
//          Oracle Customer Support.
/
12675, 00000, "External user name not available yet"
// *Cause:  The authentication service in use was not able to return the
//          external name of a user of the ORACLE server because it is not
//          available to the service yet.
// *Action: This is just an informational message and should not normally be
//          visible to the user. If the error does appear, contact Oracle
//          Customer Support.
/
12676, 00000, "Server received internal error from client"
// *Cause:  The server process received an error from the client which
//          indicated that an internal Oracle Net native services error had
//          occurred.
// *Action: Enable tracing on both processes and attempt to recreate the
//          problem. If the problem recurs, contact Oracle Customer
//          Support.
/
12677, 00000, "Authentication service not supported by database link"
// *Cause:  The authentication service used by the proxy process (database
//          link) was unable to find the adapter being used by the client
//          in its list of authentication mechanisms.
// *Action: Specify an authentication adapter that is shared by the client and
//          the server being used for the database link.
/
12678, 00000, "Authentication disabled but required"
// *Cause:  The configuration parameters that control whether Oracle Advanced
//          Security authentication is disabled or required were both set to TRUE.
// *Action: Set one or both of the parameters to FALSE.
/
12679, 00000, "Native services disabled by other process but required"
// *Cause:  The remote process has disabled native services but the local
//          process requires them.
// *Action: Enable native services on the remote process or disable them
//          locally.
/
12680, 00000, "Native services disabled but required"
// *Cause:  The process has disabled native services but at least one service
//          is required.
// *Action: Enable native services or change the configuration file so that
//          none of the available services are required.
/
12681, 00000, "Login failed: the SecurID card does not have a pincode yet"
// *Cause:  The SecurID card that is used to logon to Oracle, does not have
//          a pincode assigned to it.
// *Action: Use one of the programs supplied by Security Dynamics to assign
//          a pincode to the card. 
/
12682, 00000, "Login failed: the SecurID card is in next PRN mode"
// *Cause:  The SecurID card and the SecurID server are out of sync and the
//          server requires the next cardcode to resynchronize the card.
// *Action: Use one of the programs supplied by Security Dynamics to 
//          resynchronize the SecurID card. 
/
12683, 00000, "encryption/crypto-checksumming: no Diffie-Hellman seed"
// *Cause:  The "sqlnet.crypto_seed" parameter is missing from the
//          SQLNET.ORA parameters file for Oracle Advanced Security.
// *Action: Add this line to SQLNET.ORA:
//	      sqlnet.crypto_seed = "randomly-chosen text"
/
12684, 00000, "encryption/crypto-checksumming: Diffie-Hellman seed too small"
// *Cause:  The "sqlnet.crypto_seed" parameter in the SQLNET.ORA
//          parameter file for Oracle Advanced Security is too small.
// *Action: Add more randomly-chosen text to it, perhaps using Network
//          Manager.
/
12685, 00000, "Native service required remotely but disabled locally"
// *Cause:  A native service is required by the remote process but native
//          services have been disabled locally.
// *Action: Enable native services locally or change the configuration
//          parameters on the remote host so that no native services are
//          required.
/
12686, 00000, "Invalid command specified for a service"
// *Cause:  An operation which does not exist was specified for a native
//          service.
// *Action: This is a programming error and should not normally be visible to
//          the user. If the error does appear, contact Oracle Customer
//          Support.
/
12687, 00000, "Credentials expired."
// *Cause:  The credentials that are used to authenticate the user for the
//          requested connection have expired.
// *Action: Renew your credentials. Refer to the documentation specific for
//          your Network Authentication Adapter on how to do this.
/
12688, 00000, "Login failed: the SecurID server rejected the new pincode"
// *Cause:  There are a number of reasons why the SecurID server would refuse
//          a pincode:
//          - The user might not have permission to make up his own pincode.
//          - The pincode was either too short or too long. Valid pincodes
//            consist of minimal four, but no more than eight characters.
//          - The pincode contains any non alphanumeric characters.
// *Action: Reexecute the operation and make sure to use a pincode that
//          satisfies the above requirements. If the problem persists, turn 
//          on tracing at the Oracle Server side of the connection and 
//          examine the trace file for the exact error.
/
12689, 00000, "Server Authentication required, but not supported"
// *Cause:  Server Authentication is required for this connection, but not
//          supported by both sides of the connection.
// *Action: Make sure both sides of the connection have the correct version of
//          Advanced Networking Option, and that the Authentication Adapter
//          supports Server Authentication.
/
12690, 00000, "Server Authentication failed, login cancelled"
// *Cause:  Server Authentication is required, but the server's credentials
//          were found invalid by the client.
// *Action: Make sure that the server has a valid set of credentials. Refer to
//          your authentication adapter specific documentation on how to do
//          this.
/
12696, 00000, "Double Encryption Turned On, login disallowed"
// *Cause:  The user is using a Secure Protocol Adapter that has Encryption
//          turned ON as well as ANO Encryption.
// *Action: Turn OFF either ANO Encryption or the Protocol Adapter Encryption
//          if possible. Refer to Oracle Advanced Security Administrator's 
//          Guide on how to do this.
/
12699, 00000, "Native service internal error"
// *Cause:  An internal error occurred in the native services component.
// *Action: Enable tracing to determine the exact error. Contact Oracle
//          Customer Support.
/
/
/ This line is an OSN Magic Cookie. Don't eat it.
/ All new error messages up to 12699 ___MUST___ be placed in this file
/ above and before and preceding the preceding Magic Cookie line.
/
/ This line is an OSN Magic Cookie. Don't eat it. Last NS error in 2.0.9.
/
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
/
/ 12700 - 12999: Reserved.
/
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////


