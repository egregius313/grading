#!/usr/bin/perl
package LTI;

#
# author: Dov Kruger
# Jan. 26. 2016
# Canvas LTI Module
# access canvas using LTI
# currently the method of gaining authentication is manual
# save out the user's authentication, store in a file, and load that to run
# TODO: add full oauth authentication to allow any user to run 
# with their permissions
#
use strict;
use JSON::Parse 'parse_json';
use Data::Dumper;

my $auth;
my $cmd;
my $gopts;
my $url;
my $verbose = 0; # default is debugging prints are off
sub loadAuth {
    my $HOME = $ENV{"HOME"};
    open(AUTH, $HOME . '/canvas.tok') || die("can't open authentication file\n");
    $auth = <AUTH>;
    close(AUTH);
    chomp $auth;
    my $redir = $verbose ? "" : "2>/dev/null";
    my $op = "";
    $gopts = " $redir $op ";
    $cmd = "curl -H 'Authorization: Bearer $auth'";
    $url = "https://canvas.instructure.com/api/v1";
}

sub setVerbose {
    $verbose = $_[0];
}

#
# execute a curl command using the previously loaded authentication
# using the curl command defined above
# currently, maximum number of objects returned is hardcoded to 200
# if verbose is true, dump the text
sub curl {
    my ($uri, $opts) = @_;
    my $t = $cmd . $gopts . $url . '/' . $uri . '?per_page=200';
    if ($opts) {
	$t .= "&" . $opts;
    }
    if ($verbose) {
	print "CMD=", $t, "\n";
    }
    my $json = `$t`;
    if ($verbose) {
	print "JSON: ", $json, "\n\n";
    }
    return parse_json ($json);
}


#
# execute a curl put command using the previously loaded authentication
# if verbose is true, dump the text
sub put {
    my ($uri, $opts) = @_;
    my $t = $cmd . $gopts . " -X PUT " . $url . '/' . $uri;
    if ($opts) {
	$t .= "?" . $opts;
    }
    if ($verbose) {
	print "CMD=", $t, "\n";
    }
    my $json = `$t`;
    if ($verbose) {
	print "JSON: ", $json, "\n\n";
    }
    return parse_json ($json);
}


#
# execute a query specified by $path
# select the values from the JSON object that have the specified fields
# 
# returns a list of lists with the desired fields
sub list {
    my ($path, $fields) = @_;
    my $res = curl($path, 0);
    my $out = [];
    foreach my $r (@$res) {
	my $cols = [];
	foreach my $f (@$fields) {
	    push(@$cols, $r->{$f});
	}
	push(@$out, $cols);
    }
    return $out;
}

#
# execute a query specified by $path
# like list, except that for a query returning a single JSON object
# there is no array.
# returns a list of lists with the desired fields
sub getOne {
    my ($path, $fields) = @_;
    my $res = curl($path, 0);
    my $cols = [];
    foreach my $f (@$fields) {
	push(@$cols, $res->{$f});
    }
    return [ $cols ];
}

sub print {
    my ($rec, $fieldNames, $sep) = @_;
    if (!defined $sep) { $sep = ' '; }
    foreach my $r (@$rec) {
	print join($sep, @$r), "\n";
    }
}

sub printArrHash {
    my ($rec, $fieldNames, $sep) = @_;
    if (!defined $sep) { $sep = ' '; }
    foreach my $r (@$rec) {
	foreach my $f (@$fieldNames) {
	    print $r->{$f}, $sep;
	}
	print "\n";
    }
}

sub printList {
    my ($path, $fieldNames, $sep) = @_;
    my $rec = list($path, $fieldNames);
    LTI::print($rec, $fieldNames, $sep);
    return $rec;
}

1;
