%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Qt/C++ wrapper for the minizip library
Name:		quazip
Version:	0.6.2
Release:	4
License:	LGPLv2+
Group:		System/Libraries
Url:		http://quazip.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(QtCore)

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
%doc COPYING* NEWS.txt README.txt
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
%qmake_qt4 PREFIX=%{_prefix} QMAKE_CXXFLAGS_RELEASE= LIBS+=-lz
make

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
make INSTALL="install -p" INSTALL_ROOT=%{buildroot} install

