//
// Copyright (C) 2019-2020 Niel Clausen. All rights reserved.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
//

//----------------------------------------------------------
function OnClick(d) {
    CallPython(g_node_id, "OnChartSelection", { event_id: d.event_id, ctrl_key: d3.event.ctrlKey });
}


//----------------------------------------------------------

// global data
var g_data = null;
var g_title_text = null, g_x_label_text = null, g_y_label_text = null;

// append the svg object to the body of the page
var g_svg = d3.select("#graph")
  .append("svg")
    .attr("width", "100%")
    .attr("height", "100%");

var g_chart = g_svg.append("g");
var g_x_axis = g_chart.append("g");
var g_y_axis = g_chart.append("g");

var g_x_label = g_chart
  .append("text")
    .attr("class", "x-label");

var g_y_label = g_chart.append("text")
    .attr("class", "y-label");


//----------------------------------------------------------
function GetWidth(elem) {
    return elem.node().getBBox().width;
}

function GetHeight(elem) {
    return elem.node().getBBox().height;
}


//----------------------------------------------------------
function SetupXAxis(x_axis, x_scale, width) {
    x_scale
        .range([0, width]);

    x_axis
      .call(d3.axisBottom(x_scale))
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    return x_axis;
}

function CalcXAxisHeight(x_scale, width) {
    var tmp_axis = SetupXAxis(g_chart.append("g"), x_scale, width);
    var res = GetHeight(tmp_axis);
    tmp_axis.remove();
    return res;
}


//----------------------------------------------------------
function SetupYAxis(y_axis, y_scale, height) {
    y_scale
        .range([height, 0]);

    y_axis
        .call(d3.axisLeft(y_scale));

    return y_axis;
}

function CalcYAxisWidth(y_scale, height) {
    var tmp_axis = SetupYAxis(g_chart.append("g"), y_scale, height);
    var res = GetWidth(tmp_axis);
    tmp_axis.remove();
    return res;
}


//----------------------------------------------------------
function DoCreateChart(switch_time) {
    if (g_data == null)
        return;

    // set the dimensions and margins of the graph
    const min_window = 300, margin = 30, gap = 5, min_col_width = 20, max_col_width = 40;
    const window_width = Math.max(min_window, document.documentElement.clientWidth);
    const window_height = Math.max(min_window, document.documentElement.clientHeight);

    // determine layout sizes of the two axes
    var x_scale = d3.scaleBand()
        .domain(g_data.map(function (d) {
            return d.category;
        }))
        .padding(0.2);

    var y_scale = d3.scaleLinear()
        .domain([0, d3.max(g_data, function (d) {
            return d.value;
        })]);

    const x_axis_height = CalcXAxisHeight(x_scale, window_width * 0.75);
    const y_axis_width = CalcYAxisWidth(y_scale, window_height * 0.75);

    // determine layout sizes of the two labels
    g_x_label.text(g_x_label_text);
    const x_label_height = GetHeight(g_x_label);

    g_y_label
        .attr("transform", "translate(" + margin + "," + margin + ")rotate(-90)")
        .text(g_y_label_text);
    const y_label_width = GetHeight(g_y_label);

    // now determine locations for main elements
    const plot_left = margin + y_label_width + gap + y_axis_width;
    const col_width = Math.min(max_col_width, Math.max(min_col_width, 0.8 * (window_width - margin - plot_left) / g_data.length));
    const plot_width = g_data.length * col_width * 1.2;
    const plot_right = plot_left + plot_width;
    const plot_height = window_height - (2 * margin) - x_label_height - gap - x_axis_height;
    const plot_bottom = margin + plot_height;

    const ref_transition = d3.transition()
        .duration(switch_time);

    g_x_axis
        .attr("transform", "translate(" + plot_left + "," + plot_bottom + ")")
      .transition(ref_transition)
        .call(SetupXAxis, x_scale, plot_width);

    g_y_axis
        .attr("transform", "translate(" + plot_left + ", " + margin + ")")
      .transition(ref_transition)
        .call(SetupYAxis, y_scale, plot_height);

    g_x_label
      .transition(ref_transition)
        .attr("x", plot_right)
        .attr("y", plot_bottom + x_axis_height + gap + x_label_height);

    g_chart
      .selectAll(".column")
      .data(g_data, function (d) {
          return d.category;
      })
      .join(
        function (enter) {
            return enter
              .append("rect")
                .attr("class", "column")
                .style("opacity", 0)
                .attr("x", function (d) {
                    return x_scale(d.category);
                })
                .attr("y", -plot_bottom)
                .attr("width", x_scale.bandwidth());
        },
        function (update) {
            return update;
        },
        function (exit) {
            return exit
               .call(function (exit) {
                   exit
                     .transition(ref_transition)
                       .style("opacity", 0)
                       .attr("y", 2 * plot_bottom)
                       .on('end', function () {
                           d3.select(this).remove();
                       })
               })
        }
      )
        .on("click", OnClick)
        .on("mouseover", OnTipShow)
        .on("mousemove", OnTipMove)
        .on("mouseleave", OnTipHide)
        .attr("transform", "translate(" + plot_left + ", " + margin + ")")
      .transition(ref_transition)
        .style("opacity", 1)
        .attr("x", function (d) {
            return x_scale(d.category);
        })
        .attr("y", function (d) {
            return y_scale(d.value);
        })
        .attr("width", x_scale.bandwidth())
        .attr("height", function (d) {
            return plot_height - y_scale(d.value);
        })
        .attr("fill", function (d) {
            return d.selected ? "DarkOrange" : "DarkSlateBlue";
        });
}


//----------------------------------------------------------

SetupOnResize();
SetupTip(function (data) {
    return "<strong>" + data.category + "</strong> <span style='color:white'>" + data.value + "</span>";
});

function CreateChart(title, x_label_text, y_label_text, data_json, switch_time) {
    g_data = JSON.parse(data_json);
    g_title_text = title;
    g_x_label_text = x_label_text;
    g_y_label_text = y_label_text;
    DoCreateChart(switch_time);
}
