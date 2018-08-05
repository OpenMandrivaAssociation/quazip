%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%define debug_package %nil

Summary:	Qt/C++ wrapper for the minizip library
Name:		quazip
Version:	0.7.6
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://quazip.sourceforge.net/
SOurce0:	https://github.com/stachenov/quazip/archive/%{version}.tar.gz
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qt5-devel

%description
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Qt/C++ wrapper for the minizip library
%rename quazip

%description -n %{libname}
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%files -n %{libname}
%{_libdir}/libquazip.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains libraries, header files and documentation
for developing applications that use %{libname}.

%files -n %{devname}
%doc COPYING* NEWS.txt
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/libquazip.so

#------------------------------------------------------------------------------

%prep
%setup -q

# Fixes build and install
sed -i 's\PREFIX/lib\PREFIX/%{_lib}\' %{name}/%{name}.pro
# removing test programs
sed -i 's\qztest\\g' %{name}.pro

%build
%qmake_qt5 PREFIX=%{_prefix} QMAKE_CXXFLAGS_RELEASE= LIBS+=-lz
%make

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
make INSTALL="install -p" INSTALL_ROOT=%{buildroot} install

