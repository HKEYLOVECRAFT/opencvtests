/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.atteg.fiderademo;

import java.util.ArrayList;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;

/**
 *
 * @author laaks
 */
@Controller
public class IndexController {

    private List<DataModel> dataList;

    public IndexController() {
        this.dataList = new ArrayList<>();
    }

    /**
     * Return the index page.
     * @param model
     * @return 
     */
    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("data", dataList);
        return "index";
    }

    /**
     * Return the dataList fragment defined in dataListFragment.html
     * @param model
     * @return 
     */
    @GetMapping(value = "/data")
    public String getList(Model model) {
        model.addAttribute("data", this.dataList);
        // return dataList th:fragment of index page
        return "dataListFragment :: dataList";
    }

    /**
     * Add a DataModel object to the list. Success returns a 204 response.
     * @param difference The % difference.
     * @param time Timestamp
     */
    @PostMapping("/data")
    @ResponseStatus(value = HttpStatus.NO_CONTENT)
    public void post(@RequestParam String difference, @RequestParam String time) {

        // Keep only 5 last.
        if (this.dataList.size() > 4) {
            dataList.remove(0);
            this.dataList.add(new DataModel(Integer.parseInt(difference), time));
        } else {
            this.dataList.add(new DataModel(Integer.parseInt(difference), time));
        }

    }

}
