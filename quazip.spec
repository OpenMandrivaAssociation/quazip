%define major 1

%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name:		quazip
Version:	0.4.4
Release:	3
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
%doc COPYING* NEWS
%{_libdir}/*.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	zlib-devel
Requires:	qt4-devel
Provides:	quazip-devel = %{version}-%{release}
Obsoletes:	quazip-devel <= 0.4.3-1
Obsoletes:	%{mklibname -d quazip 1} < 0.4.4-2

%description -n %{develname}
This package contains libraries, header files and documentation
for developing applications that use %{libname}.

%files -n %{develname}
%doc COPYING* NEWS
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

dos2unix COPYING NEWS doc/html/*

%build
%{qmake_qt4} PREFIX=%{_prefix} LIBS+=-lz
make

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
make INSTALL="install -p" INSTALL_ROOT=%{buildroot} install


%changelog
* Mon Feb 13 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.4.4-1
+ Revision: 773840
- linkage fix
- version update 0.4.4

* Wed Dec 14 2011 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.4.3-2
+ Revision: 741223
- missed summary added
- package fixed to comply libraries policy

* Tue Nov 22 2011 Alexander Khrukin <akhrukin@mandriva.org> 0.4.3-1
+ Revision: 732386
- imported package quazip

