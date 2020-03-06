#!/usr/bin/env perl

use strict;
use warnings;
use diagnostics;
use feature 'say';
use feature "switch";
use v5.26.1;

#comment

print "Hello World\n";
my $name = 'Hoang Duy Tran';

my ($age, $street) = (40, '123 Main Street');

my $my_info = "$name lives on \"$street\"\n";

$my_info = qq{$name lives on "$street"\n};

print $my_info;
my $bunch_on_info = <<"END";
This is a
bunch of information
on multiple lines
END

say $bunch_on_info;

my $big_int = 182485684738432947;

# %c : character
# %s : string
# %d : decimal
# %u : unsigned
# %f : float
# %e : float, sienctific notation

printf("%u \n", $big_int + 1);

my $big_float = .10000000000000001;

printf("%.16f \n", $big_float + 1);

my $first = 1;
my $second = 2;

($first, $second) = ($second, $first);

say "first=$first, second=$second";
