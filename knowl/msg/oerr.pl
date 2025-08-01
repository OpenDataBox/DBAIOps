#!/usr/bin/perl

use English;
use strict;
use File::Basename;
use File::Spec::Functions;

my $WantTrace = 0;

# Check script usage
if (@ARGV != 2) {
    die usage_string();
}


#
# Pickup the command line arguments
my $Msg_File = @ARGV[0];
my $Code = @ARGV[1];


if ($Code =~ s/[^0-9]//g) {
    die "Non-numeric characters in error message code\n";
}

$Code =~ s/^0*//;                    # strip off any leading 0's
print "Code (trimmed): $Code\n" if $WantTrace;

#
# The message file searched is always the US English file
#my $Msg_File = catfile($ENV{ORACLE_HOME}, $Component, "mesg", $Facility . "us.msg"); 


if (! open MSGFILE, "<$Msg_File") {
    die "oerr: Cannot access the message file $Msg_File\n", 
        "$OS_ERROR\n";
}

    
#
# Search the message file for the error code, printing the message text
# and any following comment lines, which should give the cause and action
# for the error.
my $found = 0;

while (<MSGFILE>) {
    if ($found) {
        if (/^\/\//) {
            print;
        } else {
            last;
        }
    }

    if (/^0*$Code[^0-9]/) {
        $found = 1;
        print;
    }
}

exit 0;


sub usage_string {
    return "Usage: oerr facility error\n\n",
    "Facility is identified by the prefix string in the error message.\n",
    "For example, if you get ORA-7300, \"ora\" is the facility and \"7300\"\n",
    "is the error.  So you should type \"oerr ora 7300\".\n\n",
    "If you get LCD-111, type \"oerr lcd 111\", and so on.\n";
}
