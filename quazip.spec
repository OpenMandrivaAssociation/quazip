Name:		quazip
Version:	0.4.3
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

%description
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%package devel
Summary:		Development files for %{name}
Group:			Development/Other
Requires:		%{name} = %{version}-%{release}
Requires:		zlib-devel
Requires:		qt4-devel

%description devel
The %{name}-devel package contains libraries, header files and documentation
for developing applications that use %{name}. 

%prep
%setup -q

# Fixes build and install
sed -i 's\PREFIX/lib\PREFIX/%{_lib}\' %{name}/%{name}.pro
# removing test programs
sed -i 's\test/[a-zA-Z]*\\g' %{name}.pro

%build
%{qmake_qt4} PREFIX=%{_prefix} LIBS+=-lzip
make

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
make INSTALL="install -p" INSTALL_ROOT=%{buildroot} install

%files
%doc COPYING* NEWS
%{_libdir}/*.so.*

%files devel
%doc doc/html
%{_includedir}/%{name}
%{_libdir}/*.so
