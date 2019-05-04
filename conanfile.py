from conans import ConanFile, VisualStudioBuildEnvironment, tools
from pprint import pprint

class MsdetoursConan(ConanFile):
    name = "ms-detours"
    version = "4.1"
    license = "MIT"
    author = "Sersoftin"
    url = "https://github.com/Microsoft/Detours"
    description = "Test description"
    topics = ("detour", "hook", "api hook")
    settings = "build_type", "arch"
    generators = "visual_studio"
    exports_sources = "src/*"
    exports = ["system.mak", "Makefile"]

    def build(self):
        env_build = VisualStudioBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            vcvars = tools.vcvars_command(self.settings)
            if self.options.build_samples is False:
                self.run('%s && cd src && nmake && cd ..' % vcvars)
            else:
                self.run('%s && nmake' % vcvars)

    def package(self):
        self.copy("*.h", dst="include", src="src")
        if self.settings.arch == 'x86':
            self.copy("*.lib", dst="lib", keep_path=False, src="lib.X86")
        if self.settings.arch == 'x86_64':
            self.copy("*.lib", dst="lib", keep_path=False, src="lib.X64")

    def package_info(self):
        self.cpp_info.libs = ["ms-detours"]
