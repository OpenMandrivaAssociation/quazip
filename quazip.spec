%define libname %mklibname quazip 1
%define develname %mklibname -d quazip 1

Name:		quazip
Version:	0.5
Release:	1
Summary:	Qt/C++ wrapper for the minizip library
License:	LGPLv2+
Group:		System/Libraries
URL:		http://quazip.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.zip
BuildRequires:	qt4-devel
BuildRequires:	zlib-devel
BuildRequires:	libzip-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	dos2unix

%description
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

#------------------------------------------------------------------------------

%package -n %libname
Summary:	Qt/C++ wrapper for the minizip library
%rename quazip

%description -n %libname
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%files -n %libname
%doc COPYING*
%{_libdir}/*.so.*

#------------------------------------------------------------------------------

%package -n %develname
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	zlib-devel
Requires:	qt4-devel
Provides:	quazip-devel = %{version}-%{release}
Obsoletes:	quazip-devel <= 0.4.3-1

%description -n %develname
The %{develname} package contains libraries, header files and documentation
for developing applications that use %{libname}.

%files -n %develname
%doc COPYING*
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/*.so

#------------------------------------------------------------------------------

%prep
%setup -q

# Fixes build and install
sed -i 's\PREFIX/lib\PREFIX/%{_lib}\' %{name}/%{name}.pro
# removing test programs
sed -i 's\test/[a-zA-Z]*\\g' %{name}.pro

dos2unix COPYING doc/html/*

%build
%{qmake_qt4} PREFIX=%{_prefix} LIBS+=-lz
make

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
make INSTALL="install -p" INSTALL_ROOT=%{buildroot} install
