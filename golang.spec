%global go_version 1.24.3
%global __strip /bin/true

Name      : golang
Summary   : The Go Programming Language
Version   : %{go_version}.%{?build_number}%{!?build_number:x}
Release   : 1
BuildArch : x86_64
Packager  : PoiXson <support@poixson.com>
License   : AGPLv3+ADD-PXN-V1 and BSD and Public Domain
URL       : https://poixson.com/

BuildRequires: curl wget tar
#BuildRequires: pxn-scripts
Requires: glibc, gcc
Provides: GoLang = %{go_version}
Provides: go     = %{go_version}

Prefix: %{_datadir}/gocode
%define _rpmfilename  %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%global source_date_epoch_from_changelog 0
%define source_date_epoch 0

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.



%build
echo ; \uname -a ; echo
LATEST_GO_VERSION=$( \curl "https://go.dev/VERSION?m=text" 2>/dev/null | \head -n1 )
if [[ -z $LATEST_GO_VERSION ]]; then
	echo "Failed to get latest golang version" ; exit 1
fi
if [[ "$LATEST_GO_VERSION" != "go%{go_version}" ]]; then
	echo "Invalid latest version: $LATEST_GO_VERSION  expected: go%{go_version}" ; exit 1
fi
if [[ "$LATEST_GO_VERSION" != "go"* ]]; then
	echo "Invalid result getting latest golang version: $LATEST_GO_VERSION" ; exit 1
fi
echo -e "\nGoLang version: %{go_version}\n"
if [[ -f "%{_topdir}/../go%{go_version}.linux-amd64.tar.gz" ]]; then
	echo -n "Found existing package: "
else
	echo "Downloading package.."
	\wget -O  \
		"%{_topdir}/../go%{go_version}.linux-amd64.tar.gz"      \
		"https://go.dev/dl/go%{go_version}.linux-amd64.tar.gz"  \
			|| exit 1
fi
\cp -vf  \
	"%{_topdir}/../go%{go_version}.linux-amd64.tar.gz"  \
	"%{_topdir}/BUILD/go.tar.gz"                      \
		|| exit 1



%install
echo
echo "Install.."
# create dirs
%{__install} -d  \
	"%{buildroot}%{_bindir}"                \
	"%{buildroot}%{_sysconfdir}/profile.d"  \
	"%{buildroot}%{_datadir}"               \
		|| exit 1
# extract files
echo "Extracting.."
\pushd "%{buildroot}%{_datadir}/" >/dev/null || exit 1
	\tar -zx  \
		--file="%{_topdir}/BUILD/go.tar.gz"     \
		--directory="%{buildroot}%{_datadir}/"  \
		|| exit 1
	\mv  go  gocode  || exit 1
\popd >/dev/null
# copy files
\pushd  "%{_topdir}/../"  >/dev/null  || exit 1
	# profile.d
	%{__install} -m 0755  \
		"profile.sh"                                      \
		"%{buildroot}%{_sysconfdir}/profile.d/golang.sh"  \
			|| exit 1
	echo "chmodr.."
	\chmodr  0755 0644  "%{buildroot}%{_datadir}/gocode/"                        || exit 1
	\chmod   0755 -c    "%{buildroot}%{_datadir}/gocode/pkg/tool/linux_amd64/"*  || exit 1
\popd >/dev/null
# symlinks
\pushd "%{buildroot}%{_bindir}" >/dev/null || exit 1
	%{__ln} -s  "%{_datadir}/gocode/bin/go"  "go"  || exit 1
\popd >/dev/null



%files
%defattr(0644, root, root, 0755)
%license %{_datadir}/gocode/LICENSE
%license %{_datadir}/gocode/PATENTS
%doc %{_datadir}/gocode/README.md
%doc %{_datadir}/gocode/SECURITY.md
%doc %{_datadir}/gocode/VERSION
%doc %{_datadir}/gocode/go.env
# bin
%attr(0755,-,-) %{_datadir}/gocode/bin/go
%{_bindir}/go
# profile.d
%attr(0755,-,-) %{_sysconfdir}/profile.d/golang.sh
# /usr/share/gocode
%dir %{_datadir}/gocode
%{_datadir}/gocode/*
