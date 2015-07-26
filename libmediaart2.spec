#
# Conditional build:
%bcond_with	qt		# use Qt instead of GdkPixbuf for media extraction
%bcond_with	qt4		# use Qt4 instead of Qt5 (if with_qt; only when Qt5 is not installed)
%bcond_without	static_libs	# static library build
%bcond_without	vala		# Vala binding
#
Summary:	Media art extraction and cache management library
Summary(pl.UTF-8):	Biblioteka do wydobywania okładek i zarządzania ich pamięcią podręczną
Name:		libmediaart2
Version:	1.9.0
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libmediaart/1.9/libmediaart-%{version}.tar.xz
# Source0-md5:	0b65d64398d2f3dff89534c9dfffab4f
URL:		https://github.com/curlybeast/libmediaart
%if %{with qt}
%{!?with_qt4:BuildRequires:	Qt5Gui-devel >= 5.0.0}
%{?with_qt4:BuildRequires:	QtGui-devel >= 4.7.1}
%endif
%{!?with_qt:BuildRequires:	gdk-pixbuf2-devel >= 2.12.0}
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.8
%{?with_qt:BuildRequires:	libstdc++-devel}
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.16}
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with qt}
%{!?with_qt:Requires:	Qt5Gui >= 5.0.0}
%{?with_qt:Requires:	QtGui >= 4.7.1}
%endif
%{!?with_qt:Requires:	gdk-pixbuf2 >= 2.12.0}
Requires:	glib2 >= 1:2.38.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Media art extraction and cache management library.

%description -l pl.UTF-8
Biblioteka do wydobywania okładek i zarządzania ich pamięcią
podręczną.

%package devel
Summary:	Header files for libmediaart library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmediaart
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%if %{with qt}
%{!?with_qt:Requires:	Qt5Gui-devel >= 5.0.0}
%{?with_qt:Requires:	QtGui-devel >= 4.7.1}
%endif
%{!?with_qt:Requires:	gdk-pixbuf2-devel >= 2.12.0}
Requires:	glib2-devel >= 1:2.38.0
Requires:	zlib-devel

%description devel
Header files for libmediaart library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmediaart.

%package static
Summary:	Static libmediaart library
Summary(pl.UTF-8):	Statyczna biblioteka libmediaart
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmediaart library.

%description static -l pl.UTF-8
Statyczna biblioteka libmediaart.

%package apidocs
Summary:	libmediaart API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmediaart
Group:		Documentation
Conflicts:	libmediaart-apidocs < 1.9

%description apidocs
API documentation for libmediaart library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmediaart.

%package -n vala-libmediaart2
Summary:	Vala API for libmediaart library
Summary(pl.UTF-8):	API języka Vala dla biblioteki libmediaart
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16

%description -n vala-libmediaart2
Vala API for libmediaart library.

%description -n vala-libmediaart2 -l pl.UTF-8
API języka Vala dla biblioteki libmediaart.

%prep
%setup -q -n libmediaart-%{version}

%build
%configure \
	--enable-gdkpixbuf%{?with_qt:=no} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmediaart-2.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS
%attr(755,root,root) %{_libdir}/libmediaart-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediaart-2.0.so.0
%{_libdir}/girepository-1.0/MediaArt-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmediaart-2.0.so
%{_includedir}/libmediaart-2.0
%{_datadir}/gir-1.0/MediaArt-2.0.gir
%{_pkgconfigdir}/libmediaart-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmediaart-2.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libmediaart

%if %{with vala}
%files -n vala-libmediaart2
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libmediaart-2.0.vapi
%endif
