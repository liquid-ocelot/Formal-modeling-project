from getopt import getopt
import KS
import algorithms
import sys, getopt




def main(argv):
    ctl = ""
    ksfile = ""
    action =""
    label = []
    try:
        opts, args = getopt.getopt(argv,"a:c:k:",["action=","ctl=", "ksfile=", "label="])
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
            label = arg

    print("ctl: " + ctl)
    print("ksfile: " + ksfile)
    print("label:" + str(type(label)) )

    # print(args)

    if "run" == action:
        if ksfile =="" or ctl == "":
            print("ERROR: No formula or input model")
        else:
            model = KS.KS_Model(ksfile)
            algo = algorithms.Algo_checks(model)
            algo.run(ctl)
    elif "rundetailed" == action:
        if ksfile =="" or ctl == "":
            print("ERROR: No formula or input model")
        else:
            model = KS.KS_Model(ksfile)
            algo = algorithms.Algo_checks(model)
            algo.run(ctl, True)
    # elif "generateKS" == action:
    #     if ksfile =="" or ctl == "":
    #         print("ERROR: No formula or input model")
    #     else:
    #         model = KS.KS_Model(ksfile)
    #         algo = algorithms.Algo_checks(model)
    #         algo.run(ctl, True)

if __name__ == "__main__":
    main(sys.argv[1:])
