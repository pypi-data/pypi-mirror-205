import os
import sys
import glob
import stat
import shutil
import tarfile
import argparse
import subprocess

from .sxlogic import load_settings, save_settings

def gw_sh_path(ide_path):
    loc = os.path.dirname(ide_path)
    sh = os.path.join(loc, 'gw_sh.exe')
    return sh

def find_gowin():
    loc = shutil.which('gw_sh')
    if loc:
        return loc
    if sys.platform == 'win32':
        import winreg
        registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
        try:
            return gw_sh_path(winreg.QueryValue(key, "gw_ide.exe"))
        except:
            pass
        key.Close()

        registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
        try:
            return gw_sh_path(winreg.QueryValue(key, "gw_ide.exe"))
        except:
            pass
    elif sys.platform == 'linux':
        found = None
        for dirname in glob.glob('/opt/Gowin*'):
            bindir = os.path.join(dirname, 'IDE/bin')
            fullpath = os.path.join(bindir, 'gw_sh')
            if os.path.isfile(fullpath):
                found = fullpath
        if found != None:
            return found

    raise Exception("Cannot find gowin installation")

def check_gowin_opt(gowin):
    if not os.path.isdir(gowin):
        raise Exception(gowin+' is not a directory')

    exe = 'gw_sh.exe' if sys.platform == 'win32' else 'gw_sh'

    bindir = os.path.join(gowin, 'bin')
    if os.path.isdir(bindir):
        fullpath = os.path.join(bindir, exe)
        if os.path.isfile(fullpath):
            return fullpath
        else:
            raise Exception(exe + ' not found in ' + bindir)

    fullpath = os.path.join(gowin, exe)
    if os.path.isfile(fullpath):
        return fullpath
    else:
        raise Exception(exe + ' not found in ' + gowin)

def find_fs(buildir):
    for filename in glob.glob(os.path.join(buildir, '**/*.fs'), recursive=True):
        return filename

valid_tars = ['.tar.gz','.tgz']

def build(opt):
    if not any([opt.filename.endswith(suff) for suff in valid_tars]):
        print('ERROR: Expecting a compressed tar filename')
        sys.exit(1)

    settings = load_settings()
    if opt.gowin:
        try:
            settings['gw_sh'] = check_gowin_opt(opt.gowin)
            save_settings(settings)
        except Exception as err:
            print('ERROR: '+str(err))
            sys.exit(1)
    else:
        if 'gw_sh' not in settings:
            try:
                settings['gw_sh'] = find_gowin()
                save_settings(settings)
            except Exception as err:
                print('ERROR: '+str(err))
                sys.exit(1)

    gw_sh = settings['gw_sh']

    build_dir = os.path.splitext(os.path.basename(opt.filename))[0] + '-build'

    print('Extracting into %s ...' % build_dir)

    if os.path.exists(build_dir):
        for filename in glob.glob(os.path.join(build_dir, 'hw/impl/pnr/*')):
            os.chmod(filename, stat.S_IWRITE|stat.S_IREAD)
        shutil.rmtree(build_dir)

    with tarfile.open(opt.filename) as tf:
        tf.extractall(build_dir)

    print('Building bitstream ...')

    outname = os.path.join(build_dir, os.path.join('hw', 'build.log'))
    outf = open(outname, 'w')
    proc = subprocess.run([gw_sh, 'project.tcl'], cwd=os.path.join(build_dir, 'hw'), stdout=outf, stderr=subprocess.STDOUT)
    outf.close()
    if proc.returncode != 0:
        print('ERROR: Project build failed')
        print('See build log %s for errors.' % os.path.normpath(outname))
        sys.exit(1)

    bitstream = find_fs(build_dir)
    if not bitstream:
        print('ERROR: Output bitstream not found')

    print('SUCCESS! (log in %s)' % os.path.normpath(outname))

    target = os.path.join(build_dir, os.path.join('hw', os.path.basename(bitstream)))
    shutil.copyfile(bitstream, target)
    
    bitstream = os.path.splitext(bitstream)[0]+'.bin'
    target = os.path.join(build_dir, os.path.join('hw', os.path.basename(bitstream)))
    shutil.copyfile(bitstream, target)

    print('BUILT', os.path.normpath(target))

def moncole():
    parser = argparse.ArgumentParser(description='monocle')
    parser.add_argument('--gowin', help='Gowin tools directory (saved for future runs)')
    subparsers = parser.add_subparsers(dest='cmd')
    build_parser = subparsers.add_parser('build', help='build StreamLogic FPGA bitstream')
    build_parser.add_argument('filename')
    build_parser.set_defaults(func=build)
    opt = parser.parse_args()

    if opt.cmd:
        opt.func(opt)
    else:
        parser.parse_args(['--help'])

if __name__ == '__main__':
    moncole()
