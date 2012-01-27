GraphEditor.progressBar.hide = function() {
  $('#'+GraphEditor.progressBarId).hide();
  GraphEditor._stopRefreshing = false;
  $('body').trigger($.Event('fileLoaded'));
  GraphEditor.refresh();
}

var graphSchema;

var Importer = {
  counter: 0,
  addNodeURL: undefined,
  addRelationshipURL: undefined,

  nodes: undefined,
  edges: undefined,
  progressBarId: undefined,
  progressTextId: undefined,

  schemaIsCompatible: function(graphSchema, sylvaSchema){
    // Each nodetype in graphSchema exists in sylva schema
    var compatible = true;
    $.each(graphSchema.nodeTypes, function(index, value){
      if (!sylvaSchema.nodeTypes.hasOwnProperty(index)){
        Importer.error("Node", index);
        compatible = false;
        return false;
      }
    });
    if (!compatible){
      return false;
    }
    // Each allowedtype in graphSchema exists in graph schema
    $.each(graphSchema.allowedEdges, function(index, value){
      if (!sylvaSchema.allowedEdges.hasOwnProperty(index)){
        Importer.error("Edge", value);
        compatible = false;
        return false;
      }
      with (sylvaSchema.allowedEdges[index]){
        if (value.source != source || value.label != label || value.target != target){
          Importer.error("Edge", value);
          compatible = false;
          return false;
        }
      }
    });
    return compatible;
  },

  error: function(dataType, dataValue){
    dataValue = JSON.stringify(dataValue);
    var text = ("ERROR: " + dataType + " " + dataValue +
        " does not exist in your Sylva schema. " +
        "Please fix your schemas and try again");
    $('#second-step-info').text(text);
  },

  addNode: function(nodeName, nodeData){
    var nodeType = nodeData.type;
    var properties = {};
    $.each(nodeData, function(index, value){
      properties[index] = value;
    });
    delete properties.position;
    delete properties.type;
    properties.nameLabel = nodeName;
    var nodeKey = nodeName + '_' + nodeType;

    $.ajax({
      url: Importer.addNodeURL,
      data: {
        type: nodeType,
        properties: JSON.stringify(properties)
      },
      success: function(response){
        response = JSON.parse(response);
        Importer.counter++;
        $(Importer.progressTextId).text('Node ' + nodeName + ' added');
        $(Importer.progressBarId).attr('value', Importer.counter);
        nodeData._id = response.id;
        
        // If all the nodes are inserted then we can start with the edges
        if (Importer.counter == Object.keys(Importer.nodes).length){
          $('body').trigger($.Event('endNodeInsertion'));
        }
      },
    });
  },

  addEdge: function(sourceName, edgeLabel, targetName){
    $.ajax({
      url: Importer.addRelationshipURL,
      data: {
        type: edgeLabel,
        sourceId: Importer.nodes[sourceName]._id,
        targetId: Importer.nodes[targetName]._id
      },
      success: function(response){
        response = JSON.parse(response);
        Importer.counter++;
        var relationshipText = sourceName + ' -> ' + edgeLabel + ' -> ' + targetName;
        $(Importer.progressTextId).text('Relationship ' + relationshipText + ' created.');
        $(Importer.progressBarId).attr('value', Importer.counter);
        if (Importer.counterMax === Importer.counter){
          $('body').trigger($.Event('importFinished'));
        }
      }
    });
  },

  addData: function(_nodes, _edges, _progressBarId, _progressTextId){
    Importer.nodes = _nodes;
    Importer.edges = _edges;
    Importer.progressBarId = _progressBarId;
    Importer.progressTextId = _progressTextId;
    
    // Progress bar initialization
    Importer.counterMax = Object.keys(Importer.nodes).length + Importer.edges.length;
    $(Importer.progressBarId).attr('max', Importer.counterMax);
        ;

    // Nodes import
    $.each(Importer.nodes, function(index, value){
      Importer.addNode(index, value);
    });

    // Edges import when nodes are done
    $('body').bind('endNodeInsertion', function() {
      $.each(Importer.edges, function(index, value){
        Importer.addEdge(value.source, value.type, value.target);
      });
    });
    
    // Final message
    $('body').bind('importFinished', function(){
      $(Importer.progressTextId).text("Import process finished. Added " +
            Importer.counter + " elements.");
    });
  }
};