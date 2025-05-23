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
BuildRequires: pxn-scripts
Requires: glibc, gcc
Provides: GoLang = %{go_version}
Provides: go     = %{go_version}

Prefix: %{_datadir}/gocode
%define _rpmfilename  %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%global source_date_epoch_from_changelog 0
%define source_date_epoch 0

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.



### Build ###
%build
echo -e "\nBuild..\n"$( \uname -a )"\n"
LATEST_GO_VERSION=$( \curl "https://go.dev/VERSION?m=text" 2>/dev/null | \head -n1 )
if [[ -z $LATEST_GO_VERSION ]]; then
	echo -e "\nFailed to get latest golang version\n" ; exit 1
fi
if [[ "$LATEST_GO_VERSION" != "go%{go_version}" ]]; then
	echo -e "\nInvalid latest version: $LATEST_GO_VERSION  expected: go%{go_version}\n" ; exit 1
fi
if [[ "$LATEST_GO_VERSION" != "go"* ]]; then
	echo -e "\nInvalid result getting latest golang version: $LATEST_GO_VERSION\n" ; exit 1
fi
echo -e "\nGoLang version: %{go_version}\n"
if [[ -f "%{_topdir}/../go%{go_version}.linux-amd64.tar.gz" ]]; then
	echo -e "\nFound existing package\n"
else
	echo -e "\nDownloading package..\n"
	\wget -O  \
		"%{_topdir}/../go%{go_version}.linux-amd64.tar.gz"      \
		"https://go.dev/dl/go%{go_version}.linux-amd64.tar.gz"  \
			|| exit 1
fi
\cp -vf  \
	"%{_topdir}/../go%{go_version}.linux-amd64.tar.gz"  \
	"%{_topdir}/BUILD/go.tar.gz"                      \
		|| exit 1



### Install ###
%install
echo -e "\nInstall..\n"
# create dirs
%{__install} -d  \
	"%{buildroot}%{_bindir}"                     \
	"%{buildroot}%{_datadir}"                    \
	"%{buildroot}%{_sysconfdir}/profile.d"       \
	"%{buildroot}%{_datadir}/licenses/%{name}/"  \
	"%{buildroot}%{_datadir}/doc/%{name}/"       \
		|| exit 1
# extract files
echo -e "\nExtracting..\n"
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
\popd >/dev/null
\pushd  "%{buildroot}%{_datadir}/gocode/"  >/dev/null  || exit 1
	# license
	%{__install} -m 0755  \
		"LICENSE"            \
		"PATENTS"            \
		"%{_topdir}/BUILD/"  \
			|| exit 1
	# docs
	%{__install} -m 0755  \
		"README.md"          \
		"SECURITY.md"        \
		"VERSION"            \
		"go.env"             \
		"%{_topdir}/BUILD/"  \
			|| exit 1
\popd >/dev/null
# chmod
echo -e "\nchmodr.."
\chmodr  0755 0644  "%{buildroot}%{_datadir}/gocode/"                        || exit 1
\chmod   0755 -c    "%{buildroot}%{_datadir}/gocode/pkg/tool/linux_amd64/"*  || exit 1
# symlinks
\ln -svf  "%{_datadir}/gocode/bin/go"  "%{buildroot}%{_bindir}/go"  || exit 1



%files
%defattr(0644, root, root, 0755)
%license LICENSE
%license PATENTS
%doc README.md
%doc SECURITY.md
%doc VERSION
%doc go.env
# /usr/share/gocode
%dir %{_datadir}/gocode
%{_datadir}/gocode/*
# bin
%{_bindir}/go
%attr(0755,-,-) %{_datadir}/gocode/bin/go
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/addr2line
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/asm
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/buildid
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/cgo
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/compile
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/covdata
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/cover
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/doc
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/fix
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/link
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/nm
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/objdump
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/pack
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/pprof
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/preprofile
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/test2json
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/trace
%attr(0755,-,-) %{_datadir}/gocode/pkg/tool/linux_amd64/vet
# profile.d
%attr(0755,-,-) %{_sysconfdir}/profile.d/golang.sh
