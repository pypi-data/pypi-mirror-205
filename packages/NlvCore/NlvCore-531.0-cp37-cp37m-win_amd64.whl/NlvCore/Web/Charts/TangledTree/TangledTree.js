//
// Copyright (C) 2020 Niel Clausen. All rights reserved.
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
function OnNodeClick(node) {
    CallPython(g_nodes_table_node_id, "OnChartSelection", { event_id: node.event_id, ctrl_key: d3.event.ctrlKey });
}

function OnLinkClick(link) {
    CallPython(g_links_table_node_id, "OnChartSelection", { event_id: link.event_id, ctrl_key: d3.event.ctrlKey });
}


//----------------------------------------------------------

// Style & behaviour configuration items. Override these
// functions in your plugin. Don't rely on 'this'; the functions
// are generally call'ed against a UI object.

var f_colourScale = null;
function Config(data, svg) {
    f_colourScale = d3.scaleOrdinal(d3.schemeDark2)
}

// populate the graphical elements of all displayed nodes
Config.prototype.EnterNode = function (display_node) {
    display_node
      .append("text")
        .attr("class", "node-text");

    // the rect is solely to allow the text to be clicked/selected
    display_node
      .insert("rect", ":first-child");

    display_node
      .append("line")
        .attr("class", "node-outline");

    display_node
      .append("line")
        .attr("class", "node-fill");
}

Config.prototype.UpdateNode = function (display_node) {
    display_node
        .attr("transform", function (node_data) {
            return "translate(" + node_data.x + "," + node_data.y + ")"
        });

    display_node
      .select(".node-text")
        .attr("x", g_layout.BallRadius + g_layout.TextOffsetX)
        .attr("y", function (node_data) {
            return - g_layout.TextOffsetY;
        })
        .text(function (node_data) {
            return node_data.title;
        })
        .each(function (node_data) {
            node_data.text_extent = d3.select(this).node().getBBox();
        });

    display_node
        .select("rect")
        .attr("x", function (node_data) {
            return node_data.text_extent.x;
        })
        .attr("y", function (node_data) {
            return node_data.text_extent.y;
        })
        .attr("width", function (node_data) {
            return node_data.text_extent.width;
        })
        .attr("height", function (node_data) {
            return node_data.text_extent.height;
        })
        .style("fill", "white")
        .style("stroke", "white");

    function SetBall(node) {
        node
            .attr("y2", function (node_data) {
                return node_data.bundle_height;
            });
    }

    display_node
      .select(".node-outline")
        .call(SetBall);

    display_node
        .select(".node-fill")
        .call(SetBall);
}

// style (set styles/attributes) on display nodes
Config.prototype.StyleNode = function (display_node) {
    display_node
      .select(".node-outline")
        .attr("stroke-width", 2 * g_layout.BallRadius);

    display_node
        .select(".node-fill")
        .attr("stroke", NodeFillColour)
        .attr("stroke-width", g_layout.BallRadius);
}

// populate the graphical elements of all displayed links
Config.prototype.EnterBundle = function (display_bundle) {
    display_bundle
      .append("path")
        .attr("class", "bundle-background");

    display_bundle
      .append("path")
        .attr("class", "bundle-selected");

    display_bundle
      .append("path")
        .attr("class", "bundle-foreground");
}

Config.prototype.UpdateBundle = function (display_bundle) {
    function CalcPath(path, include) {
        path.attr("d", function (bundle_data) {
            R = g_layout.LinkRadius
            return bundle_data.links.map(function (link) {
                return !include(link) ? "M 0 0" : "M " + link.px + " " + link.py
                    + " H " + (link.x - R)
                    + " A " + R + " " + R + " 0 0 1 " + link.x + " " + (link.py + R)
                    + " V " + (link.cy - R)
                    + " A " + R + " " + R + " 0 0 0 " + (link.x + R) + " " + link.cy
                    + " H " + link.cx
            }).join(" ");
        });
    }

    display_bundle
      .select(".bundle-background")
        .call(CalcPath, function (link) {
            return !IsLinkSelected(link);
        });

    display_bundle
      .select(".bundle-selected")
        .call(CalcPath, function (link) {
            return IsLinkSelected(link);
        });

    display_bundle
      .select(".bundle-foreground")
        .call(CalcPath, function (link) {
            return true;
        });
}

// style (set styles/attributes) on a displayed bundle
Config.prototype.StyleBundle = function (display_bundle) {
    display_bundle
      .select(".bundle-foreground")
        .attr("stroke", function (bundle_data) {
            return f_colourScale(bundle_data.id);
        });
}

var g_configConstructor = Config;
var g_config = null;

function SetConfigConstructor(config_constructor) {
    g_configConstructor = config_constructor;
}

function SetupConfig(data) {
    g_config = new g_configConstructor(data, g_svg);
}


//----------------------------------------------------------

//
// display/layout configuration:
//
var g_options = null;
var g_layout = null;

// append the svg object to the body of the page
var g_svg = d3
    .select("#graph")
    .append("svg");

var g_bundles_group = g_svg.append("g");
var g_nodes_group = g_svg.append("g");


//----------------------------------------------------------

// selection support
var g_selected_nodes = new Set();
var g_selected_links = new Set();

function IsNodeSelected(node_data) {
    return g_selected_nodes.has(node_data.event_id);
}

function NodeFillColour(node_data) {
    return IsNodeSelected(node_data) ? "gold" : "white";
}

function IsLinkSelected(link_data) {
    return g_selected_links.has(link_data.event_id);
}


//----------------------------------------------------------
function DoCreateChart(data) {
    SetupConfig(data);

    node_data = data.nodes;
    bundle_data = data.bundles;
    g_layout = data.config

    // set chart size
    g_svg
        .attr("width", g_layout.Width + "px")
        .attr("height", g_layout.Height + "px");

    g_bundles_group.selectAll(".bundle-group")
        .data(bundle_data)
        .join(
            function (enter) {
                return enter
                  .append("g")
                    .attr("class", "bundle-group")
                    .call(g_config.EnterBundle)
            })
        .call(g_config.UpdateBundle)
        .call(g_config.StyleBundle);

    g_joined_nodes = g_nodes_group.selectAll(".node-group")
        .data(node_data)
        .join(
            function (enter) {
                return enter
                  .append("g")
                    .attr("class", "node-group")
                    .call(g_config.EnterNode)
            }
        )
        .call(g_config.UpdateNode)
        .call(g_config.StyleNode)
        .on("click", OnNodeClick);
}


//----------------------------------------------------------
var g_data = null;

function CreateChart(data_json, options_json) {
    g_data = JSON.parse(data_json);
    g_options = JSON.parse(options_json);

    DoCreateChart(g_data);
}

function SetSelection(selection_json, options_json) {
    selection = JSON.parse(selection_json);
    g_options = JSON.parse(options_json);

    g_selected_nodes = new Set();
    selection.nodes.forEach(function (event_id) {
        g_selected_nodes.add(event_id);
    });

    g_selected_links = new Set();
    selection.links.forEach(function (event_id) {
        g_selected_links.add(event_id);
    });

    // link selection changes requuire the drawing order
    // of elements to also change, which requires a relayout
    DoCreateChart(g_data);
}
