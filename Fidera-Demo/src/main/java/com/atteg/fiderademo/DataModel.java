/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.atteg.fiderademo;

/**
 *
 * @author laaks
 */
public class DataModel {
    private int difference;
    private String time;

    public DataModel() {
        
    }
    
    public DataModel(int difference, String time) {
        this.difference = difference;
        this.time = time;
    }

    public int getDifference() {
        return difference;
    }

    public void setDifference(int difference) {
        this.difference = difference;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }
    
    @Override
    public String toString() {
        return String.format("%d%% difference at %s", difference, time);
    }
     
}
