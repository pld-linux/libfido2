Summary:	Library functionality for FIDO 2.0, including communication with a device over USB
Summary(pl.UTF-8):	Biblioteka funkcji dla FIDO 2.0, wraz z komunikacją z urządzeniem po USB
Name:		libfido2
Version:	1.2.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/Yubico/libfido2/releases
Source0:	https://github.com/Yubico/libfido2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3075949f4683d3960871d4c23d6f4089
URL:		https://developers.yubico.com/libfido2/
BuildRequires:	cmake >= 3.0
BuildRequires:	hidapi-devel >= 0.8.0
BuildRequires:	libcbor-devel
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	pkgconfig
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
Requires:	hidapi-devel >= 0.8.0

%description devel
Header files for FIDO2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FIDO2.

%prep
%setup -q

%build
install -d build
cd build
# note: exects CMAKE_INSTALL_LIBDIR relative to prefix
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DGZIP_PATH=FALSE

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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfido2.so
%{_includedir}/fido
%{_includedir}/fido.h
%{_pkgconfigdir}/libfido2.pc
