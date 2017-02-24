#!/usr/bin/perl

require LTI;

LTI::loadAuth('auth.dat');
my $users = LTI::list("courses/20041/users", ['id', 'name', 'login_id']);
foreach my $c (@$users){
    print $c->[0], $c->[1], $c->[2], "\n";
}

#system("git log ....");
#my $result = `git log ...`;
