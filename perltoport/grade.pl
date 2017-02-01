#!/usr/bin/perl
#
#   Author: Dov Kruger
#
#   Purpose
#   unzip  homework from Canvas
#   TODO: Check contents of each students directory and reject if contents do not match requirements
#   TODO: Check if code is trivial
#   Compile code and issue base grade if it does not compile
#
#
#
#   Usage: grade.pl gradefile.csv HWxx.zip
#
use File::Copy;
use Text::CSV;
use File::Path;
use Cwd;

my $csv = Text::CSV->new({ sep_char => ',' });


use strict;
my $n = @ARGV;
if ($n < 2) {
    die "Usage: grade.pl courseGrade.csv hw##.zip\n";
}
my $courseGrade = $ARGV[0];
my $zipName = $ARGV[1];
my $datafile = $ARGV[2];
if ($datafile) { #todo: this does not support windows well
    $datafile = getcwd() . '/' . $datafile;
    print $datafile;
}
if ($zipName !~ /(HW\w+)/i) { # case insensitive, accept hw or HW
    die ("Error, filename must contain a valid HW name\n");
}


rmtree("temp");
mkdir("temp");
chdir("temp");
system("unzip ../$zipName");

my $hw = $1;
my @files = <*>;
my $cmd;
my $run;
my $realFileName;

#my $courseGrade = "Grades-EE810.csv";
my $uploadName = "../810upload".$hw;
open (GRADECSV, "<../$courseGrade") || die("can't open course grade file: $courseGrade\n");
my @lines = <GRADECSV>;
close(GRADECSV);
open (GRADESUPLOAD, ">$uploadName.csv") || die("Can't Create file $uploadName.csv");
my @titles;
if ($csv->parse($lines[0])) {
    @titles = $csv->fields();
}
my $index;
for (my $i = 4; $i <= $#titles; $i++) {
    if ($titles[$i] =~ /$hw/i) {
    	$index = $i;
        last;
    }
}

my @cols = (0..4,$index);
my %studentMap = ();
print GRADESUPLOAD  join(",", @titles[(@cols)]), "\n";
if ($csv->parse($lines[1])) {
    my @fields = $csv->fields();
    print GRADESUPLOAD join(",", @fields[(@cols)]), "\n";
}
for (my $i = 2; $i <= $#lines; $i++) {
    if ($csv->parse($lines[$i])) {
	my @student = $csv->fields();
	#print join("\t", @student), "\n";
        $studentMap{$student[2]}=\@student[(@cols)];
    }
}

foreach my $line(@lines) {
}
open (GRADEFILE, ">../grade.txt") || die("Can't open grade file\n");

foreach my $file (@files) {
    my ($studentName, $id, $unknown, $origFilename);
    if ($file !~ /([^_]*_?[^_]+)_(\d+)_(\d+)_(.*)/) {
	die("Failed on filename: $file\n");
    }
    $studentName = $1;
    $id = $2;
    $unknown = $3;
    $origFilename = $4;

    if ($origFilename =~ s/\-\d//) {
        print "Stripped submission number! $origFilename\n";
    }

    mkdir("tmp");
    chdir("tmp");
    move("../$file", "$origFilename");
    print "\n\n\nGrading student: $studentName\n";
    open (CODE, "<$origFilename") || die("can't open student file: $origFilename\n");
    while (my $line = <CODE>) {
	print $line;
    }
    close(CODE);
    if ($file =~ /\.pde$/) {
        mkdir("a");
        move($origFilename, "a/a.pde");
        $origFilename = "a";
    	$cmd = "processing-java --sketch=a --output=test --build";
    	$run = "cd test;java a";
    } elsif ($file =~/\.java/) {
        $cmd = "javac -d .";
    	$run = "java " . substr($origFilename, 0, length($origFilename)-5);
    } elsif ($file =~/\.(cc|cpp|cxx)/) {
	    $cmd = "g++ -std=c++11";
    	$run = "./a.out";
    } elsif ($file =~/\.jpg/) {
    	$cmd = "echo";
    } elsif ($file =~/\.zip/) {
	    $cmd = "unzip";
    }
    if ($cmd) {
    	$cmd .= ' "' . $origFilename . '" >log 2>log2';
    }
    my $stat = system($cmd);
    my $score;
    if ($stat == 0) {
	if ($datafile) {
	    copy("$datafile", ".");
	}
	my $runstat = system($run);
	{
	    $score=100;
	}
    } else {
	   $score = 25;
    }
    print "$studentName $id: Enter grade [$score]";
    my $TAscore = <STDIN>;
    chomp $TAscore;
    if ($TAscore ne "") {
	$score = $TAscore;
    }

    my $succeed = $stat == 0 ? 'T' : 'F';
    my $grade = "$studentName,$id,$unknown,$score\n";
    chomp($grade);
    print GRADEFILE $grade, "\n";
    my $thisStudent = $studentMap{$id};
    #print "THIS STUDENT: $thisStudent\n";
    print GRADESUPLOAD join(",", $thisStudent->[@cols]);
    chdir ("..");
    rmtree("tmp");
}
close(GRADEFILE);
close(GRADESUPLOAD);
