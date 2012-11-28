class mtrac {
  package { "python-pip":
    ensure => present,
  }

  package { "python-dev":
    ensure => present,
  }

  exec { "pip-modules":
    require => [Package["python-pip"], Package["python-dev"]],
    command => "/usr/bin/pip install -r /vagrant/pip-requires.txt",
    timeout => 0,
  }

#  exec { "runserver":
#    require => Exec["pip-modules"],
#    command => "/vagrant/mtrack_project/manage.py runserver",
#  }
}
