node 'vagrant-trusty64' {

    package { 'pip':
        ensure   => latest,
        provider => 'pip',
        require  => Package['python-pip'],
    }

    package { 'python-pip':
        ensure => present
    }

    package { [
        'python-dev',
        'build-essential',
        'libxml2-dev',
        'libxslt1-dev',
        'zlib1g-dev',
        'libffi-dev',
        'libssl-dev',
        ]:
        ensure => present
    }
}
