#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Library functionality for FIDO 2.0, including communication with a device over USB
Summary(pl.UTF-8):	Biblioteka funkcji dla FIDO 2.0, wraz z komunikacją z urządzeniem po USB
Name:		libfido2
Version:	1.14.0
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/Yubico/libfido2/tags
Source0:	https://github.com/Yubico/libfido2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6aa04c6e9d029e595397fe026a3a03ce
URL:		https://developers.yubico.com/libfido2/
BuildRequires:	cmake >= 3.7
BuildRequires:	hidapi-devel
BuildRequires:	libcbor-devel
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	udev-devel
BuildRequires:	zlib-devel
Requires:	openssl >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides library functionality for communicating with a
FIDO device over USB as well as verifying attestation and assertion
signatures.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę funkcji do komunikacji z urządzeniami
FIDO po USB, a także weryfikowania podpisów poświadczeń i zapewnień.

%package devel
Summary:	Header files for FIDO2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FIDO2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel >= 1.1.0

%description devel
Header files for FIDO2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FIDO2.

%package static
Summary:	Static FIDO2 library
Summary(pl.UTF-8):	Biblioteka statyczna FIDO2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FIDO2 library.

%description static -l pl.UTF-8
Biblioteka statyczna FIDO2.

%prep
%setup -q

%build
install -d build
cd build
# note: exects CMAKE_INSTALL_LIBDIR relative to prefix
%cmake .. \
	%{cmake_on_off static_libs BUILD_STATIC_LIBS} \
	-DBUILD_TESTS:BOOL=OFF \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DGZIP_PATH=FALSE \
	-DMANDOC_PATH=FALSE \
	-DUSE_HIDAPI=ON \
	-DUSE_PCSC:BOOL=ON \
	-DNFC_LINUX=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.adoc
%attr(755,root,root) %{_bindir}/fido2-assert
%attr(755,root,root) %{_bindir}/fido2-cred
%attr(755,root,root) %{_bindir}/fido2-token
%attr(755,root,root) %{_libdir}/libfido2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfido2.so.1
%{_mandir}/man1/fido2-assert.1*
%{_mandir}/man1/fido2-cred.1*
%{_mandir}/man1/fido2-token.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfido2.so
%{_includedir}/fido
%{_includedir}/fido.h
%{_pkgconfigdir}/libfido2.pc
%{_mandir}/man3/*_pk_*.3*
%{_mandir}/man3/fido*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfido2.a
%endif
