#Load DICOM Data 
<<<<<<< HEAD
import slicer
=======
>>>>>>> 8e05e2e210b0c4fbee48cfaaed5ff46903444bd6
import os
dicomFilesDirectory = input("Path to input folder with DICOM files:")   # input folder with DICOM files
outputPath = input("Path to export and save the generated *.STL file:")
loadedNodeIDs = []  # this list will contain the list of all loaded node IDs
import DICOMLib.DICOMUtils as utils
import DICOMScalarVolumePlugin
from DICOMLib import DICOMUtils
scalarVolumeReader = DICOMScalarVolumePlugin.DICOMScalarVolumePluginClass()
with DICOMUtils.TemporaryDICOMDatabase() as db:
  DICOMUtils.importDicom(dicomFilesDirectory, db)
  patientUIDs = db.patients()
  #loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))
  loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUIDs[0])) 
  
masterVolumeNode =slicer.mrmlScene.GetNodeByID(loadedNodeIDs[0]) 
# Create segmentation
segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
segmentationNode.CreateDefaultDisplayNodes() # only needed for display
segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)

# Create temporary segment editor to get access to effects
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
segmentEditorWidget.setSegmentationNode(segmentationNode)
segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

# Create segments by thresholding
segmentsFromHounsfieldUnits = [ 
    ["bone", 135, 1165] ]
for segmentName, thresholdMin, thresholdMax in segmentsFromHounsfieldUnits:
    # Create segment
    addedSegmentID = segmentationNode.GetSegmentation().AddEmptySegment(segmentName)
    segmentEditorNode.SetSelectedSegmentID(addedSegmentID)
    # Fill by thresholding
    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("MinimumThreshold",str(thresholdMin))
    effect.setParameter("MaximumThreshold",str(thresholdMax))
    effect.self().onApply()
    #Smothing
    segmentEditorWidget.setActiveEffectByName("Smoothing")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("SmothingMethod","Median")
    effect.setParameter("KernelSizeMm",11)
    effect.self().onApply()
    #
    segmentationNode.CreateClosedSurfaceRepresentation()
    surfaceMesh = segmentationNode.GetClosedSurfaceInternalRepresentation(addedSegmentID)    
    writer = vtk.vtkSTLWriter()
    writer.SetInputData(surfaceMesh)
    writer.SetFileName(os.path.join (outputPath,"SINGLE.stl"))
    writer.Update()
# Delete temporary segment editor
segmentEditorWidget = None
slicer.mrmlScene.RemoveNode(segmentEditorNode)

# Compute segment volumes
resultsTableNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTableNode')
import SegmentStatistics
segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
segStatLogic.getParameterNode().SetParameter("ScalarVolume", masterVolumeNode.GetID())
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.enabled","False")
segStatLogic.getParameterNode().SetParameter("ScalarVolumeSegmentStatisticsPlugin.voxel_count.enabled","False")
segStatLogic.getParameterNode().SetParameter("ScalarVolumeSegmentStatisticsPlugin.volume_mm3.enabled","False")
segStatLogic.computeStatistics()
segStatLogic.exportToTable(resultsTableNode)
segStatLogic.showTable(resultsTableNode)

# Export segmentation to a labelmap
labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode')
slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode, labelmapVolumeNode, masterVolumeNode)
<<<<<<< HEAD
slicer.util.saveNode(labelmapVolumeNode, os.path.join (outputPath,"Bone-label.nrrd"))
=======
slicer.util.saveNode(labelmapVolumeNode, os.path.join (outputPath,"Bone-label.nrrd"))
>>>>>>> 8e05e2e210b0c4fbee48cfaaed5ff46903444bd6
