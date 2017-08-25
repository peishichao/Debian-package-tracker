#!/bin/sh

# Copyright: © 2002-2012 Raphaël Hertzog <hertzog@debian.org>
# Copyright: © 2007-2009 Stefano Zacchiroli <zack@debian.org>

# This file is distributed under the terms of the General Public License
# version 2 or (at your option) any later version.

umask 002
set -e

if [ -d "../incoming" ]; then
    root=$PWD/..
elif [ -d "incoming" ]; then
    root=$PWD
else
    root=/srv/packages.qa.debian.org/www
fi

dir=/etc/ssl/ca-debian
test -d $dir && ca_debian="--ca-directory=$dir"
dir=/etc/ssl/ca-global
test -d $dir && ca_global="--ca-directory=$dir"

mirror="http://deb.debian.org/debian"
security="http://security.debian.org"
piuparts="https://piuparts.debian.org"

# Allow local-override
if [ -e $root/etc/update_incoming.conf ]; then
    . $root/etc/update_incoming.conf
fi

official_distros="oldstable stable testing unstable experimental"
pu_distros="oldstable-updates oldstable-proposed-updates stable-updates stable-proposed-updates testing-proposed-updates"
security_distros="oldstable stable testing"
backports_distros="oldstable-backports oldstable-backports-sloppy stable-backports"

if [ -z "$disable_oldoldstable" ]; then
    official_distros="oldoldstable $official_distros"
    pu_distros="oldoldstable-updates oldoldstable-proposed-updates $pu_distros"
    security_distros="oldoldstable $security_distros"
    backports_distros="$backports_distros"
fi

cd $root/incoming

nice_copy() {
    # $1: path / $2: filename
    if [ -e $1 ]; then
	if [ ! -e $2 -o $1 -nt $2 ]; then
	    cp --remove-destination $1 $2
	fi
	if [ -n "$ret" ] ; then return 0 ; fi
    else
	if [ -n "$ret" ] ; then return 1 ; else echo "$1 doesn't exist, $2 is stale now" ; fi
    fi
}
nice_wget() {
    # $1: url / $2: filename
    # For timestamping to work, copy to .new (not link, wget will not break
    # the link)
    test -e $2 && cp -a $2 $2.new || true
    if wget -T 180 -t 3 -U pts -q -O $2.new $3 "$1" ; then
        mv -f $2.new $2
        if [ -n "$ret" ] ; then return 0 ; fi
    else
        rm -f $2.new
        if [ -n "$ret" ] ; then return 1 ; else echo "Downloading $1 failed, $2 is stale now" ; fi
    fi
}
get() {
    # $1: url-or-path / $2: filename
    if echo $1 | grep -q ^/; then
	nice_copy $1 $2
    else
        if [ -n "$3" ] ; then
            ca="$3"
        else
            ca="$ca_debian"
        fi
        nice_wget $1 $2 $ca
    fi
}

get_src() {
    # $1: url-or-path / $2: filename
    ret=1
    if echo $1 | grep -q ^/; then
        nice_copy $1.xz $2.xz ||
        nice_copy $1.gz $2.gz ||
        nice_copy $1 $2 ||
        echo "Downloading $1 failed, $2 is stale now"
    else
        if [ -n "$3" ] ; then
            ca="$3"
        else
            ca="$ca_debian"
        fi
        nice_wget $1.xz $2.xz $ca ||
        nice_wget $1.gz $2.gz $ca ||
        nice_wget $1    $2    $ca ||
        echo "$1 doesn't exist, $2 is stale now"
    fi
    unset ret
}

nice_redirect_to() {
  # $1 : target file
  # $2-... : shell command
  dest="$1"
  shift
  if [ -f "$dest" ] ; then
    mv -f "$dest" "$dest.bak"
  fi
  $* > "$dest" || (echo "Failure while executing $* . Continuing ..." ; cp "$dest.bak" "$dest")
}

# Download all Sources
for comp in main contrib non-free
do
    for dist in $official_distros $pu_distros $backports_distros; do
      get_src $mirror/dists/$dist/$comp/source/Sources \
	Sources-${dist}_$comp
    done
    for dist in $security_distros ; do
      get_src $security/dists/$dist/updates/$comp/source/Sources \
	Sources-security-${dist}_$comp
    done
done
for comp in main contrib non-free
do
    get_src http://mentors.debian.net/debian/dists/unstable/$comp/source/Sources \
        Sources-mentors_$comp
done

# Download update_excuses.html
get https://release.debian.org/britney/update_excuses.html.gz \
    update_excuses.html.gz

# Download DM permissions
get https://ftp-master.debian.org/dm.txt dm.txt

# Download PTS subscription count
get https://packages.qa.debian.org/data/pts-subscription-count.txt \
  count.txt

# Download override disparities
get https://qa.debian.org/data/ftp/override-disparities.unstable \
    override-disparities.unstable
get https://qa.debian.org/data/ftp/override-disparities.experimental \
    override-disparities.experimental

# Download lintian.d.o run info
#get https://lintian.debian.org/lintian.log lintian.log
get https://lintian.debian.org/qa-list.txt lintian.qa-list.txt

# Download builddlogcheck info
#get https://qa.debian.org/bls/logcheck.txt logcheck.txt
get https://qa.debian.org/bls/logcheck.txt logcheck.txt

# Download clang build info
get http://clang.debian.net/pts.php clang.txt

# Download bugs summary
get https://udd.debian.org/cgi-bin/bugs-binpkgs-pts.cgi bugs.txt
get https://udd.debian.org/cgi-bin/ddpo-bugs.cgi bugs-src.txt
nice_redirect_to bugs.help.txt $root/bin/tagged_bugs.py "help"
nice_redirect_to bugs.newcomer.txt $root/bin/tagged_bugs.py "newcomer"
piuparts_distros="sid lenny2squeeze"
for distro in $piuparts_distros ; do
  get $piuparts/$distro/sources.txt piuparts-$distro.txt
done

# Download debcheck lists
DCROOT=https://qa.debian.org/data/debcheck/result
for distro in $official_distros ; do
    [ "$distro" != "experimental" ] || continue
    get $DCROOT/$distro/lists/ALL-pkglist debcheck-$distro
done

# Download the translation status of packages
get https://i18n.debian.org/l10n-pkg-status/pkglist l10n-status.txt

# Get wnpp information
get https://qa.debian.org/data/bts/wnpp_rm wnpp_rm

# Get Debian patch information
get https://sources.debian.net/patches/api/list/ patches.debian $ca_global

# Get derivatives patch information
get http://deriv.debian.net/sources.patches.pts patches.derivs

# get patches from ubuntu
get https://patches.ubuntu.com/PATCHES patches.ubuntu $ca_global
# get packages version in Ubuntu
get https://udd.debian.org/cgi-bin/ubuntupackages.cgi versions.ubuntu
# get bugs in Ubuntu
get https://udd.debian.org/cgi-bin/ubuntubugs.cgi bugs.ubuntu

# download LowThresholdNmu list
get 'https://wiki.debian.org/LowThresholdNmu?action=raw' \
    low_threshold_nmu.txt

# ongoing transitions
get https://ftp-master.debian.org/transitions.yaml \
    transitions.yaml
get https://release.debian.org/transitions/export/packages.yaml \
    transitions-packages.yaml

# release goals
# no longer exist
#get https://release.debian.org/testing/goals.yaml release-goals.yaml
#get https://udd.debian.org/pts-release-goals.cgi \
#    release-goals-bugs.yaml

# download the list of packages indexed by svnbuildstat
#get http://svnbuildstat.debian.net/packages/flatlist \
#    svnbuildstat_list.txt

# download watch file information
get https://udd.debian.org/cgi-bin/upstream-status.json.cgi dehs.json
# needs UDD replacement:
get https://qa.debian.org/watch/watch-avail.txt watch-avail.txt
get https://qa.debian.org/watch/watch-broken.txt watch-broken.txt

# download list of security issues
get https://security-tracker.debian.org/tracker/data/pts/1 \
    security_issues.txt

# download NEW queue info
get https://ftp-master.debian.org/new.822 new.822

# retrieve package descriptions from UDD
get https://qa.debian.org/data/pts/shortdesc.txt shortdesc.txt
get https://qa.debian.org/data/pts/longdesc.json longdesc.json

# download the Debian fonts review
#FIXME: re-enable when this is updated again
get https://pkg-fonts.alioth.debian.org/review/debian-font-review.yaml debian-font-review.yaml

# download the Debian URL Checker results
get http://duck.debian.net/static/sourcepackages.txt duck.txt

# download the list of packages with screenshots
get https://screenshots.debian.net/json/packages screenshots-packages.json $ca_global

get https://dedup.debian.net/static/ptslist.txt dedup.txt $ca_debian

nice_redirect_to upstream-info.txt svn ls -R svn://svn.debian.org/svn/collab-qa/packages-metadata

# testing autoremoval info
get https://udd.debian.org/cgi-bin/autoremovals.yaml.cgi autoremovals.yaml

get https://ci.debian.net/data/status/unstable/amd64/packages.json testing.json $ca_global

# What more ?

# Decompress all files
for file in *.gz; do
    gzip -d -c $file > ${file%%.gz}.new
    touch -r $file ${file%%.gz}.new
    mv -f ${file%%.gz}.new ${file%%.gz}
done
for file in *.xz; do
    xz -d -c $file > ${file%%.xz}.new
    touch -r $file ${file%%.xz}.new
    mv -f ${file%%.xz}.new ${file%%.xz}
done

# filter out some packages from Sources-mentors_*
$root/bin/filter_mentors.pl
mv Sources-mentors_main_new Sources-mentors_main
mv Sources-mentors_contrib_new Sources-mentors_contrib
mv Sources-mentors_non-free_new Sources-mentors_non-free


