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
    if (!node.dragged) {
        CallPython(g_nodes_table_node_id, "OnChartSelection", { event_id: node.event_id, ctrl_key: d3.event.ctrlKey });
    }
}

function OnLinkClick(link) {
    CallPython(g_links_table_node_id, "OnChartSelection", { event_id: link.event_id, ctrl_key: d3.event.ctrlKey });
}


//----------------------------------------------------------

// Style & behaviour configuration items. Override these
// functions in your plugin. Don't rely on 'this'; the functions
// are generally call'ed against a UI object.

function Config(data, svg) { }

// fetch a node's ID; link elements use the ID to identify
// the node's they connect
Config.prototype.GetNodeId = function (node_data) {
    return node_data.title;
}

// populate the graphical elements of all displayed nodes
Config.prototype.EnterNode = function (display_node) {
    display_node
      .append("circle")
        .attr("class", "node-shape");

    display_node
      .append("text");
}

Config.prototype.UpdateNode = function (display_node) {
    display_node
      .select("circle")
        .attr("class", "node-shape")
        .attr("r", 10)
        .attr("fill", "green")
        .attr("style", "stroke: white; stroke-width: 1.5px;");

    display_node
      .select("text")
        .attr("class", "node-text")
        .attr("x", 15)
        .text(function (node_data) {
            return node_data.title;
        });
}

// style (set styles/attributes) on display nodes
// default behaviour sets node opacity according to selection state
Config.prototype.StyleNode = function (display_node) {
    display_node
        .attr("opacity", function (node_data) {
            return NodeOpacity(node_data);
        });
}

// populate the graphical elements of all displayed links
Config.prototype.EnterLink = function (display_link) {
    display_link
      .append("line");
}

Config.prototype.UpdateLink = function (display_link) {
    display_link
      .select("line")
        .attr("stroke", "black");
}

// style (set styles/attributes) on a display links
// default behaviour sets link opacity according to selection state
Config.prototype.StyleLink = function (display_link) {
    display_link
        .attr("opacity", function (link_data) {
            return LinkOpacity(link_data);
        });

    visibility = g_options.show_link_labels ? "visible" : "hidden";
    label = display_link
      .select("g")
        .attr("visibility", visibility);
}

// refine the D3 simulation; the link force is "link", and the attraction
// force is called "charge"
Config.prototype.StyleSimulation = function (simulation) {
    simulation.force("link")
        .distance(50);
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
// data to display - schema:
//
//  nodes[]
//    event_id - number used by link structures to identify the node
//    type - arbitrary type; nodes of the same type will normally the same style
//    title - textual title displayed for the node
//    size - arbitrary size; after normalising, the displayed diameter is proportional to this value
//
//  links[]
//    source - initially node.event_id of source node; re-written to be reference to source node
//    target - initially node.event_id of target node; re-written to be reference to target node
//    type - (optional) arbitrary type; typically used to determine line style/colour
//    label - (optional) name for the link
//

//
// display/layout configuration - schema:
//
var g_options = null;

// retained data
var g_simulation = null;
var g_curZoom = 0;
var g_curTransform = d3.zoomIdentity;

// append the svg object to the body of the page
var g_svg = d3
  .select("#graph")
  .append("svg")
    .attr("width", "100%")
    .attr("height", "100%");

var g_links_group = g_svg.append("g");
var g_joined_links = null;

var g_nodes_group = g_svg.append("g");
var g_joined_nodes = null;


//----------------------------------------------------------

// selection support
var g_has_selection = false;
var g_selected_nodes = new Set();
var g_selected_links = new Set();

function IsNodeSelected(node_data) {
    return !g_has_selection || g_selected_nodes.has(node_data.event_id);
}

function NodeOpacity(node_data) {
    return IsNodeSelected(node_data) ? 1.0 : 0.2;
}

function IsLinkSelected(link_data) {
    return !g_has_selection || g_selected_links.has(link_data.event_id);
}

function LinkOpacity(link_data) {
    return IsLinkSelected(link_data) ? 1.0 : 0.2;
}


//----------------------------------------------------------
function GetWindowWidth() {
    return document.getElementById("graph").clientWidth;
}

function GetWindowHeight() {
    return document.getElementById("graph").clientHeight;
}


//----------------------------------------------------------
// determine intersection of line L1 (x1, y1) -> (x2, y2) with L2 (x3, y3) -> (x4, y4)
// from https://stackoverflow.com/questions/9043805/test-if-two-lines-intersect-javascript-function
function LineIntersect(x1, y1, x2, y2, x3, y3, x4, y4) {
    // determinant
    var D = (x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1);

    if (D !== 0) {
        // position of intersection along L1 (L) & L2 (G)
        var L = ((y4 - y3) * (x4 - x1) + (x3 - x4) * (y4 - y1)) / D;
        var G = ((y1 - y2) * (x4 - x1) + (x2 - x1) * (y4 - y1)) / D;

        if (0 <= L && L <= 1 && 0 <= G && G <= 1) {
            return { intersects: true, x: x1 + (x2 - x1) * L, y: y1 + (y2 - y1) * L };
        }
    }

    return { intersects: false };
};

// determine intersection of line L1 (x1, y1) -> (x2, y2) with rectangle (x3, y3, width, height)
function RectIntersect(x1, y1, x2, y2, x3, y3, width, height) {
    var left_top = { x: x3, y: y3 },
        right_top = { x: left_top.x + width, y: left_top.y },
        right_bottom = { x: right_top.x, y: right_top.y + height },
        left_bottom = { x: left_top.x, y: right_bottom.y };

    var lines = [
        { src: left_top, tgt: right_top },
        { src: right_top, tgt: right_bottom },
        { src: right_bottom, tgt: left_bottom },
        { src: left_bottom, tgt: left_top }
    ];

    for (var idx in lines) {
        var line = lines[idx];
        var res = LineIntersect(x1, y1, x2, y2, line.src.x, line.src.y, line.tgt.x, line.tgt.y);

        if (res.intersects) {
            return res;
        }
    }

    return { intersects: false };
}

function Layout() {
    const doTransition = (g_curZoom != g_curTransform.k);
    g_curZoom = g_curTransform.k;

    const ref_transition = d3.transition()
        .duration(250);

    (doTransition ? g_joined_links.transition(ref_transition) : g_joined_links)
        .each(function (link_data) {
            // map model coord system to SVG coord system
            var x1 = g_curTransform.applyX(link_data.source.x),
                y1 = g_curTransform.applyY(link_data.source.y),
                x2 = g_curTransform.applyX(link_data.target.x),
                y2 = g_curTransform.applyY(link_data.target.y);

            // where extents are available, use them to trim link lines
            var src_extent = link_data.source.node_extent;
            if (src_extent) {
                var res = RectIntersect(x1, y1, x2, y2, src_extent.x + x1, src_extent.y + y1, src_extent.width, src_extent.height);
                if (res.intersects) {
                    x1 = res.x;
                    y1 = res.y;
                }
            }

            var tgt_extent = link_data.target.node_extent;
            if (tgt_extent) {
                var res = RectIntersect(x1, y1, x2, y2, tgt_extent.x + x2, tgt_extent.y + y2, tgt_extent.width, tgt_extent.height);
                if (res.intersects) {
                    x2 = res.x;
                    y2 = res.y;
                }
            }

            d3.select(this)
              .select("line")
                .attr("x1", x1)
                .attr("y1", y1)
                .attr("x2", x2)
                .attr("y2", y2);

            var tx = x1 + (x2 - x1) / 2,
                ty = y1 + (y2 - y1) / 2;

            d3.select(this)
              .select("g")
                .attr("transform", "translate(" + tx + "," + ty + ")");
        });

    (doTransition ? g_joined_nodes.transition(ref_transition) : g_joined_nodes)
        .attr("transform", function (node_data) {
            // map model coord system to SVG coord system
            const x = g_curTransform.applyX(node_data.x);
            const y = g_curTransform.applyY(node_data.y);
            return "translate(" + x + "," + y + ")";
        });
}


function DoCreateChart(data) {
    SetupConfig(data);
    g_curZoom = g_curTransform.k;

    g_svg
       .call(d3.zoom()
            .scaleExtent([1, 8])
            .wheelDelta(function wheelDelta() {
                // d3.event here is the underlying WheelEvent
                // fixed step per event; avoids magic numbers like this:
                //  return -d3.event.deltaY * (d3.event.deltaMode === 1 ? 0.15 : d3.event.deltaMode ? 1 : 0.01);
                return d3.event.deltaY < 0 ? 0.4 : -0.4;
            })
            .on("zoom", function () {
                g_curTransform = d3.event.transform;
                Layout();
            })
        );

    g_joined_links = g_links_group
      .selectAll(".link-group")
      .data(data.links)
      .join(
        function (enter) {
            return enter
              .append("g")
                .attr("class", "link-group")
                .call(g_config.EnterLink)
        }
      )
        .call(g_config.UpdateLink)
        .call(g_config.StyleLink)
        .on("click", OnLinkClick);

    g_joined_nodes = g_nodes_group
      .selectAll(".node-group")
      .data(data.nodes)
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
        .on("click", OnNodeClick)
        .call(d3.drag()
            .on("start", function (node_data) {
                // ignore active here, its for multi-touch screens
                // active - the number of currently active drag gestures (on start and end, not including this one).

                node_data.fx = node_data.x;
                node_data.fy = node_data.y;
                node_data.dragged = false;
            })
            .on("drag", function (node_data) {
                if (!node_data.dragged)
                    g_simulation.alphaTarget(0.3).restart();
                // map SVG coord system back to model coord system
                node_data.fx += d3.event.dx / g_curZoom;
                node_data.fy += d3.event.dy / g_curZoom;
                node_data.dragged = true;
            })
            .on("end", function (node_data) {
                if (node_data.dragged)
                    g_simulation.alphaTarget(0);
                node_data.fx = null;
                node_data.fy = null;
            })
        );
}


function DoSimulation(data) {
    centre_x = GetWindowWidth() / 2;
    centre_y = GetWindowHeight() / 2;

    g_simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links)
            .id(g_config.GetNodeId)
        )
        .force("charge", d3.forceManyBody())
        .on("tick", Layout)
        .stop();

    if ("graph_is_disjoint" in g_options && g_options.graph_is_disjoint) {
        g_simulation
            .force("x", d3.forceX(centre_x))
            .force("y", d3.forceY(centre_y));
    }
    else {
        g_simulation
            .force("center", d3.forceCenter(centre_x, centre_y));
    }

    g_config.StyleSimulation(g_simulation);
    g_simulation.restart();
}


function CreateChart(data_json, options_json) {
    data = JSON.parse(data_json);
    g_options = JSON.parse(options_json);

    DoCreateChart(data);
    DoSimulation(data);
}


//----------------------------------------------------------
function DoSetSelection() {
    g_joined_nodes.transition(250)
        .call(g_config.StyleNode);

    g_joined_links.transition(250)
        .call(g_config.StyleLink);
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

    g_has_selection = g_selected_nodes.size != 0 || g_selected_links.size != 0;

    DoSetSelection();
}
