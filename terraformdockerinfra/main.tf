terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.16.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "targetserver" {
  name         = "nishanthkp/targetserver:ubuntu16"
  keep_locally = false
}

resource "docker_container" "web_server" {
  image = docker_image.targetserver.name
  name  = "web_server"
  ports {
    internal = 5000
    external = 5000
  }
}

resource "docker_container" "db_server" {
  image = docker_image.targetserver.name
  name  = "db_server"
  ports {
    internal = 3306
    external = 3306
  }
}