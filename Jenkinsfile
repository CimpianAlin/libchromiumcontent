def startVM(name) {
  stage("Create /Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant ${name} VM") {
    withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=/Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant"]) {
      sh "vagrant up ${name}"
    }
  }
}

def stopVM(name) {
  stage("Stop /Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant ${name} VM") {
    withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=/Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant"]) {
      sh "vagrant halt ${name}"
    }
  }
}

def destroyVM(name) {
  stage("Destroy /Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant ${name} VM") {
    withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=/Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant"]) {
      sh "vagrant destroy -f ${name}"
    }
  }
}

def vmSSH(name, command) {
  withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=/Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant"]) {
    sh "vagrant ssh ${name} -c ${command}"
  }
}

def updateLibchromiumcontent() {
  stage('Clean') {
    deleteDir()
  }
  stage('Checkout') {
    checkout scm
  }
  stage('Bootstrap') {
    retry(3) {
      timeout(60) {
        sh "python script/bootstrap -t ${env.TARGET_ARCH}"
      }
    }
  }
  stage('Update') {
    sh "python script/update -t ${env.TARGET_ARCH}"
  }
}

def buildLibchromiumcontent() {
  stage('Build') {
    sh "python script/build -t ${env.TARGET_ARCH}"
  }
  stage('Create Dist') {
    sh "python script/create-dist"
  }
}

def updateLibchromiumcontentVagrant(name) {
  stage('Clean') {
    deleteDir()
  }
  stage('Checkout') {
    vmSSH(name, "'git clone https://github.com/brave/libchromiumcontent.git'")
  }
  stage('Bootstrap') {
    retry(3) {
      timeout(60) {
        vmSSH(name, "'source ~/.profile && cd libchromiumcontent && python script/bootstrap -t ${env.TARGET_ARCH}'")
      }
    }
  }
  stage('Update') {
    vmSSH(name, "'source ~/.profile && cd libchromiumcontent && python script/update -t ${env.TARGET_ARCH}'")
  }
}

def buildLibchromiumcontentVagrant(name) {
  stage('Build') {
    vmSSH(name, "'source ~/.profile && cd libchromiumcontent && python script/build -t ${env.TARGET_ARCH}'")
  }
  stage('Create Dist') {
    vmSSH(name, "'source ~/.profile && cd libchromiumcontent && python script/create-dist'")
  }
  // TODO(bridiver) - upload
}

def installBoto(name) {
  git clone git://github.com/boto/boto.git
  cd boto
  python setup.py install
}

def installLinuxDeps(name) {
  stage('install deps') {
    vmSSH(name, "'echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections'")
    vmSSH(name, "'src/build/install-build-deps.sh --no-prompt --no-arm'")
  }
}

timestamps {
  withEnv([
    'LIBCHROMIUMCONTENT_MIRROR=https://s3.amazonaws.com/brave-laptop-binaries/libchromiumcontent']) {

    parallel (
      mac: {
        node {
          withEnv(['TARGET_ARCH=x64']) {
            updateLibchromiumcontent()
            buildLibchromiumcontent()
          }
        }
      },
      winx64: {
        node {
          withEnv(['TARGET_ARCH=x64']) {
            try {
              destroyVM('win-x64')
              startVM('win-x64')
              updateLibchromiumcontentVagrant('win-x64')
              buildLibchromiumcontentVagrant('win-x64')
            } finally {
              destroyVM('win-x64')
            }
          }
        }
      },
      winia32: {
        node {
          withEnv(['TARGET_ARCH=ia32']) {
            try {
              destroyVM('win-ia32')
              startVM('win-ia32')
              updateLibchromiumcontentVagrant('win-ia32')
              buildLibchromiumcontentVagrant('win-ia32')
            } finally {
              destroyVM('win-ia32')
            }
          }
        }
      },
      linuxx64: {
        node {
          withEnv(['TARGET_ARCH=x64']) {
            try {
              destroyVM('linux-x64')
              startVM('linux-x64')
              updateLibchromiumcontentVagrant('linux-x64')
              installLinuxDeps('linux-x64')
              buildLibchromiumcontentVagrant('linux-x64')
            } finally {
              destroyVM('linux-x64')
            }
          }
        }
      }
//      linuxia32: {
//        node {
//          withEnv(['TARGET_ARCH=ia32']) {
//            destroyVM('linux-ia32')
//            startVM('linux-ia32')
//            updateLibchromiumcontentVagrant('linux-ia32')
//            installLinuxDeps('linux-ia32')
//            buildLibchromiumcontentVagrant('linux-ia32')
//            destroyVM('linux-ia32')
 //         }
//        }
//      }
    )
  }
}
