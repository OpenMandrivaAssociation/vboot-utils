%define gitshort 595108c0

Name:		vboot-utils
Version:	20230127
Release:	5.git%{gitshort}1
Group:		System/Kernel and hardware
Summary:	Verified Boot Utility from Chromium OS
License:	BSD
URL:		https://chromium.googlesource.com/chromiumos/platform/vboot_reference

ExclusiveArch:	%{arm} aarch64 %{ix86} %{x86_64}

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  git clone https://git.chromium.org/git/chromiumos/platform/vboot_reference.git
#  cd vboot_reference/
#  git archive --format=tar --prefix=vboot-utils-a1c5f7c/ a1c5f7c | xz > vboot-utils-a1c5f7c.tar.xz
Source0:	%{name}-%{gitshort}.tar.xz

# Fix FTBFS agsinst gcc10
Patch0:		https://src.fedoraproject.org/rpms/vboot-utils/raw/rawhide/f/vboot-utils-595108c0-gcc10.patch

BuildRequires:	glibc-static-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	trousers-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(uuid)

%description
Verified boot is a collection of utilities helpful for chromebook computer.
Pack and sign the kernel, manage gpt partitions.

%prep
%autosetup -p1 -n %{name}-%{gitshort}

%build
%ifarch %{arm} aarch64
%global ARCH arm
%endif

%ifarch %{x86_64}
%global ARCH x86_64
%endif

%ifarch i686
%global ARCH i386
%endif

make V=1 ARCH=%{ARCH} COMMON_FLAGS="%{optflags}"

%install
make install V=1 DESTDIR=%{buildroot}/usr ARCH=%{ARCH} COMMON_FLAGS="%{optflags}"

# Remove unneeded build artifacts
rm -rf %{buildroot}/usr/lib/pkgconfig/
rm -rf %{buildroot}/usr/default/

%files
%license LICENSE
%doc README
%{_bindir}/*
