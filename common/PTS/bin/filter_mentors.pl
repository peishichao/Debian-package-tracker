#!/usr/bin/perl -w

#    filter_mentors.pl - filter out some packages from Sources-mentors_*
#    Copyright (C) 2011 Bart Martens <bartm@knars.be>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

use strict;
use Dpkg::Version;
use SOAP::Lite;

# Work around SOAP::Lite/wget not being able to verify certs correctly
my $ca_dir = '/etc/ssl/ca-debian';
$ENV{PERL_LWP_SSL_CA_PATH} = $ca_dir if -d $ca_dir;
my $ca_debian = -d $ca_dir ? "--ca-directory=$ca_dir" : '';

sub read_page
{
	my $url = shift;
	my $page = '';

	{
		local $/ = undef;
		open INPUT, "wget $ca_debian -qO - $url |" or return '';
		$page = <INPUT>;
		close INPUT;
	}

	return $page;
}

my $buginfo_success = 0;
my $buginfo = {};

eval
{
	my $soap = SOAP::Lite->uri('Debbugs/SOAP')->proxy('https://bugs.debian.org/cgi-bin/soap.cgi');
	my $buglist = $soap->get_bugs(package=>'sponsorship-requests',status=>'open')->result();
	while ( my @slice = splice(@$buglist, 0, 500) )
	{
		my $tmp = $soap->get_status(@slice)->result;
		%$buginfo = (%$buginfo, %$tmp);
	}
	$buginfo_success = 1;
};

if( $buginfo_success == 0 )
{
	print STDERR "$0: warning: failed to read bts info via soap interface, continuing without\n";
}

my %rfsbug;

foreach my $bug ( keys %$buginfo )
{
	my $subject = $buginfo->{$bug}->{'subject'};

	$subject =~ s/(\d)(\[ITP\])/$1 $2/;
	$subject =~ s/^\[sponsorship-requests\]\s+//;
	$subject =~ s/^sponsorship-requests:\s+//;

	if( $subject =~ /^RFS: (\S+)\/(\S+).*$/ )
	{
		$rfsbug{$1} = $bug;
		next;
	}

	#print STDERR "$0: warning: title of RFS $bug does not match template\n";
}

my %mentorsneedssponsor;

my $page = read_page( "http://mentors.debian.net/packages/index" );

my $re = '<tr class="pkg-list">'
	. '\s*'
	. '<td class="lines"><a href="/package/[^"]+">([^<]+)</a></td>'
	. '\s*'
	. '<td class="lines">(.*?)</td>'
	. '\s*'
	. '<td class="lines">(.*?)</td>'
	. '\s*'
	. '<td class="lines">.*?</td>'
	. '\s*'
	. '<td class="lines">\s*(Yes|No)\s*</td>'
	. '\s*'
	. '</tr>';

if( $page !~ /$re/ )
{
	print STDERR "$0: warning: failed to read mentors packages index, continuing without\n";
}

while( $page =~ s,$re,,s )
{
	$mentorsneedssponsor{$1} = $4;
}

if( $page =~ /pkg-list/ )
{
	print STDERR "$0: warning: mentors packages index not fully parsed, continuing anyway\n";
}

my $keys_mentorsneedssponsor = keys %mentorsneedssponsor;

if( $keys_mentorsneedssponsor == 0 )
{
	print STDERR "$0: warning: mentors packages index appears empty, continuing without\n";
}

my %unstable;

foreach my $component ( "main", "contrib", "non-free" )
{
	my $package;
	my $version;

	open INPUT, "<Sources-unstable_$component" or die;
	while(<INPUT>)
	{
		chomp;

		$package = $1 if( /^Package: (.*)$/ );
		$version = $1 if( /^Version: (.*)$/ );

		if( /^$/ )
		{
			$unstable{$package} = $version
				if( ! defined $unstable{$package}
				or Dpkg::Version::version_compare( $unstable{$package}, $version ) < 0 );

			$package = undef;
			$version = undef;
		}
	}
	die if( defined $package );
	close INPUT;
}

my %experimental;

foreach my $component ( "main", "contrib", "non-free" )
{
	my $package;
	my $version;

	open INPUT, "<Sources-experimental_$component" or die;
	while(<INPUT>)
	{
		chomp;

		$package = $1 if( /^Package: (.*)$/ );
		$version = $1 if( /^Version: (.*)$/ );

		if( /^$/ )
		{
			$experimental{$package} = $version
				if( ! defined $experimental{$package}
				or Dpkg::Version::version_compare( $experimental{$package}, $version ) < 0 );

			$package = undef;
			$version = undef;
		}
	}
	die if( defined $package );
	close INPUT;
}

my %seen;

sub process_block
{
	my $package = shift;
	my $version = shift;
	my $block = shift;

	return if( defined $seen{$package}{$version} );
	$seen{$package}{$version} = 1;

	return if( defined $unstable{$package} and $unstable{$package} eq $version );
	return if( defined $experimental{$package} and $experimental{$package} eq $version );

	return if( defined $unstable{$package}
		and $version !~ /~bpo\d+\+\d+$/
		and $version !~ /(squeeze|wheezy|jessie)/
		and Dpkg::Version::version_compare( $unstable{$package}, $version ) > 0 );

	return if( ! defined $mentorsneedssponsor{$package} and $keys_mentorsneedssponsor > 0 );

	return if( defined $mentorsneedssponsor{$package} and $mentorsneedssponsor{$package} eq "No"
		and ! defined $rfsbug{$package} and $buginfo_success == 1 );

	print OUTPUT "$block\n";
}

foreach my $component ( "main", "contrib", "non-free" )
{
	my $package;
	my $version;
	my $block = "";

	open INPUT, "<Sources-mentors_$component" or die;
	open OUTPUT, ">Sources-mentors_${component}_new" or die;
	while(<INPUT>)
	{
		chomp;

		$package = $1 if( /^Package: (.*)$/ );
		$version = $1 if( /^Version: (.*)$/ );

		if( ! /^$/ )
		{
			$block .= "$_\n";
		}
		else
		{
			process_block $package, $version, $block;

			$package = undef;
			$version = undef;
			$block = "";
		}
	}
	if( defined $package )
	{
		process_block $package, $version, $block;
	}
	close INPUT;
	close OUTPUT;
}

