//Maya ASCII 2019 scene
//Name: armour_guide_test.ma
//Last modified: Mon, Dec 09, 2024 01:59:38 PM
//Codeset: 936
requires maya "2019";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "202003131251-bd5bbc395a";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
createNode transform -n "armour_nurbsGuide_grp";
	rename -uid "4432B839-49D2-EC36-125E-3ABFA2BFD311";
createNode transform -n "armour_nurbs_guide" -p "armour_nurbsGuide_grp";
	rename -uid "1B27D086-4FCC-D12F-0524-D0BA1C38A628";
	addAttr -ci true -sn "spans_u" -ln "spans_u" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "spans_v" -ln "spans_v" -dv 3 -min 3 -max 20 -at "long";
	setAttr -k on ".spans_u" 4;
	setAttr -k on ".spans_v" 6;
createNode nurbsSurface -n "armour_nurbs_guideShape" -p "armour_nurbs_guide";
	rename -uid "79FD2E5D-4862-AA7D-F53B-0BA58A357B96";
	setAttr -k off ".v";
	setAttr -s 6 ".iog[0].og";
	setAttr -av ".iog[0].og[2].gid";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr -s 35 ".cp[16:34]" -type "double3" 0 4.4408920985006262e-16 
		0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
		0 0 0 0 0 0 0 0 0 0 0 0 0 0;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 3;
	setAttr ".dvv" 3;
	setAttr ".cpr" 15;
	setAttr ".cps" 4;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode nurbsSurface -n "armour_nurbs_guideShapeOrig" -p "armour_nurbs_guide";
	rename -uid "54E41101-40FB-71A0-90F7-A9AC00823BF8";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 1;
createNode transform -n "armour_nurbs_normal_grp" -p "armour_nurbsGuide_grp";
	rename -uid "AD78F9B4-4FF6-51B9-E30B-A89FA4C5D51E";
createNode transform -n "armour_nurbs_normal" -p "armour_nurbs_normal_grp";
	rename -uid "A8AEFC2C-4BEE-7607-B6AE-539C5921747B";
	setAttr -l on ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "armour_nurbs_normalShape" -p "armour_nurbs_normal";
	rename -uid "0E77DE0E-4744-4A1B-370C-248169077FEA";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 3;
	setAttr ".dvv" 3;
	setAttr ".cpr" 15;
	setAttr ".cps" 4;
createNode transform -n "armour_nurbs_center_grp" -p "armour_nurbsGuide_grp";
	rename -uid "4F0E1D90-42C4-5015-823E-78A5F462E926";
createNode transform -n "armour_nurbs_center" -p "armour_nurbs_center_grp";
	rename -uid "84679FAC-459B-4EE3-37A1-8EA595EA6853";
	setAttr -l on ".v";
	setAttr ".ovdt" 1;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr ".s" -type "double3" 0.05 1 0.05 ;
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "armour_nurbs_centerShape" -p "armour_nurbs_center";
	rename -uid "880212BD-4E7C-2DDA-5F32-638185DC622D";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 3;
	setAttr ".cps" 1;
createNode transform -n "armour_nurbs_blend" -p "armour_nurbsGuide_grp";
	rename -uid "58C570EF-451D-9C37-9458-908BAAB7CD83";
	addAttr -ci true -sn "spans_u" -ln "spans_u" -dv 1 -min 1 -max 20 -at "long";
	addAttr -ci true -sn "spans_v" -ln "spans_v" -dv 3 -min 3 -max 20 -at "long";
	setAttr -k on ".spans_u" 4;
	setAttr -k on ".spans_v" 6;
createNode nurbsSurface -n "armour_nurbs_blendShape" -p "armour_nurbs_blend";
	rename -uid "92BCDEEB-4D28-0663-0800-8FA74F9AC9E4";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 3;
	setAttr ".dvv" 3;
	setAttr ".cpr" 15;
	setAttr ".cps" 4;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode nurbsSurface -n "armour_nurbs_blendShapeOrig" -p "armour_nurbs_blend";
	rename -uid "C5AABDB2-411D-03FE-5179-08905B245FA7";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 1;
	setAttr ".cc" -type "nurbsSurface" 
		1 1 0 0 no 
		5 0 0.5 1 1.5 2
		7 0 0.51763809020504148 1.035276180410083 1.5529142706151244 2.0705523608201659
		 2.5881904510252074 3.1058285412302489
		
		35
		0 -0.99999999999999989 -1
		0.49999999999999994 -1 -0.86602540378443882
		0.8660254037844386 -1 -0.50000000000000022
		1 -1 -3.4450928483976665e-16
		0.86602540378443882 -1 0.49999999999999967
		0.50000000000000033 -1 0.86602540378443849
		4.4981039857617246e-16 -1 0.99999999999999989
		0 -0.49999999999999994 -1
		0.49999999999999994 -0.49999999999999994 -0.86602540378443871
		0.8660254037844386 -0.49999999999999994 -0.50000000000000011
		1 -0.5 -3.1389311486108282e-16
		0.86602540378443882 -0.5 0.49999999999999967
		0.50000000000000033 -0.5 0.8660254037844386
		4.4981039857617246e-16 -0.50000000000000011 1
		0 5.7211887261098333e-18 -1
		0.49999999999999994 -2.4823892950124813e-18 -0.86602540378443871
		0.8660254037844386 -2.4894981252573991e-17 -0.50000000000000011
		1 -5.5511151231257809e-17 -2.8327694488239898e-16
		0.86602540378443882 -8.6127321209941639e-17 0.49999999999999972
		0.50000000000000033 -1.0853991316750316e-16 0.8660254037844386
		4.4981039857617246e-16 -1.167434911886255e-16 1
		0 0.50000000000000011 -1
		0.49999999999999994 0.5 -0.86602540378443871
		0.8660254037844386 0.5 -0.50000000000000011
		1 0.5 -2.5266077490371514e-16
		0.86602540378443882 0.49999999999999994 0.49999999999999978
		0.50000000000000033 0.49999999999999994 0.8660254037844386
		4.4981039857617246e-16 0.49999999999999994 1
		0 1 -0.99999999999999989
		0.49999999999999994 1 -0.8660254037844386
		0.8660254037844386 1 -0.5
		1 1 -2.2204460492503131e-16
		0.86602540378443882 1 0.49999999999999978
		0.50000000000000033 1 0.86602540378443871
		4.4981039857617246e-16 0.99999999999999989 1
		
		;
createNode transform -n "armour_nurbs_lattice" -p "armour_nurbsGuide_grp";
	rename -uid "6B65C7B4-45B9-2198-AEF8-AB8152A5CD4B";
createNode transform -n "ffd1Lattice" -p "armour_nurbs_lattice";
	rename -uid "D5AF3A3C-4176-2100-54DB-CF91A6272AF0";
	setAttr ".t" -type "double3" 0.5 0 0 ;
	setAttr ".s" -type "double3" 1 2 2 ;
createNode lattice -n "ffd1LatticeShape" -p "ffd1Lattice";
	rename -uid "C7C50C12-411D-3F79-03D2-66BBB2BD2762";
	setAttr -k off ".v";
	setAttr ".td" 2;
	setAttr ".cc" -type "lattice" 2 2 2 8 -0.5 -0.5 -0.5 0.5 -0.5
		 -0.5 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5 ;
createNode transform -n "ffd1Base" -p "armour_nurbs_lattice";
	rename -uid "757D18FE-4268-4CE8-DB8D-66B039F0F729";
	setAttr ".t" -type "double3" 0.5 0 0 ;
	setAttr ".s" -type "double3" 1 2 2 ;
createNode baseLattice -n "ffd1BaseShape" -p "ffd1Base";
	rename -uid "C26C6386-4DF1-31CA-FADD-13A945013643";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
createNode transform -s -n "persp";
	rename -uid "78EC5063-4F8C-E3EC-9F09-528B034F8373";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 4.8066581774984209 2.3467461328972394 1.6021073771193322 ;
	setAttr ".r" -type "double3" -26.738352729609385 68.600000000003007 -8.7167910319034756e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "AA9579A0-497B-0D09-B10F-0EAF071C12AE";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 4.9396429840400593;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0.5 0 0 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "9BB70A46-4AEA-6AFF-2983-E5B7786C4F4A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "D3684272-41C9-1E31-F9D1-C99C0CC36B5C";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "A6DC08F8-4503-0C99-69D3-87AAC7173573";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "721C6E38-4309-4DCF-BFC3-6490F28195D3";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "50833B75-4DC7-B303-A4DA-E983BBBEBAD4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "3DA058CA-42FC-12EB-6FEF-97BB3343CEB3";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode materialInfo -n "materialInfo1";
	rename -uid "031E689C-4C39-20A2-1C93-75B3054F06D7";
createNode shadingEngine -n "surfaceShader1SG";
	rename -uid "A7C4B536-416F-CD93-E46F-FDB146195AF4";
	setAttr ".ihi" 0;
	setAttr -s 4 ".dsm";
	setAttr ".ro" yes;
createNode surfaceShader -n "surfaceShader1";
	rename -uid "4335201C-4973-0302-2F71-77B86676B8EA";
	setAttr ".oc" -type "float3" 0.38589999 0.0902 0.0902 ;
	setAttr ".ot" -type "float3" 0.64361703 0.64361703 0.64361703 ;
createNode makeNurbCylinder -n "armour_surGuide_makeNurb";
	rename -uid "28245E9D-4614-A893-6E62-4B9B12EBC65A";
	setAttr ".ax" -type "double3" 0 1 0 ;
	setAttr ".ssw" -90;
	setAttr ".esw" 90;
	setAttr ".d" 1;
createNode rebuildSurface -n "armour_surGuide_rebuildSurface";
	rename -uid "674ECE77-4042-23EA-BA11-2E82B71CB230";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "3C641F3F-456F-60FB-5E1A-D29AD962304E";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "5FBBAD56-4CD3-CCFA-4EC7-BEB89C9D2D36";
	setAttr ".bsdt[0].bscd" -type "Int32Array" 1 0 ;
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "DA31A3BF-4883-2C82-8CF4-CABF96D08462";
createNode displayLayerManager -n "layerManager";
	rename -uid "B9A609C0-4931-6CCE-7593-0BA07BE15E7F";
createNode displayLayer -n "defaultLayer";
	rename -uid "876FE680-40F2-D50E-8DA9-27BF295FAE08";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "F75458BD-4052-EAA0-9A3C-D69641AC8745";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "F3C9996A-48E0-7FF3-A2B1-F99CD3F38B51";
	setAttr ".g" yes;
createNode tweak -n "tweak1";
	rename -uid "C46F0CBF-4A63-E834-37CF-938417B50501";
createNode objectSet -n "tweakSet1";
	rename -uid "B4F1A07F-4B75-3E00-42E7-FAB0EF421D8C";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	rename -uid "9BB5F1A3-4C14-351E-B696-F486E1729165";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	rename -uid "B14629DF-4FF0-6AFE-3BDA-1BB95156A2F4";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode blendShape -n "head_geo_coreModel_CorrectBlendShape";
	rename -uid "5842AC01-4741-F902-74DC-9599C3C80FD0";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".w[0]"  1;
	setAttr ".mlid" 0;
	setAttr ".mlpr" 0;
	setAttr ".pndr[0]"  0;
	setAttr ".tgvs[0]" yes;
	setAttr ".tpvs[0]" yes;
	setAttr ".tgdt[0].cid" -type "Int32Array" 1 0 ;
	setAttr ".aal" -type "attributeAlias" {"armour_nurbs_guide1","weight[0]"} ;
createNode objectSet -n "head_geo_coreModel_CorrectBlendShapeSet";
	rename -uid "D58073E0-4FC9-985D-CE1B-51BA09539B0C";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "head_geo_coreModel_CorrectBlendShapeGroupId";
	rename -uid "144740C6-45AF-C51F-0DA4-E58EC855C1C1";
	setAttr ".ihi" 0;
createNode groupParts -n "head_geo_coreModel_CorrectBlendShapeGroupParts";
	rename -uid "D7E8D414-4CFA-94AF-8939-078341312ED7";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode ffd -n "ffd1";
	rename -uid "CEABB219-405A-357C-27E8-3B88D0632511";
	setAttr ".lo" yes;
createNode objectSet -n "ffd1Set";
	rename -uid "DEC66D2B-42F4-A140-B6A2-6B8F5FCDA4BD";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "ffd1GroupId";
	rename -uid "BA60A851-4178-7066-3F1B-63BAC74E66DF";
	setAttr ".ihi" 0;
createNode groupParts -n "ffd1GroupParts";
	rename -uid "A651459A-4BAE-4F51-2974-1BBCEE492FA3";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "362CC7DF-472E-8CB3-0771-5792520D3DA9";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "5E96BC20-4D5B-A5C2-23BB-34B88C551C41";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -393.09790246683008 -249.57923221030052 ;
	setAttr ".tgi[0].vh" -type "double2" 1206.90205265438 531.93335091087874 ;
	setAttr -s 4 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 307.39495849609375;
	setAttr ".tgi[0].ni[0].y" 138.40335083007813;
	setAttr ".tgi[0].ni[0].nvs" 18306;
	setAttr ".tgi[0].ni[1].x" 298.57144165039063;
	setAttr ".tgi[0].ni[1].y" 362.85714721679688;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" -131.260498046875;
	setAttr ".tgi[0].ni[2].y" 155.79832458496094;
	setAttr ".tgi[0].ni[2].nvs" 18306;
	setAttr ".tgi[0].ni[3].x" 320;
	setAttr ".tgi[0].ni[3].y" 232.85714721679688;
	setAttr ".tgi[0].ni[3].nvs" 18304;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av -k on ".unw" 1;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rm";
	setAttr -av -k on ".lm";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av -k on ".hom";
	setAttr -av -k on ".hodm";
	setAttr -av -k on ".xry";
	setAttr -av -k on ".jxr";
	setAttr -av -k on ".sslt";
	setAttr -av -k on ".cbr";
	setAttr -av -k on ".bbr";
	setAttr -av -k on ".mhl";
	setAttr -av -k on ".cons";
	setAttr -av -k on ".vac";
	setAttr -av -k on ".hwi";
	setAttr -av -k on ".csvd";
	setAttr -av -k on ".ta";
	setAttr -av -k on ".tq";
	setAttr -av -k on ".ts";
	setAttr -av -k on ".etmr";
	setAttr -av -k on ".tmr";
	setAttr -av -k on ".aoon";
	setAttr -av -k on ".aoam";
	setAttr -av -k on ".aora";
	setAttr -av -k on ".aofr";
	setAttr -av -k on ".aosm";
	setAttr -av -k on ".hff";
	setAttr -av -k on ".hfd";
	setAttr -av -k on ".hfs";
	setAttr -av -k on ".hfe";
	setAttr -av ".hfc";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av -k on ".hfa";
	setAttr -av -k on ".mbe";
	setAttr -av -k on ".mbt";
	setAttr -av -k on ".mbsof";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".mbc";
	setAttr -av -k on ".mbfa";
	setAttr -av -k on ".mbftb";
	setAttr -av -k on ".mbftg";
	setAttr -av -k on ".mbftr";
	setAttr -av -k on ".mbfta";
	setAttr -av -k on ".mbfe";
	setAttr -av -k on ".mbme";
	setAttr -av -k on ".mbcsx";
	setAttr -av -k on ".mbcsy";
	setAttr -av -k on ".mbasx";
	setAttr -av -k on ".mbasy";
	setAttr -av -k on ".blen";
	setAttr -av -k on ".blth";
	setAttr -av -k on ".blfr";
	setAttr -av -k on ".blfa";
	setAttr -av -k on ".blat";
	setAttr -av -k on ".msaa";
	setAttr -av -k on ".aasc";
	setAttr -av -k on ".aasq";
	setAttr -av -k on ".laa";
	setAttr -k on ".fprt" yes;
	setAttr -av -k on ".rtfm";
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -k on ".hio";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -k on ".hio";
lockNode -l 0 -lu 1;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -av -k off -cb on ".fbfm";
	setAttr -av -k off -cb on ".ehql";
	setAttr -av -k off -cb on ".eams";
	setAttr -av -k off -cb on ".eeaa";
	setAttr -av -k off -cb on ".engm";
	setAttr -av -k off -cb on ".mes";
	setAttr -av -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -av -k off -cb on ".mbs";
	setAttr -av -k off -cb on ".trm";
	setAttr -av -k off -cb on ".tshc";
	setAttr -av -k off -cb on ".enpt";
	setAttr -av -k off -cb on ".clmt";
	setAttr -av -k off -cb on ".tcov";
	setAttr -av -k off -cb on ".lith";
	setAttr -av -k off -cb on ".sobc";
	setAttr -av -k off -cb on ".cuth";
	setAttr -av -k off -cb on ".hgcd";
	setAttr -av -k off -cb on ".hgci";
	setAttr -av -k off -cb on ".mgcs";
	setAttr -av -k off -cb on ".twa";
	setAttr -av -k off -cb on ".twz";
	setAttr -av -k on ".hwcc";
	setAttr -av -k on ".hwdp";
	setAttr -av -k on ".hwql";
	setAttr -av -k on ".hwfr";
	setAttr -av -k on ".soll";
	setAttr -av -k on ".sosl";
	setAttr -av -k on ".bswa";
	setAttr -av -k on ".shml";
	setAttr -av -k on ".hwel";
select -ne :ikSystem;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".gsn";
	setAttr -k on ".gsv";
	setAttr -s 4 ".sol";
connectAttr "ffd1.og[0]" "armour_nurbs_guideShape.cr";
connectAttr "ffd1GroupId.id" "armour_nurbs_guideShape.iog.og[2].gid";
connectAttr "ffd1Set.mwc" "armour_nurbs_guideShape.iog.og[2].gco";
connectAttr "groupId2.id" "armour_nurbs_guideShape.iog.og[3].gid";
connectAttr "tweakSet1.mwc" "armour_nurbs_guideShape.iog.og[3].gco";
connectAttr "head_geo_coreModel_CorrectBlendShapeGroupId.id" "armour_nurbs_guideShape.iog.og[5].gid"
		;
connectAttr "head_geo_coreModel_CorrectBlendShapeSet.mwc" "armour_nurbs_guideShape.iog.og[5].gco"
		;
connectAttr "armour_surGuide_makeNurb.os" "armour_nurbs_guideShapeOrig.cr";
connectAttr "armour_nurbs_guide.t" "armour_nurbs_normal_grp.t";
connectAttr "armour_nurbs_guide.r" "armour_nurbs_normal_grp.r";
connectAttr "armour_nurbs_guide.s" "armour_nurbs_normal_grp.s";
connectAttr "armour_surGuide_rebuildSurface.os" "armour_nurbs_normalShape.cr";
connectAttr "armour_nurbs_guide.t" "armour_nurbs_center_grp.t";
connectAttr "armour_nurbs_guide.r" "armour_nurbs_center_grp.r";
connectAttr "armour_nurbs_guide.s" "armour_nurbs_center_grp.s";
connectAttr "armour_nurbs_guideShape.ws" "armour_nurbs_centerShape.cr";
connectAttr "armour_surGuide_makeNurb.os" "armour_nurbs_blendShape.cr";
connectAttr "armour_nurbs_guide.t" "armour_nurbs_lattice.t";
connectAttr "armour_nurbs_guide.r" "armour_nurbs_lattice.r";
connectAttr "armour_nurbs_guide.s" "armour_nurbs_lattice.s";
connectAttr "surfaceShader1SG.msg" "materialInfo1.sg";
connectAttr "surfaceShader1.msg" "materialInfo1.m";
connectAttr "surfaceShader1.msg" "materialInfo1.t" -na;
connectAttr "surfaceShader1.oc" "surfaceShader1SG.ss";
connectAttr "armour_nurbs_guideShape.iog" "surfaceShader1SG.dsm" -na;
connectAttr "armour_nurbs_centerShape.iog" "surfaceShader1SG.dsm" -na;
connectAttr "armour_nurbs_normalShape.iog" "surfaceShader1SG.dsm" -na;
connectAttr "armour_nurbs_blendShape.iog" "surfaceShader1SG.dsm" -na;
connectAttr "armour_nurbs_guide.spans_v" "armour_surGuide_makeNurb.s";
connectAttr "armour_nurbs_guide.spans_u" "armour_surGuide_makeNurb.nsp";
connectAttr "armour_nurbs_guideShape.ws" "armour_surGuide_rebuildSurface.is";
connectAttr "armour_surGuide_makeNurb.s" "armour_surGuide_rebuildSurface.sv";
connectAttr "armour_surGuide_makeNurb.nsp" "armour_surGuide_rebuildSurface.su";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "surfaceShader1SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "surfaceShader1SG.message" ":defaultLightSet.message";
connectAttr "head_geo_coreModel_CorrectBlendShape.mlpr" "shapeEditorManager.bspr[0]"
		;
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "armour_nurbs_guideShape.iog.og[3]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "armour_nurbs_guideShapeOrig.ws" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "head_geo_coreModel_CorrectBlendShapeGroupParts.og" "head_geo_coreModel_CorrectBlendShape.ip[0].ig"
		;
connectAttr "head_geo_coreModel_CorrectBlendShapeGroupId.id" "head_geo_coreModel_CorrectBlendShape.ip[0].gi"
		;
connectAttr "armour_nurbs_blendShape.ws" "head_geo_coreModel_CorrectBlendShape.it[0].itg[0].iti[6000].igt"
		;
connectAttr "shapeEditorManager.obsv[0]" "head_geo_coreModel_CorrectBlendShape.tgdt[0].dpvs"
		;
connectAttr "head_geo_coreModel_CorrectBlendShapeGroupId.msg" "head_geo_coreModel_CorrectBlendShapeSet.gn"
		 -na;
connectAttr "armour_nurbs_guideShape.iog.og[5]" "head_geo_coreModel_CorrectBlendShapeSet.dsm"
		 -na;
connectAttr "head_geo_coreModel_CorrectBlendShape.msg" "head_geo_coreModel_CorrectBlendShapeSet.ub[0]"
		;
connectAttr "ffd1GroupParts.og" "head_geo_coreModel_CorrectBlendShapeGroupParts.ig"
		;
connectAttr "head_geo_coreModel_CorrectBlendShapeGroupId.id" "head_geo_coreModel_CorrectBlendShapeGroupParts.gi"
		;
connectAttr "head_geo_coreModel_CorrectBlendShape.og[0]" "ffd1.ip[0].ig";
connectAttr "ffd1GroupId.id" "ffd1.ip[0].gi";
connectAttr "ffd1LatticeShape.wm" "ffd1.dlm";
connectAttr "ffd1LatticeShape.lo" "ffd1.dlp";
connectAttr "ffd1BaseShape.wm" "ffd1.blm";
connectAttr "ffd1GroupId.msg" "ffd1Set.gn" -na;
connectAttr "armour_nurbs_guideShape.iog.og[2]" "ffd1Set.dsm" -na;
connectAttr "ffd1.msg" "ffd1Set.ub[0]";
connectAttr "tweak1.og[0]" "ffd1GroupParts.ig";
connectAttr "ffd1GroupId.id" "ffd1GroupParts.gi";
connectAttr "armour_nurbs_lattice.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "armour_nurbs_guideShapeOrig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "armour_nurbs_guide.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "armour_nurbs_guideShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "surfaceShader1SG.pa" ":renderPartition.st" -na;
connectAttr "surfaceShader1.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of armour_guide_test.ma
