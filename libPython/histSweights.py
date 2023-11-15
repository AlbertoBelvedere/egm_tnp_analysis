import ROOT

def list_workspace_and_observables(input_file, results_name):
    # Open the ROOT file
    infile = ROOT.TFile.Open(input_file, "READ")

    import pdb
    pdb.set_trace()

    r = gDirectory.Get()
    roofitresults = infile.Get(results_name)
    # To print the best fit values
    final_param = roofitresults.floatParsFinal()

    #1) RooRealVar::  acmsP = 50.0001 +/- (-6.59713e-05,1.24771)
    #2) RooRealVar::  betaP = 0.0100001 +/- (-1.04069e-07,6.42852e-05)
    #3) RooRealVar:: gammaP = 0.0353873 +/- 0.000147396
    #4) RooRealVar::  meanP = -0.887778 +/- (-0.0131056,0.0127332)
    #5) RooRealVar::  nBkgP = 423089 +/- (-984.382,946.232)
    #6) RooRealVar::  nSigP = 317725 +/- (-892.18,925.965)
    #7) RooRealVar:: sigmaP = 0.995864 +/- (-0.0388924,0.044162)

    param1 = final_param[0].getValV()

    # Get a list of all objects in the file
    keys = roofitresults.GetListOfKeys()

    # Iterate through the objects and identify workspaces and observables
    workspaces = []
    observables = []

    for key in keys:
        obj = key.ReadObj()
    	import pdb
    	pdb.set_trace()
        if isinstance(obj, ROOT.RooWorkspace):
            workspaces.append(obj.GetName())
            # Check for observables in the workspace
            if obj.obj("observables"):
                obs_set = obj.obj("observables")
                for obs_name in obs_set.contentsString().split(", "):
                    observables.append((obj.GetName(), obs_name))

    # Close the ROOT file
    infile.Close()

    # Return the list of workspaces and observables
    return workspaces, observables


def get_analytical_function(input_file, workspace_name, fit_result_name, observable_name, xmin, xmax):
    # Open the ROOT file
    infile = ROOT.TFile.Open(input_file, "READ")

    # Load the RooWorkspace from the ROOT file
    workspace = infile.Get(workspace_name)

    # Load the RooFitResult from the ROOT file
    fit_result = infile.Get(fit_result_name)

    # Get the observable variable
    observable = workspace.var(observable_name)

    # Get the fitted PDF from the RooFitResult
    fitted_pdf = fit_result.floatParsFinal().front().getVal()

    # Create the prototype function
    observables = ROOT.RooArgSet(observable)
    prototype_pdf = fitted_pdf.createPrototype(observables)

    # Optionally, compute the analytical integral of the prototype function over the specified range
    analytical_integral = prototype_pdf.analyticalIntegral(observables, ROOT.RooFit.NormSet(observables), ROOT.RooFit.Range(xmin, xmax))

    # Close the ROOT file
    infile.Close()

    # Return the analytical PDF and the analytical integral (if computed)
    return prototype_pdf, analytical_integral

def run(input_file):
    # Get the name of workspace and observable
    workspaces, observables = list_workspace_and_observables("results/UL2018_continuousSF/tnpEleID/passingMVA94Xwp80isoV2/data_Run2018A_passingMVA94Xwp80isoV2.nominalFit-bin00_el_sc_eta_m2p50Tom1p57_el_pt_10p00To20p00.root", "bin00_el_sc_eta_m2p50Tom1p57_el_pt_10p00To20p00_resP")
    
    # Print the list of workspaces and observables
    print("Workspaces:")
    print(workspaces)
    print("\nObservables:")
    print(observables)
    
    
    # Get differents functions and their integrals
    analytical_pdf, analytical_integral = get_analytical_function("results/UL2018_continuousSF/tnpEleID/passingMVA94Xwp80isoV2/data_Run2018A_passingMVA94Xwp80isoV2.nominalFit-bin00_el_sc_eta_m2p50Tom1p57_el_pt_10p00To20p00.root", "bin00_el_sc_eta_m2p50Tom1p57_el_pt_10p00To20p00_resP", "your_fit_result_name", "your_observable_name", 60, 120)



