from getopt import getopt
import KS
import algorithms
import sys, getopt




def main(argv):
    ctl = ""
    ksfile = ""
    action =""
    label = []
    nbstate = 0
    transition_probability = 0.55
    label_probability = 0.4
    try:
        opts, args = getopt.getopt(argv,"a:c:k:",["action=","ctl=", "ksfile=", "label=", "nbstate=", "transitionProb=", "labelProb="])
    except getopt.GetoptError:
        print("error")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--ctl"):
            ctl = arg
        elif opt in ("-k", "--ksfile"):
            ksfile = arg
        elif opt in ("-a", "--action"):
            action = arg
        elif opt in ("--label"):
            label = arg[1:-1].split(",")
        elif opt in ("--nbstate"):
            nbstate = int(arg)
        elif opt in ("--transitionProb"):
            transition_probability = float(arg)
        elif opt in ("--labelProb"):
            label_probability = float(arg)

    print("ctl: " + ctl)
    print("ksfile: " + ksfile)
    # print("label:" + label)

    # print(args)

    if "run" == action:
        if ksfile =="" or ctl == "":
            print("ERROR: No formula or input model")
        else:
            print("ctl: " + ctl)
            print("ksfile: " + ksfile)
            model = KS.KS_Model(ksfile)
            algo = algorithms.Algo_checks(model)
            algo.run(ctl)
    elif "rundetailed" == action:
        if ksfile =="" or ctl == "":
            print("ERROR: No formula or input model")
        else:
            print("ctl: " + ctl)
            print("ksfile: " + ksfile)
            model = KS.KS_Model(ksfile)
            algo = algorithms.Algo_checks(model)
            algo.run(ctl, True)
    elif "generateKS" == action:
        if ksfile =="" or nbstate == 0 or label == []:
            print("ERROR: wrong input")
        else:
            KS.KS_Model.generate(nbstate, label, ksfile, transition_probability, label_probability)

if __name__ == "__main__":
    main(sys.argv[1:])
