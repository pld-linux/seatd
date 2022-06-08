Summary:	Seat management daemon
Name:		seatd
Version:	0.7.0
Release:	1
License:	MIT
Group:		Applications
Source0:	https://git.sr.ht/~kennylevinsen/seatd/archive/%{version}.tar.gz
# Source0-md5:	922b8a4ca4dfdb1f43a294db9e77bcf7
Patch0:		x32.patch
URL:		https://git.sr.ht/~kennylevinsen/seatd
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	scdoc >= 1.9.7
BuildRequires:	systemd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A seat management daemon, that does everything it needs to do. Nothing
more, nothing less. Depends only on libc.

%package -n libseat
Summary:	Seat management library
Group:		Libraries

%description -n libseat
A seat management library allowing applications to use whatever seat
management is available.

Supports:
- seatd
- (e)logind
- embedded seatd for standalone operation

Each backend can be compile-time included and is runtime auto-detected
or manually selected with the LIBSEAT_BACKEND environment variable.

Which backend is in use is transparent to the application, providing a
simple common interface.

%package -n libseat-devel
Summary:	Header files for libseat library
Group:		Development/Libraries
Requires:	libseat = %{version}-%{release}
Requires:	systemd-devel

%description -n libseat-devel
Header files for libseat library.

%package -n libseat-static
Summary:	Static libseat library
Group:		Development/Libraries
Requires:	libseat-devel = %{version}-%{release}

%description -n libseat-static
Static libseat library.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Dlibseat-logind=systemd
%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n libseat -p /sbin/ldconfig
%postun -n libseat -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/seatd
%attr(755,root,root) %{_bindir}/seatd-launch
%{_mandir}/man1/seatd.1*
%{_mandir}/man1/seatd-launch.1*

%files -n libseat
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libseat.so.1

%files -n libseat-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libseat.so
%{_includedir}/libseat.h
%{_pkgconfigdir}/libseat.pc

%files -n libseat-static
%defattr(644,root,root,755)
%{_libdir}/libseat.a
