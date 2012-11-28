class postgres {

  package { "postgresql":
    ensure => present,
  }

  package { "libpq-dev":
    ensure => present,
  }

  service { "postgresql":
    ensure => running,
  }
}
