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
150,    0, "Error in comma-separated options string parsed: '%s'."
151,    0, "Trailing comma found.\nNote, the comma-separated options string should not contain spaces."
152,    0, "Error in comma delimited entry '%s'."
153,    0, "ATTRIBUTE=VALUE expected."
160,    0, "The attribute '%s' is not supported in this resource type." 
161,    0, "The resource profile template's attribute '%s' has an error." 
162,    0, "The file '%s' exists. Creation is cancelled."
163,    0, "Cannot open the file '%s'."
164,    0, "The file '%s' is locked by another process."
165,    0, "Cannot get a read lock on the file '%s'."
166,    0, "Cannot read the file '%s'."
167,    0, "Cannot remove the action script '%s'."
168,    0, "Cannot create the backup file."
169,    0, "Cannot remove the resource '%s'."
170,    0, "The resource '%s' doesn't exist."
171,    0, "The action script '%s' cannot be created."
172,    0, "The parameter '%s' cannot be interpreted by CRSD."
173,    0, "Invalid command line option."
174,    0, "Resource name cannot exceed 256 characters."
175,    0, "Resource type '%s' either doesn't exist or cannot be accessed."
178,    0, "The pathname is incorrect."
180,    0, "Resource '%s' validation failed."
181,    0, "Cannot access the resource profile '%s'."
182,    0, "RTI error: '%s'"
184,    0, "Cannot communicate with the CRS daemon."
// *Cause:  The CRS daemon on the local node is either not running or there was
//          an internal communication error with the CRS daemon.
// *Action: Check if the CRS daemon process is running on the local node.
185,    0, "Resource template '%s' not found."
186,    0, "There is a switch conflict in the type definition files used by crs_profile\nwhen creating your '%s' type resource. Please make sure each attribute\nswitch is defined only once.\n"
187,    0, "Switch '%s' is used by the following attributes: '%s'."
199,    0, "CRS general warning. No reason is provided."
200,    0, "CRS general failure. No reason is provided."
201,    0, "Catch all failure. No reason is provided."
202,    0, "No resources are registered."
203,    0, "Reason is to be supplied."
204,    0, "One or more attributes not found for resource '%s'"
210,    0, "Could not find resource '%s'."
// *Cause:  An attempt was made to operate on a resource that is not 
//          registered.
// *Action: Check if the resource is registered using crs_stat.
211,    0, "Resource '%s' has already been registered."
// *Cause:  An attempt was made to register a resource that is already
//          registered.
// *Action: Check if the resource is registered using crs_stat.
212,    0, "Resource '%s' is not registered."
213,    0, "Could not register resource '%s'."
// *Cause:  There was an internal error while registering the resource.
// *Action: Check the CRS daemon log file.
214,    0, "Could not unregister resource '%s'."
// *Cause:  There was an internal error while unregistering the resource.
// *Action: Check the CRS daemon log file.
215,    0, "Could not start resource '%s'."
// *Cause:  There was an internal error while starting the resource.
// *Action: Check the CRS daemon log file.
216,    0, "Could not stop resource '%s'."
// *Cause:  There was an internal error while stopping the resource.
// *Action: Check the CRS daemon log file.
217,    0, "Could not relocate resource '%s'."
// *Cause:  There was an internal error while relocating the resource.
// *Action: Check the CRS daemon log file.
218,    0, "Could not restart the resource '%s' on the original node."
// *Cause:  There was an internal error while restarting the resource.
// *Action: Check the CRS daemon log file.
219,    0, "Could not update resource '%s'."
// *Cause:  There was an internal error while updating the resource.
// *Action: Check the CRS daemon log file.
220,    0, "Resource '%s' has invalid resource profile."	
// *Cause: Invalid attributes in the resource profile.
// *Action: Run crs_profile -validate to identify the invalid attributes.
221,    0, "Resource '%s''s action script cannot be found."
// *Cause: The action script has been deleted from the file system.
// *Action: Run crs_stat -p to determine the action script location and to check for its existence.
222,    0, "Resource '%s' has dependency error."
223,    0, "Resource '%s' has placement error."
// *Cause: There was no host available to on which failover/start the resource
//         based on the Placement Policy for the resource.
// *Action: Check the target host for the resource and restart the resource
//          using the crs_start command.    

/
/ added for 10i
224,	0, "Warning: failed to redirect I/O"
225,    0, "Resource name not specified"
226,    0, "Warning: memory allocation"
227,    0, "Invalid resource name"
228,	0, "Invalid host"
229,    0, "Invalid combination of flags"
/ end 10i additions
/
230,    0, "Member '%s' is not in the cluster."
// *Cause: The hostname was not found in the cluster.
// *Action: Check the hostnames in the cluster.
231,    0, "Operation is invalid for this type of resource."
232,    0, "Cluster member is down.  Cannot perform operation."
// *Cause:  The node on which CRS is attempting to start the resource is down.
// *Action: Start the node and retry the operation.
233,    0, "Resource or relatives are currently involved with another operation."
// *Cause: Another CRS daemon was operating on the same resource.
// *Action: Wait for a minute and try the command or operation again.
234,    0,  "Attribute not defined in profile"
/
/ added for 10i
/
239,	0,  " Invalid command"
240,	0,  " Piped channel output error"
241,	0,  " Invalid directory path."
242,	0,  " ACL information is not available"
243,	0,  " default setting unavailable"
244,	0,  " registration allow/deny information is not available"
245,	0,  " User doesn't have enough privilege to perform the operation"
246,	0,  " User id is invalid"
247,	0,  " User name or group name is invalid"

248,	0,  " Acl operation failed"
249,	0,  " Authentication failure. "
250,	0,  " Configuration unsuccessful. Try again or restart CRSD."
251,	0,  " CRS configuration file missing."
252,	0,  " CRS configuration file syntax error."
/
253,	0,  " CRS configuration error, the CRS default directory is not set in OCR. "
// *Cause:   The OCR key which contains the user default CRS key is not 
//           initialised.
// *Action:  Check the CRS configuration. If necessary reinstall CRS.
/
254,	0,  " authorization failure"
// *Cause:  The user permissions were insufficient to operate on the
//          resource.
// *Action: Check the permissions associated with the resource using 
//          crs_getperm.
255,	0,  " CRSD is not running in privileged mode. Insufficient permissions to run this command. "
// *Cause:  The CRS daemon was not running as the privileged user.
// *Action: Check if the CRS daemon is running as root (Unix) or Administrator 
//          (Windows).
256,    0,  "Username conflicts with the owner of the resource."
// *Cause:  An attempt was made to give separate user level permissions for the
//          owner of the resource.
// *Action: Check the owner of the resource and the user being given 
//          permissions.
257,    0,  "Groupname conflicts with the primary group of the resource."
// *Cause:  An attempt was made to give separate group level permissions for 
//          the primary group of the resource.
// *Action: Check the primary group of the resource and the group being given 
//          permissions.
258,    0,  "Invalid ACL string format."
// *Cause:  An invalid permission string (ACL) was supplied.
// *Action: Check the syntax of the permission string (ACL).

259,    0,  "Owner of the resource does not belong to the group."
// *Cause:  The owner of the resource does not belong to the expected group.
// *Action: If this resource is owned by the root user, check if the root user
//          belongs to the dba group.

/
/
301,    0, "'%s': Hostname can be between 2 and %d alphanumeric or '.' or '-' characters."
302,    0, "'%s': Hostname must consist of alphanumeric or '.' or '-' characters."
303,    0, "'%s': Hostname must begin with a letter."
304,    0, "'%s': Short Hostname can be between 2 and %d alphanumeric or '-' characters."
305,     0, "Cluster Information not available."
306,     0, "\tLook for '%s' among %d cluster members."
307,     0, "Warning: '%s' is not available."
308,     0, "Warning: It may be among [%d] unavailable members."
309,     0, " Specify Subnet in [nnn.nnn.nnn.0] format."
310,     0, "Duplicate definition is not allowed : '%s' at line %d"
311,     0, "HOSTING_MEMBERS values are ignored for balanced placement"
312,     0, "value:  ACTION_SCRIPT is at line %d"
313,     0, "'%s' at line no %d, Action Script must have read and execute permissions."
314,     0, "'%s' at line no %d, Action Script must be a file."
315,     0, "value: '%s' of the keyword: OWN_OPERATIONS is not absolute path at line no %d"
316,     0, "'%s' at line no %d, Action Script must be have read and execute permissions."
317,     0, "'%s' at line no %d, Action Script is not accessible."
318,     0, "'%s' '%s' at line no %d, Access Error"
319,     0, " 'Active Placement' is currently unsupported."
320,     0, " A required resource '%s' is not registered."
321,     0, "profile '%s' extension is not '%s'."
322,     0, "Keyvalue : '%s' for keyword : '%s' is not valid."
323,     0, "['%s'] is not a keyword at line %d."
324,     0, "'%s' is not a keyword."
/
/
/
401,    0, "Directory '%s' not found."
402,     0, "Could not make safe dir('%s')"
// *Cause: Unable to create safe directory('%s')
// *Action: Please check if you have proper permissions and sufficient space on the disk to create the directory.
403,     0, "Could not chdir to safe dir('%s')"
// *Cause: Unable to change directory to safe dir('%s')
// *Action: Please check if safe  dir exists and if you have proper permissions. 
404,     0, "Could not fork for daemon ('%s')"
405,     0, "Could not get local hostname ('%s')"
406,     0, "Could not create lock dir ('%s')"
// *Cause: Unable to create lock directory ('%s')
// *Action: Please check if you have proper permissions and sufficient space on the disk to create the directory.
407,     0, "Another CRSD may be running, could not obtain lock file '%s'."
// *Cause: Unable to obtain lock file as another CRSD may be running 
// *Action: Please stop the existing CRSD before attempting to start CRSD again.
408,     0, "Could not send application restart request to CRSD"
409,     0, "Could not send application shutdown request to CRSD"
410,     0, "ORACLE_HOME not set"
411,     0, "Could not init the cluster context"
412,     0, "Could not join the cluster group"

413,     0, "Could not initialize the CSS context"
// *Cause:   Unable to communicate with the cluster services.
// *Action:  Verify that the CSS Daemon is properly configured and is running.
/

414,     0, "Could not establish EVM connection"
// *Cause: Unable to communicate with EVM daemon
// *Action: Run the 'crsctl check evmd' command to determine whether EVM daemon is properly configured and is running.

415,     0, "Could not establish dependency graph."
416,     0, "Could not create UI connection"
417,     0, "Fixed port %d in use"
418,     0, "Error trying to portmap port %d"
419,     0, "All reserved ports in use"

// OCR Related Messages 450-470
451,	0,  " CRS configuration error, unable to initialize OCR. "
// *Cause:   The OCR that contains information about the CRS configuration
//           is unavailable.
// *Action:  Check the CRS configuration. If necessary reinstall CRS.
/
452,	0,  " CRS configuration error, unable to find CRSD Connection Information in OCR. "
// *Cause:   The OCR key which contains the user default CRSD connection is not
//           initialised.
// *Action:  Check the CRS configuration. If necessary reinstall CRS.
/
453,	0,  " CRS configuration error, unable to find Instance Information in OCR. "
// *Cause:   The OCR key which contains the Instance's information is not
//           initialised.
// *Action:  Add the instance using srvctl.
/

// CSS Related Messages 471-500
471,     0, "Node number is not found"
// *Cause:   Cluster Services is unable to retrieve the node name
// *Action:  Verify your cluster installation, including any vendor
//           cluster ware. If necessary reinstall the cluster.
/

472,     0, "Node name is not found"
// *Cause:   Cluster Services is unable to retrieve the node name
// *Action:  Verify your cluster installation, including any vendor
//           cluster ware. If necessary reinstall the cluster.
/

// EVM Related messages
501, 0, "Invalid file descriptor in IO_Dispatcher, cannot recover ('%s')"
503, 0, "Connected to Montior '%s', subscribed to %d resources."
/
/ EVMMgr messages
/
504, 0, "Couldn't connect to EVMD.  Reconnecting in %d seconds."
505, 0, "Lost connection to EVMD.  Reconnecting in %d seconds."
506, 0, "Couldn't connect to EVMD for posting."
507, 0, "Error posting EVM Event (error=%d)."
508, 0, "Error subscribing to EVM events."


/
/ From Placement Policy
/
1001, 0, "Unknown placement policy name: '%s'\n\"Balanced\" used"
1002, 0, "Resource '%s' is already running on member '%s'"
1003, 0, "Target member should not be in the exclusion list"
1004, 0, "Trying to start on a dead member ..."
1005, 0, "Failed to get required resources"
// *Cause:  There was an internal error while evaluating the required 
//          resources for the subject resource.
// *Action: Check if the status of any resource is UNKONOWN using crs_stat -t.
1006, 0, "No more members to consider"
// *Cause:  There was no host found on which to start the resource based on 
//          the placement policy. 
// *Action: Check the placement policy and the required resources for the
//          subject resource.
1007, 0, "Failed after successful dependency consideration"
// *Cause:  There was no host found on which to start the resource based on 
//          the placement policy. 
// *Action: Check the placement policy and the required resources for the
//          subject resource.
1008, 0, "Resource '%s' is not relocatable (current and target state not running)"
1009, 0, "Resource '%s' is already running on member '%s'"
// *Cause:  An attempt was made to start a resource on a host while it is 
//          already running on that host.
// *Action: This is an insignificant error. Check the operation being 
//          performed. 
1011, 0, "Trying to relocate to a dead member ..."
1012, 0, "Failed to get connected resources"
1015, 0, "Failed to get resources depending on this resource"
1016, 0, "Resources depending on '%s' are running"
1017, 0, "Resource %s (%s) is not available on %s"
1018, 0, "Resource %s (%s) is already running on %s"
1019, 0, "Resource %s (%s) cannot run on %s"
1022, 0, "Resource %s (%s) is running on %s"
1023, 0, "Trying to relocate a non-runnable resource '%s'?"
1024, 0, "Failed to failover any subset of the connected resources to '%s'"
1025, 0, "Trying to start a non-runnable resource '%s'?"
1026, 0, "Trying to stop a non-runnable resource '%s'?"
1027, 0, "Resource '%s' cannot be failed over (wrong state)"
1028, 0, "Dependency analysis failed because of:\n'%s'"
/
/ From CRSD
/

2001, 0, "User does not have permission to start CRSD."
// *Cause: Unable to start CRSD due to insufficent permissions 
// *Action: Start CRSD as a privileged user.
2002, 0, "Directory '%s' not found."
2003, 0, "CRSD exiting. '%s'."
2004, 0, "Could not fork background process."
2005, 0, "Could not get hostname."
2006, 0, "Another CRSD may be running, could not obtain lock file '%s'." 
2007, 0, "Could not communicate with EVM."
// *Cause: Unable to communicate with EVM daemon
// *Action: Run the 'crsctl check evmd' command to determine whether EVM daemon is properly configured and is running.
2008, 0, "CRSD can not create UI socket."
2009, 0, "CRSD can not create message socket."
2010, 0, "portmap error, mapping E2E on port %d."
2011, 0, "All network reserved ports in use."
2012, 0, "Usage \"CRSD [-0|-1|-2]\""
2013, 0, "Unable to send '%s' request to running Manager"
2014, 0, "Could not establish dependency graph."

/
/ License checking error
2020, 0, "Software is not licensed for use on this system."
