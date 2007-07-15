#
# TODO:
# - pl desc
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	SSR packets scheduler (Simple Round Robin)
#Summary(pl.UTF-8):
Name:		kernel%{_alt_kernel}-net-sch_srr
Version:	0.4
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://mordor.strace.net/sched-srr/sch_srr.v%{version}.tgz
# Source0-md5:	943ed9d1a237336085331d43050d955c
URL:		http://mordor.strace.net/sched-srr/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains SRR packets scheduler (Simple Round Robin).

Simple Round Robin packets schedules - this is the schedules of
packets for the linux operating system with kernels 2.4 or 2.6. Its
purpose is the simply round robin distribution of the resources of the
allocated bandwidth between its users. It works as follows: the
internal queue of scheduler is divided into the given number of
virtual queues (slots). Each slot, in turn, has hard limited number of
packets located in it. Internal classifier distributes the entering in
scheduler packets along the slots, being based either on source ip
address or on destination ip address. With the selection of packet
from the scheduler, the slots will be processed cyclically, which will
ensure more or less uniform distribution.

#%description -l pl.UTF-8

%prep
%setup -q -n sch_srr.v%{version}

cat > Makefile <<'EOF'
obj-m := sch_srr.o
CFLAGS += -DKERNEL26
EOF

%build
%build_kernel_modules  -m sch_srr
# -C .
%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m sch_srr -d kernel/net/sch_srr

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/kernel/net/sch_srr
/lib/modules/%{_kernel_ver}/kernel/net/sch_srr/sch_srr*.ko*
