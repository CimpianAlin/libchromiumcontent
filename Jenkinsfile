def libchromiumcontentVagrantfilePath = '/Users/Shared/Jenkins/vagrant/libchromiumcontent-vagrant'

def startVM(vagrantfilePath, name) {
  stage("Create ${vagrantfilePath} ${name} VM") {
    withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=${vagrantfilePath}"]) {
      sh "vagrant up ${name}"
    }
  }
}

def stopVM(vagrantfilePath, name) {
  stage("Stop ${vagrantfilePath} ${name} VM") {
    withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=${vagrantfilePath}"]) {
      sh "vagrant halt ${name}"
    }
  }
}

def destroyVM(vagrantfilePath, name) {
  stage("Destroy ${vagrantfilePath} ${name} VM") {
    withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=${vagrantfilePath}"]) {
      sh "vagrant destroy -f ${name}"
    }
  }
}

def vmSSH(vagrantFilePath, name, command) {
  withEnv(["VAGRANT_DOTFILE_PATH=${env.BUILD_TAG}", "VAGRANT_CWD=${vagrantfilePath}"]) {
    sh "vagrant ssh -c ${command}"
  }
}

  return (run_script('bootstrap') or
          run_script('update', args) or
          run_script('build', args) or
          run_script('create-dist', args) or
          run_script('upload', args))


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

def installLinuxDeps() {
  stage('install deps') {
    vmSSH(libchromiumcontentVagrantfilePath, 'linux-x64', "'echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections'")
    vmSSH(libchromiumcontentVagrantfilePath, 'linux-x64', "'src/build/install-build-deps.sh --no-prompt --no-arm'")
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
            startVM(libchromiumcontentVagrantfilePath, 'win-x64')
            updateLibchromiumcontent()
            buildLibchromiumcontent()
            destroyVM(libchromiumcontentVagrantfilePath, 'win-x64')
          }
        }
      },
      winia32: {
        node {
          withEnv(['TARGET_ARCH=ia32']) {
            startVM(libchromiumcontentVagrantfilePath, 'win-ia32')
            updateLibchromiumcontent()
            buildLibchromiumcontent()
            destroyVM(libchromiumcontentVagrantfilePath, 'win-ia32')
          }
        }
      },
      linuxx64: {
        node {
          withEnv(['TARGET_ARCH=x64']) {
            startVM(libchromiumcontentVagrantfilePath, 'linux-x64')
            updateLibchromiumcontent()
            installLinuxDeps()
            buildLibchromiumcontent()
            destroyVM(libchromiumcontentVagrantfilePath, 'linux-x64')
          }
        }
      }
      linuxia32: {
        node {
          withEnv(['TARGET_ARCH=ia32']) {
            startVM(libchromiumcontentVagrantfilePath, 'linux-ia32')
            updateLibchromiumcontent()
            installLinuxDeps()
            buildLibchromiumcontent()
            destroyVM(libchromiumcontentVagrantfilePath, 'linux-ia32')
          }
        }
      }
    )
  }
}
