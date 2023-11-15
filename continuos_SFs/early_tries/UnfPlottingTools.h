#ifndef PlotingTools_h
#define PlotingTools_h

#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <TH1.h>
#include <TH2.h>
#include <TFile.h>
#include <string>
#include "TH1F.h"
#include "TPaveStats.h"
#include "TH2F.h"
#include "THStack.h"
#include "TCanvas.h"
#include "TString.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TColor.h"
#include "TLatex.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TFrame.h"
//#include "tdrstyle.C"
//#include "CMS_lumi.C"
namespace UnfPlottingTools {
int col1 = TColor::GetColor(64, 83, 211); // Blue
int col2 = TColor::GetColor(238, 119, 51);// Orange
int col3 = TColor::GetColor(215, 0, 132); // Magenta
int col4 = TColor::GetColor(0, 190, 255);//new TColor::GetFreeColorIndex();
//int col1 = kAzure;
vector<int> colours = {kBlack, col2, col1, kMagenta, col4, kGreen, kOrange+1, kRed+1, 40};
TH1* ratio(TH1* hnom, TH1* hdenom)
{
    TH1* hratio = (TH1*)hnom->Clone("ratio");
    cout << hratio->GetNbinsX() << endl;
    cout << hnom->GetNbinsX() << endl;
    double content=0, error=0;
    for(int i = 1; i<=hratio->GetNbinsX(); ++i){
        content=hnom->GetBinContent(i);
        error=hnom->GetBinError(i);
        double div=hdenom->GetBinContent(i);
        if(div==0)
        {
            content=1;
            error = 1;
        }
        else
        { 
            content /= div;
            //error /=div;
        }
        //hratio->SetBinContent(i,content);
        //hratio->SetBinError(i, error/div);
    }
    hratio->Divide(hnom, hdenom);
    hratio->GetYaxis()->SetTitle("Ratio to JetHT");
    cout << "Finsih ratio" << endl;
    return hratio;
}

TCanvas* set_canvas(TString name, string frame_text, int square=0, int multi=0)
{
    int W = 700;
    int H = 900;
    int W2= W;
    if(square==1) H=W;
    if(square==2){H=W;W2*=multi;} 
    float T = 0.08*W;
    float B = 0.12*W;
    float L = 0.18*H;
    float R = 0.12*H;
    TCanvas *c = new TCanvas(name, name, 50,50,W2, H);
    c->SetFillColor(0);
    c->SetBorderMode(0);
    c->SetFrameFillStyle(0);
    c->SetFrameBorderMode(0);
    c->SetLeftMargin( L/W );
    c->SetRightMargin( R/W );
    c->SetTopMargin( T/H );
    c->SetBottomMargin( B/H );
    c->SetTickx(0);
    c->SetTicky(0);
    //writeExtraText = true;       
    //extraText  = frame_text;

    return c;
}
void LegendEntry(float gap, int nb_item, int col, TString legend_str, int legend_type, float textsize=0.2)
{
    TLatex latex;
    latex.SetTextFont(42);
    latex.SetTextAngle(0);
    latex.SetTextColor(kBlack);
    latex.SetTextSize(textsize);
    latex.SetTextAlign(12);
    float bwx_ = 0.12;
    float bwy_ = gap/1.5;
    float height = 1-gap*(nb_item+1);
    float x_l[1];
    float ex_l[1];
    float y_l[1];
    float ey_l[1];
    x_l[0] = 1.2*bwx_;
    y_l[0] = height+0.03;
    ex_l[0] = 0;
    ey_l[0] = 0.04;
    float xx_ = x_l[0];
    if(legend_type == 0)
    {
        TGraph* gr_l = new TGraphErrors(1, x_l, y_l,ex_l, ey_l );
        gStyle->SetEndErrorSize(0);
        gr_l->SetMarkerStyle(20+nb_item);
        gr_l->SetMarkerColor(col);
        gr_l->SetMarkerSize(0.9);
        gr_l->Draw("0P");
        latex.DrawLatex(xx_+1.*bwx_, height, legend_str);
    }
    if(legend_type == 1)
    {
    //   TLine* line = new TLine(1.2*bwx_+0.06, height, 1.2*bwx_-0.06, height);
    //   line->SetLineColor(col);
    //   //line->SetLineStyle(nb_item);
    //   line->SetLineStyle(1);
    //   line->Draw("0P");
    //   latex.DrawLatex(xx_+1.*bwx_, height, legend_str);
    }
    if(legend_type ==2)
    {
        TBox box_;
        box_.SetLineStyle( kSolid );
        box_.SetLineWidth(3);
        box_.SetLineColor(col);
        box_.SetFillColor(col);
        box_.SetFillStyle( 3002+1*nb_item);
        box_.DrawBox( xx_-bwx_/3, height-bwx_/3, xx_+bwx_/3, height+bwx_/3 );
        box_.SetFillStyle(0);
        box_.DrawBox( xx_-bwx_/3, height-bwx_/3, xx_+bwx_/3, height+bwx_/3 );
        latex.DrawLatex(xx_+1.*bwx_,height, legend_str);
    }
    if(legend_type == 3)
    {
        latex.DrawLatex(1.2*bwx_, height, legend_str);
    }
}
TPad* TextPad(TString name, float x1, float y1, float dx, float dy)
{
    float x0 = x1-dx;
    float y0 = y1-dy;
    TPad *pad = new TPad(name, name, x0, y0, x1, y1);
    return pad;
}
TCanvas* PlotTH1(TH1* h, int logX, int logY, int pureMC=0, TString bin_text="", string frame_text="Work in Progress")
{
    TString name = h->GetName();
    int square=1;
    TCanvas* canvas = set_canvas(name, frame_text, square);
    canvas->cd();
    h->SetMarkerStyle(20);
    h->SetMarkerSize(0.7);
    TString draw_op="E1X0";
    h->Draw(draw_op);
    h->SetStats(0);
    h->SetTitle("");
    h->SetLineColor(colours[0]);
    h->SetMaximum(h->GetMaximum()*1.2);
    //h->GetYaxis()->SetTitle(" Events / 0.02 ");
/*for more histo in the same plot you should pass vector<TH1*> h instead of only one histogram and instead of h in the above lines you should have h[0]
    for(size_t i=1; i<h.size(); ++i)
    {
        h[i]->SetLineColor(colours[i+1+type]);
        if(type==0){h[i]->SetFillColor(colours[i+1]);
        h[i]->SetMarkerStyle(21+i);
        h[i]->SetMarkerColor(colours[i+1]);
        }
        h[i]->SetLineStyle(i+type);
        h[i]->Draw(draw_op);
    }*/
    // Legend definition
    //TLegend *leg=new TLegend(0.7,0.65,0.85,0.89);
    //leg->SetTextSize(0.04);
    //legend->Draw();
    //legend->cd();
    //float legend_gap = 1.0/(h.size()+2);
    //float textsize = 0.22;

    canvas->cd();

    float t = canvas->GetTopMargin();
    float l = canvas->GetLeftMargin();
    TLatex latex;
    latex.SetNDC();
    latex.SetTextAngle(0);
    //latex.SetTextFont(cmsTextFont);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.3*t);
    //latex.DrawLatex(l,1-t+0.2*t, bin_text);
    
    if(logY==1) gPad->SetLogy();
    if(logX==1) gPad->SetLogx();
    //int iPeriod = 5;
    //if(pureMC==1)  iPeriod = 10;
    //CMS_lumi(canvas, iPeriod, 11); 
    canvas->RedrawAxis();
    canvas->Update();
    //canvas->GetFrame()->Draw();
    return canvas;   
}
TCanvas* PlotTH2(TH2* h, int isMC = 1, int logX=0, int logY=0, int logZ=0, TString bin_info = " ")
{
    TString _name = h->GetName();
    string extra_text = "Work in Progress";
    int iPeriod = 5;
    if(isMC==1) iPeriod=10;
    TCanvas* canvas = set_canvas(_name, extra_text , 1);
    float t = canvas->GetTopMargin();
    float l = canvas->GetLeftMargin();
    canvas->cd();
    h->SetTitle("");
    h->Draw("COLZ");
    h->SetStats(0);
    h->GetXaxis()->SetTitleOffset(1.5);
    canvas->cd();
    TLatex latex;
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextAlign(11);
    latex.SetTextSize(0.3*t);
    latex.DrawLatex(l,1-t+0.2*t, bin_info);
    if(logX==1) gPad->SetLogx();
    if(logY==1) gPad->SetLogy();
    if(logZ==1) gPad->SetLogz();
    //CMS_lumi(canvas, iPeriod, 11);
    canvas->Update();
    canvas->GetFrame()->Draw();
    return canvas;
}
vector<TH1*> TH2toTH1(TH2* h2, TString datatype)
{
    vector<TH1*> h1vec;
    int nbinsy = h2->GetNbinsY();
    int nbinsx = h2->GetNbinsX();
    TString _name = h2->GetName();
    h1vec.push_back(h2->ProjectionX(_name+"_projX_"+datatype));
    for(int i = 1; i<= nbinsy; ++i) 
    {
        h1vec.push_back(h2->ProjectionX(_name+"_firstjet_ptbin="+(i-1)+"_"+datatype, i, i));
    }
    return h1vec;
}
TCanvas* th1_ratio_plot(vector<TH1*> histos, int logX, int logY, double min, double max, int legend, TString rationame, int pureMC=0, int Text = 0, string frame_text="Work in Progress")
{
    TString name = histos[0]->GetName();
    int square = 0;
    TCanvas* c = set_canvas(name, frame_text, square);
    c->cd();
    //histos[0]->SetMarkerStyle(20);
    histos[0]->SetLineColor(colours[0]);
    histos[0]->SetLineWidth(3);
    //histos[0]->Scale(1/histos[0]->Integral("width"));
    for(size_t i=1; i<histos.size(); i++)
    {
        if(histos.size()<3){
            histos[i]->SetLineColor(colours[3+i]);
            histos[i]->SetLineWidth(3);
        }
        else{
            histos[i]->SetLineColor(colours[i+1]);
            histos[i]->SetLineWidth(3);
        }
    }
    TPad* pad1 = new TPad("pad1", "pad1", 0, 0.35, 1, 1);
    pad1->Draw();
    pad1->cd();
    pad1->SetBottomMargin(0.025);
    //histos[0]->SetMarkerSize(1.2);
    //histos[0]->SetMarkerColor(colours[0]);
    //histos[0]->SetMarkerStyle(26);
    histos[0]->Draw("EHIST");
    for(size_t i=1; i<histos.size(); ++i) histos[i]->Draw("SAME EHIST");
    if (legend == 2){
        if(logY==1) histos[0]->SetMaximum(histos[0]->GetMaximum()*2);
        else histos[0]->SetMaximum(histos[1]->GetMaximum()*1.3);    
    }
    else{
        if(logY==1) histos[0]->SetMaximum(histos[0]->GetMaximum()*2);
        else histos[0]->SetMaximum(histos[1]->GetMaximum()*1.2);    
    }
    histos[0]->GetXaxis()->SetTitle("");
    histos[0]->GetYaxis()->SetTitle("A.U.");
    histos[0]->SetTitle("");
    histos[0]->SetStats(0);
    histos[0]->GetXaxis()->SetLabelOffset(999);
    histos[0]->GetYaxis()->SetTitleOffset(1.5);
    //histos[0]->GetYaxis()->SetTitle("");
    //histos[0]->GetYaxis()->SetRangeUser(0., 0.008);
    if(legend == 1){
        TLegend *leg=new TLegend(0.65,0.65,0.85,0.89);
        leg->SetTextSize(0.04);
        leg->SetBorderSize(0);
        leg->AddEntry(histos[0],"Data","l");
        leg->AddEntry(histos[1],"MC","l");
        //leg->AddEntry(histos[0],"SM","l");
        //leg->AddEntry(histos[1],"cpd","l");
        leg->SetEntrySeparation(0.03);
        leg->Draw();
    }
    if (legend == 2){
        TLegend *leg=new TLegend(0.7,0.65,0.85,0.89);
        leg->SetTextSize(0.04);
        leg->SetBorderSize(0);
        leg->SetNColumns(2);
        leg->AddEntry(histos[0],"SM","l");
        leg->AddEntry(histos[1],"O_{tG}","l");
        leg->AddEntry(histos[2],"O_{#phi t}","l");
        leg->AddEntry(histos[3],"O_{tZ}","l");
        leg->AddEntry(histos[4],"O^{(3)}_{#phi Q}","l");
        leg->AddEntry(histos[5],"O_{tW}","l");
        leg->AddEntry(histos[6],"O^{(-)}_{#phi Q}","l");
        leg->SetEntrySeparation(0.05);
        leg->Draw();
    }
    if(legend == 3){
        TLegend *leg=new TLegend(0.7,0.65,0.85,0.89);
        leg->SetTextSize(0.04);
        leg->SetBorderSize(0);
        leg->AddEntry(histos[0],"TWZ","l");
        //leg->AddEntry(histos[1],"Analytic","l");
        leg->AddEntry(histos[1],"TTZ","l");
        //leg->AddEntry(histos[0],"SM","l");
        //leg->AddEntry(histos[1],"WtoSM1","l");
        //leg->AddEntry(histos[2],"WtoSM2","l");
        //leg->AddEntry(histos[3],"WtoSM3","l");
        //leg->AddEntry(histos[4],"SM2","l");
        //leg->SetNColumns(2);
        //leg->AddEntry(histos[0],"SM","l");
        //leg->AddEntry(histos[1],"O_{tG}","l");
        //leg->AddEntry(histos[2],"O_{#phi t}","l");
        //leg->AddEntry(histos[3],"O_{tZ}","l");
        //leg->AddEntry(histos[4],"O_{tW}","l");
        //leg->AddEntry(histos[5],"O^{(3)}_{#phi Q}","l");
        //leg->AddEntry(histos[6],"O^{(-)}_{#phi Q}","l");
        leg->SetEntrySeparation(0.03);
        leg->Draw();
    }
    if(logY==1) gPad->SetLogy();
    if(logX==1) gPad->SetLogx();
    if(logY==1) histos[0]->SetMinimum(1); 
    c->cd();
    TPad* pad2 = new TPad("pad2", "pad2", 0 , 0, 1, 0.35);
    pad2->Draw();
    pad2->SetTopMargin(0.025);
    pad2->SetBottomMargin(0.25);
    pad2->cd();
    if(logX==1) gPad->SetLogx();
    vector<TH1*> hratio;
    for(size_t i=1; i<histos.size(); ++i){
        hratio.push_back((TH1*)histos[i]->Clone());
        hratio[i-1]->Divide(hratio[i-1], histos[0]);
    }
    TH1* href = (TH1*)histos[0]->Clone();
    href->Divide(histos[0]);
    hratio[0]->SetStats(0);
    hratio[0]->SetTitle("");
    //hratio[0]->GetXaxis()->SetTitle("W_{1} #eta");
    //hratio[0]->GetXaxis()->SetTitle("p_{t} W_{1} [GeV]");
    hratio[0]->SetTitleSize(0.1);
    hratio[0]->SetLabelSize(0.08);
    hratio[0]->SetLineWidth(3);
    hratio[0]->GetYaxis()->SetTitleSize(0.06);
    hratio[0]->GetYaxis()->SetLabelSize(0.06);
    hratio[0]->GetYaxis()->SetTitleOffset(0.7);
    hratio[0]->GetYaxis()->SetTitle(rationame);
    hratio[0]->GetXaxis()->SetTitleSize(0.06);
    hratio[0]->GetXaxis()->SetLabelSize(0.06);
    hratio[0]->GetXaxis()->SetTitleOffset(1.4);
    hratio[0]->SetMaximum(max);
    hratio[0]->SetMinimum(min);
    hratio[0]->SetFillStyle(0);
    hratio[0]->Draw("EHIST");
    for(size_t i=1; i<hratio.size(); ++i){
        hratio[i]->SetLineWidth(3);
        hratio[i]->Draw("SAME EHIST");
    }
    href->Draw("SAME");
    gPad->SetTicks(1, 0);
    c->cd();
    //CMS_lumi( pad1, 0, 1);
    pad1->RedrawAxis();
    c->Update();
    c->RedrawAxis();
    return c;
}

};
#endif

