from flask import Flask, render_template, redirect, request, url_for, Response, send_file
import time, pickle, re
import datetime, os
import cv2, pickle,random
import numpy as np
import tensorflow as tf
from scipy.spatial import distance
from werkzeug import secure_filename
from pymediainfo import MediaInfo

MAIN_DIR='C:\\Users\\tusha\Desktop\\'           #change the main dir as per the system
UPLOAD_FOLDER = MAIN_DIR + 'ISL\\upload'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

f = open('output_check.pkl', 'rb')
opt_dic = pickle.load(f)
f.close()

# load model
from tensorflow.keras.models import load_model
model = load_model('model.h5')

graph = tf.get_default_graph()          #loading default graph

# app.config['MAX_CONTENT_LENGTH'] =  * 1024 * 1024

@app.route("/")
def home():
    return render_template('index.html')

def check_if_video(filename):
    global UPLOAD_FOLDER
    video_file_extensions = (
        '.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec',
        '.aep', '.aepx',
        '.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf',
        '.asx', '.avb',
        '.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik',
        '.bin', '.bix',
        '.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine',
        '.cip',
        '.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat',
        '.dav', '.dce',
        '.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm',
        '.dmsm3d', '.dmss',
        '.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms',
        '.dvx', '.dxr',
        '.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp',
        '.fcproject',
        '.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp',
        '.h264', '.hdmov',
        '.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf',
        '.ivr', '.ivs',
        '.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg',
        '.m1v', '.m21',
        '.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv',
        '.mj2', '.mjp',
        '.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie',
        '.mp21',
        '.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex',
        '.mpl',
        '.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb',
        '.mvc',
        '.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv',
        '.nvc', '.ogm',
        '.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist',
        '.plproj',
        '.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr',
        '.pxv',
        '.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd',
        '.rmd',
        '.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk',
        '.sbt',
        '.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi',
        '.smi',
        '.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf',
        '.swi',
        '.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts',
        '.tsp', '.ttxt',
        '.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg', '.vem', '.vep', '.vf',
        '.vft',
        '.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7',
        '.vpj',
        '.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx',
        '.wot', '.wp3',
        '.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog',
        '.yuv', '.zeg',
        '.zm1', '.zm2', '.zm3', '.zmv')
    try:
        if filename.endswith((video_file_extensions)):
            return True

        else:
            return False
    except:
        return False

fname = None
given_file_name=None

@app.route('/sigml_conv', methods=["POST", "GET"])
def sigml_conv():
    global fname
    if request.method == "POST":
        file = request.files["files"]
        filename = secure_filename(file.filename)
        if check_if_video(filename):
            fname = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            video_to_sigml_convertor(filename)
            return render_template('sigml_conv.html', content="Download sigml file by clicking button above")
        else:
            return render_template('sigml_conv.html', content="Issue with the file...try again")
    else:
        return render_template('sigml_conv.html')


@app.route('/download')
def download():
    global given_file_name
    if given_file_name != None:
        path = UPLOAD_FOLDER + "\\" + 'sigml_' + given_file_name
        given_file_name = None
        return send_file(path, as_attachment=True)
    else:
        given_file_name=None
        return render_template('sigml_conv.html', content="nothing selected...")


@app.route("/about_us")
def about_us():
    return render_template('about_us.html')


# main formatter

start = '<sigml><hns_sign gloss=""><hamnosys_nonmanual><hnm_body tag=""/><hnm_shoulder tag=""/><hnm_head tag="TR"/><hnm_mouthpicture picture="hVl@_U"/><hnm_eyegaze tag=""/><hnm_eyebrows tag=""/><hnm_nose tag=""/><hnm_eyelids tag=""/></hamnosys_nonmanual><hamnosys_manual>'
end = '</hamnosys_manual></hns_sign></sigml>'
ham_text = ''


def process(raw_sigml):
    new_sigml = []

    for sigm in raw_sigml:
        new = ''
        # sigm=sigm.rstrip().rsplit()
        for s in sigm:
            if s != '<':
                new += s

        new_sigml.append(new)

    return new_sigml


def savesigml(gen_sigml):
    global ham_text, test
    fin_sigml = []

    for s in gen_sigml:
        if 'Unnamed' not in s:

            if '.' in s:
                s, _ = s.split('.')
                ham_text += '<' + s + '/>'
                fin_sigml.append(s)
            else:
                ham_text += '<' + s + '/>'
                fin_sigml.append(s)

    return fin_sigml
    # just put the symbols and save the string
    # DONE


def get_sigml(opt):
    global opt_dic
    # here our output will be 0 to 101 which are already mapped to sigml columns.
    # so we will load the pickle file and return the mapped output

    raw_sigml = opt_dic[opt]
    gen_sigml = process(raw_sigml)
    fin_sigml = savesigml(gen_sigml)

    return fin_sigml

def final_process(all_sigml):
  ind_dic={}
  tags=[]
  class_num=0

  for each_sigml in all_sigml:
    for each_tag in each_sigml:

      if len(tags)==0:
        tags.append(each_tag)
        ind_dic[each_tag] = class_num

      else:
        if each_tag in ind_dic:
          if ind_dic[each_tag] == class_num:
            tags.append(each_tag)
            ind_dic[each_tag] = class_num
        else:
          tags.append(each_tag)
          ind_dic[each_tag] = class_num

    class_num+=1
  return tags

def joiner(final_tags):

    real_tags = []
    for f in final_tags:
        value = '<' + f + '/>'

        real_tags.append(value)
    return real_tags

f = open('order_dic.pkl','rb')
order_dic = pickle.load(f)
def make_order(real_tags):
    global order_dic
    for tag in real_tags:
        if tag in order_dic:
            order_dic[tag] += 1
        else:
            order_dic[tag] = 0

    ordered_tags = []
    for key in order_dic:

        for i in range(order_dic[key]):
            ordered_tags.append(key)

    return ordered_tags

def join_tags(ordered_tags):
    sigml=''

    for f in ordered_tags:
        sigml += f

    return sigml

def video_to_sigml_convertor(filename=None):

    global ham_text,given_file_name,model,graph
    with graph.as_default():
        print(filename)
        cumulated_list=[]
        input_video = UPLOAD_FOLDER + '//' + filename
        if filename is not None:
            cap = cv2.VideoCapture(input_video)

            while True:
                try:
                    _, img = cap.read()

                    img = cv2.resize(img, (60, 60), interpolation=cv2.INTER_AREA)
                    img = img.reshape(1, 60, 60, 3)  # preparing input image
                    #gen_output=np.argmax(model.predict(img))
                    gen_output = random.randint(0,100)  # for testing

                    fin_sigml=get_sigml(gen_output)  # passing output that is generated
                    cumulated_list.append(fin_sigml)
                except:
                    break

            final_tags = final_process(cumulated_list)
            real_tags = joiner(final_tags)
            ordered_tags = make_order(real_tags)
            final_sigml_text = join_tags(ordered_tags)
            final_text= start + final_sigml_text + end      #text file will be generated; and that will be our final output sigml file
            sigmlfile_name = filename.split('.')[0]
            given_file_name=sigmlfile_name+'.txt'
            opt_name_file=UPLOAD_FOLDER+'//'+'sigml_'+given_file_name
            f=open(opt_name_file,'w')
            f.write(final_text)
            f.close()
    # after this function a cumulated ham_text will be generated, this can be concatenated with start and end text as declared above and saved

if __name__ == "__main__":
    app.run(host='192.168.43.166', debug=True)
