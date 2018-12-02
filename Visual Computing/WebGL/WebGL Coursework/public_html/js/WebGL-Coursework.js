"use strict"; // https://stackoverflow.com/q/1335851/72470
/*-------------------------------- Globals -----------------------------------*/
var camera, defaultCamera, scene, renderer;
var cube, bunny;
var rubiksCube, perfectRubiksCube;
var animationID; 
var activeObject;

var textureLoader = new THREE.TextureLoader();
var objLoader = new THREE.OBJLoader();
textureLoader.setPath("resources/");
objLoader.setPath("resources/");

var sqr = val => val*val;
var sum = (accumulator, val) => accumulator + val;

/*-------------------------------- Defaults ----------------------------------*/
var Defaults = {
    backgroundColor: new THREE.Color(0x000000),
    cameraPos: [3, 4, 5],
    cameraLookAt: new THREE.Vector3(0, 0, 0),
    cubeColor: new THREE.Color(0x00fB8B),
    wireframeColor: new THREE.Color(0xffff00),
    pointsColor: new THREE.Color(0xffffff),
    pointsSize: 0.075,
    bunnyColor: new THREE.Color(0xf44298),
    bunnyScaling: 0.3,
    bunnyPointsSize: 0.01,
    axisLength: 4,
    rotationStep: 0.01, 
    cameraMovementDistance: 0.1
};

/*------------------------------ Object States -------------------------------*/                 
var States = {
    rotating: {
        on: false,
        axis: 'x'
    },
    vertexRendering: false,
    edgeRendering: false, 
    faceRendering: false,
    textureRendering: false,
    orbiting: false,
    bunnyLoaded: false, 
    cubeDisplayed: false,
    bunnyDisplayed: false, 
    rubiksCubeMode: false, 
    rubiksCubeGenerated: false
};

/*-------------------------------- Init Call ---------------------------------*/
init();
rotateObj();
States.rotating.on = true;

/*------------------------------- Scene Setup --------------------------------*/
function init () {
    scene = new THREE.Scene();
    scene.background = Defaults.backgroundColor;
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio); // HiDPI/retina rendering
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    
    // Lights Setup
    var ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    
    var lights = [];
    lights[0] = new THREE.PointLight(0xffffff, 1, 0);
    lights[1] = new THREE.PointLight(0xffffff, 1, 0);
    lights[2] = new THREE.PointLight(0xffffff, 1, 0);

    lights[0].position.set(0, 200, 0);
    lights[1].position.set(100, 200, 100);
    lights[2].position.set(-100, -200, -100 );

    for (var i = 0; i < lights.length; i++) { scene.add(lights[i]); }

    // Event Listeners
    document.addEventListener("keydown", onKeyDown);
    document.addEventListener("wheel", onWheelScroll);
    document.addEventListener("mousedown", onMouseDown);
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
    window.addEventListener('resize', onResize, false);

    // Default Camera Positioning
    defaultCamera = camera.clone();  
    defaultCamera.position.set(
                Defaults.cameraPos[0], 
                Defaults.cameraPos[1],
                Defaults.cameraPos[2]
            );
    
    resetCamera();
    cubeSetup();
    axesSetup();
}

function resetCamera () {
    camera = defaultCamera.clone(); 
    if (States.rubiksCubeMode) {
        camera.position.set(
            3.8403576514431155,
            2.2156435527398592,
            5.262113506418356 
        );
    }
    camera.lookAt(Defaults.cameraLookAt);
}

function cubeSetup () {
    var geometry = new THREE.BoxGeometry(2, 2, 2);  
    var material = new THREE.MeshPhongMaterial({color: Defaults.cubeColor, vertexColors: THREE.VertexColors , flatShading: true});
    var pointsMaterial = new THREE.PointsMaterial({color:Defaults.pointsColor, size: Defaults.pointsSize});
    var points = new THREE.Points(geometry, pointsMaterial);
    var wireframeMaterial = new THREE.MeshBasicMaterial({color: Defaults.wireframeColor, wireframe: true});           
    var wireframe = new THREE.Mesh(geometry, wireframeMaterial);
   
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    activeObject = cube;
    States.cubeDisplayed = true;
    
    cube.userData.material = material;
    cube.userData.pointsMaterial = pointsMaterial;
    cube.userData.points = points;
    cube.userData.wireframeMaterial = wireframeMaterial;  
    cube.userData.wireframe = wireframe;    
    cube.userData.textures = [];
}

function axesSetup () {
    var xAxisGeometry = new THREE.Geometry();
    var yAxisGeometry = xAxisGeometry.clone();
    var zAxisGeometry = xAxisGeometry.clone();
    var xAxisMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });
    var yAxisMaterial = new THREE.LineBasicMaterial({ color: 0x00ff00 });
    var zAxisMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff });

    xAxisGeometry.vertices.push(
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(Defaults.axisLength, 0, 0)
    );

    yAxisGeometry.vertices.push(
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, Defaults.axisLength, 0)
    );

    zAxisGeometry.vertices.push(
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, 0, Defaults.axisLength)
    );

    var xAxis = new THREE.Line(xAxisGeometry, xAxisMaterial);
    var yAxis = new THREE.Line(yAxisGeometry, yAxisMaterial);
    var zAxis = new THREE.Line(zAxisGeometry, zAxisMaterial);

    scene.add(xAxis, yAxis, zAxis);       
}

//function wallSetup () 
/*----------------------------- Object Rotation ------------------------------*/
function rotateObj () {
    var obj = activeObject;
    animationID = requestAnimationFrame(rotateObj); 
    obj.rotation[States.rotating.axis] += Defaults.rotationStep;
    zeroOtherAxes();
    
    if (obj.rotation[States.rotating.axis] >= 2*Math.PI){
        obj.rotation[States.rotating.axis] = 0;
        cancelAnimationFrame(animationID); 

        switch (States.rotating.axis) {
            case 'x':
                States.rotating.axis = 'y';
                break;
            case 'y':
                States.rotating.axis = 'z';
                break
            default:
                States.rotating.axis = 'x';
                break;
        }
        rotateObj();
    }
    renderer.render(scene, camera);
}

function zeroOtherAxes() {
    var obj = activeObject;
    
    if (obj.rotation.x !== 0) { 
        obj.rotation.y = 0;
        obj.rotation.z = 0;                               
    }
    if (obj.rotation.y !== 0) {
        obj.rotation.x = 0;
        obj.rotation.z = 0;
    }
    if (obj.rotation.z !== 0) {
        obj.rotation.x = 0;
        obj.rotation.y = 0;
    }    
}

function toggleRotation ()  {
    var obj = activeObject;
    if (States.rotating.on){
        cancelAnimationFrame(animationID); 
    } else {
        if (obj.rotation.y !== 0){
            States.rotating.axis = 'y';
        } else if (obj.rotation.z !== 0){
            States.rotating.axis = 'z';
        } else { 
            States.rotating.axis = 'x';                                 
        }
        rotateObj();
    }
    States.rotating.on = !States.rotating.on; 
}

/*------------------------------ Render Modes --------------------------------*/
function toggleEdges (obj) {
    if (!States.edgeRendering){ 
        obj.add(obj.userData.wireframe);
    } else {
        obj.remove(obj.userData.wireframe);
    }
    States.edgeRendering = !States.edgeRendering; 
}

function toggleFaces (obj) {
    if (!States.textureRendering)   { 
        if (!States.faceRendering){
             obj.traverse(
                function (child) {
                    if (child.material !== undefined && child.material.isMaterial && !child.material.wireframe && !child.isPoints) {
                        child.material.opacity = 0.0;
                        child.material.transparent = true;
                    }        
                });
        } else {
            obj.traverse(
                function (child) {
                    if (child.material !== undefined && child.material.isMaterial && !child.material.wireframe && !child.isPoints) { 
                        child.material.opacity = 1.0;
                        child.material.transparent = false;
                    }        
                });
        }    
        States.faceRendering = !States.faceRendering;
    }
}    

function toggleVertices (obj) {
if (!States.vertexRendering){
        obj.add(obj.userData.points);
    } else {
        obj.remove(obj.userData.points);
    }     
    States.vertexRendering = !States.vertexRendering;   
}

/*---------------------------- Camera Translation ----------------------------*/    
function translateCamera (direction) {
    switch (direction){
        case 'left':
            camera.translateX(-Defaults.cameraMovementDistance);
            break;
        case 'up':
             camera.translateY(Defaults.cameraMovementDistance);
            break;
        case 'right':
            camera.translateX(Defaults.cameraMovementDistance);                              
            break;
        case 'down':
            camera.translateY(-Defaults.cameraMovementDistance);
            break;
        case 'forwards':
            camera.translateZ(-Defaults.cameraMovementDistance);
            break;
        case 'backwards':
            camera.translateZ(Defaults.cameraMovementDistance);
            break;
        default:
            break;
    }
};

/*------------------------------ Camera Orbit --------------------------------*/   
var Orbit = {
    started: false,
    xStart: 0, 
    yStart: 0,
    xMove: 0,
    yMove: 0,
    xSensitivity: 7.25,
    ySensitivity: 6.5,
    xMax: Defaults.axisLength,
    yMax: Defaults.axisLength,
    xMaxStep: 0.8,
    yMaxStep: 0.8,
    radius: 0,
    cameraDistance: 0,
    lookAtPoint: null
};
       
function orbitCamera () {
    var screen2Cartesian = function (xScreen, yScreen) {
    var result = [];
    result.push(-1 + (2*xScreen/window.innerWidth));
    result.push(-(-1 + (2*yScreen/window.innerHeight))); 
    var zSquared = sqr(result[0]) + sqr(result[1]);
    result.push(zSquared);
    if (!Orbit.started) { Orbit.radius = zSquared; }
    if (zSquared <= Orbit.radius){
        result[2] = Math.sqrt(Orbit.radius - zSquared);
    } else {
        result = result.map(x => x / zSquared);        
    }
    return new THREE.Vector3(result[0], result[1], result[2]);  
};  
    var getXYZDistances = function (point1, point2) {
        var xDistance = point1.x - point2.x;
        var yDistance = point1.y - point2.y;
        var zDistance = point1.z - point2.z;
        return [xDistance, yDistance, zDistance];
    };
    var getDistance = function (point1, point2) {
        var distances = getXYZDistances(point1, point2);
        return Math.sqrt(sqr(distances[0])+sqr(distances[1])+sqr(distances[2]));
    };   
    var fixDistance = function (cameraPos, lookAtPos, distance) {
        var distances = getXYZDistances(cameraPos, lookAtPos);
        var newCameraZ = Math.sqrt(
            sqr(distance) - sqr(distances[0]) -  sqr(distances[1])
        );
        
        if (Math.abs(distance[2]) < 0.2 || Number.isNaN(newCameraZ) ) { 
            newCameraZ = 0.2;
            Orbit.xMax = cameraPos.x; Orbit.yMax = cameraPos.y;       
        }
        return newCameraZ;
    };
    
    if (!Orbit.started) {
        Orbit.lookAtPoint = screen2Cartesian(Orbit.xStart, Orbit.yStart);
        Orbit.cameraDistance = getDistance(camera.position, Orbit.lookAtPoint);
        Orbit.started = true;                          
    } else {
        if (Orbit.xMove !== 0 || Orbit.yMove !== 0) {      
            var xDiff = Orbit.xMove/window.innerWidth;
            var yDiff = Orbit.yMove/window.innerHeight;
            var xTrans = (Math.abs(xDiff) <= Orbit.xMaxStep)? xDiff : Orbit.xMaxStep; 
            var yTrans = (Math.abs(yDiff) <= Orbit.yMaxStep)? yDiff : Orbit.yMaxStep;
            var xTransAdj = -Orbit.xSensitivity * xTrans;
            var yTransAdj = Orbit.ySensitivity * yTrans;
            camera.translateX(xTransAdj); camera.translateY(yTransAdj); 
        }
    }
    camera.lookAt(Orbit.lookAtPoint);
    var newCameraDistance = getDistance(camera.position, Orbit.lookAtPoint);
    if (newCameraDistance !== Orbit.cameraDistance) {
       var newZ = fixDistance(
            camera.position, Orbit.lookAtPoint, Orbit.cameraDistance
        );
        camera.position.z = newZ;
    }
};

/*------------------------------ Cube Texture --------------------------------*/ 
var textureNames = ['bronze', 'wire', 'scratched', 'shapes', 'colour', 'water'];
for (var texture in textureNames){                          
    cube.userData.textures.push(new THREE.MeshBasicMaterial({
        map: textureLoader.load(textureNames[texture] + '.jpg')
    }));
}

function toggleTextures () {
    if (activeObject === cube){
        if (!States.textureRendering){
            cube.material = cube.userData.textures;
        } else {
            cube.material = cube.userData.material;
        }
        States.faceRendering = false;
        States.textureRendering = !States.textureRendering;      
    }
 };

/*------------------ Object Loading/Switch Active Object ---------------------*/
function loadBunny (filename) {                            
    var material = new THREE.MeshPhongMaterial({color: Defaults.bunnyColor});
    var pointsMaterial = cube.userData.pointsMaterial.clone();
    pointsMaterial.size = Defaults.bunnyPointsSize; 
    var wireframeMaterial = cube.userData.wireframeMaterial.clone();
    var points, wireframe;

    objLoader.load(filename,

        function(object) {   
            bunny = object;                                                  
            bunny.traverse( function (child) {
                    if (child.isMesh) { 
                        child.material = material;
                        points = new THREE.Points(child.geometry, pointsMaterial);
                        wireframe = new THREE.Mesh(child.geometry, wireframeMaterial);
                        bunny.userData.points = points;
                        bunny.userData.wireframe = wireframe;
                    }        
            });
            
            bunny.scale.x = Defaults.bunnyScaling;
            bunny.scale.y = Defaults.bunnyScaling; 
            bunny.scale.z = Defaults.bunnyScaling;
            
            scene.add(bunny);
                    
            States.bunnyDisplayed = true;
            toggleActiveObject();
            States.bunnyLoaded = true;
        }
    );
}
        
function toggleActiveObject () {
    if (activeObject === cube) {
        if (!States.bunnyDisplayed) { scene.add(bunny); } 
        if (States.textureRendering) { toggleTextures(); }
        if (!States.edgeRendering) { toggleEdges(cube); }                               
        if (!States.faceRendering) { toggleFaces(cube); }     
        States.faceRendering = false;
        States.edgeRendering = false;  
        activeObject = bunny;
    } else {
        if (!States.cubeDisplayed) { scene.add(cube); } 
        States.faceRendering = !States.faceRendering;
        activeObject = cube;
    }     
}

function toggleNonActiveObjectDisplay () {            
    if (activeObject === cube && States.bunnyLoaded) {
        if (States.bunnyDisplayed) {
            scene.remove(bunny);
        } else {
            scene.add(bunny);
        }
        States.bunnyDisplayed = !States.bunnyDisplayed;
    } else {
        if (States.bunnyLoaded) { 
            if (States.cubeDisplayed) {
                scene.remove(cube);
            } else {
                scene.add(cube);
            }
            States.cubeDisplayed = !States.cubeDisplayed;
        }
    }
}

/*--------------------------- Rubik's Cube Mode ------------------------------*/
function toggleRubiksCube () {
    if (!States.rubiksCubeMode){
        if (States.rotating.on) { toggleRotation(); }       
        if (!States.rubiksCubeGenerated) { generateRubiksCube(); }
        scene.add(rubiksCube);
    } else {  
        scene.remove(rubiksCube);
        if (!States.rotating.on) { toggleRotation(); }
    }
    
    States.rubiksCubeMode = !States.rubiksCubeMode;
    resetCamera();
}

var rubiksColors = [0xff0000, 0xffa500, 0xffffff, 0xffff00, 0x00ff00, 0x0000ff];
    
var FaceIndexes = {
    'r': 0,
    'l': 2,
    'u': 4,
    'd': 6,
    'f': 8,
    'b': 10
};

var RubiksMap = {
    'cube0': {
        faces: ['l', 'u', 'f'],
        colors: [1, 2, 4],
        position: [-1, 1, 1]
    },
    'cube1': {
        faces: ['u', 'f'],
        colors: [2, 4],
        position: [0, 1, 1]
    },
    'cube2': {
        faces: ['r', 'u', 'f'],
        colors: [0, 2, 4],
        position: [1, 1, 1] 
    },
    'cube3': {
        faces: ['l', 'f'],
        colors: [1, 4],
        position: [-1, 0, 1] 
    },
    'cube4': {
        faces: ['f'],
        colors: [4],
        position: [0, 0, 1] 
    },
    'cube5': {
        faces: ['r', 'f'],
        colors: [0, 4],
        position: [1, 0, 1] 
    },
    'cube6': {
        faces: ['l', 'd', 'f'],
        colors: [1, 3, 4],
        position: [-1, -1, 1] 
    },
    'cube7': {
        faces: ['d', 'f'],
        colors: [3, 4],
        position: [0, -1, 1] 
    },
    'cube8': {
        faces: ['r', 'd', 'f'],
        colors: [5, 3, 4],
        position: [1, -1, 1] 
    },
    'cube9': {
        faces: ['l', 'u'],
        colors: [1, 2],
        position: [-1, 1, 0] 
    },
    'cube10': {
        faces: ['u'],
        colors: [2],
        position: [0, 1, 0] 
    },
    'cube11': {
        faces: ['r', 'u'],
        colors: [0, 2],
        position: [1, 1, 0] 
    },
    'cube12': {
        faces: ['l'],
        colors: [1],
        position: [-1, 0, 0] 
    },
    'cube13': {
        faces: ['r'],
        colors: [0],
        position: [1, 0, 0] 
    },
    'cube14': {
        faces: ['l','d'],
        colors: [1, 3],
        position: [-1, -1, 0] 
    },
    'cube15': {
        faces: ['d'],
        colors: [3],
        position: [0, -1, 0] 
    },
    'cube16': {
        faces: ['r', 'd'],
        colors: [0, 3],
        position: [1, -1, 0] 
    },
    'cube17': {
        faces: ['l', 'u', 'b'],
        colors: [1, 2, 5],
        position: [-1, 1, -1] 
    },
    'cube18': {
        faces: ['u', 'b'],
        colors: [2, 5],
        position: [0, 1, -1] 
    },
    'cube19': {
        faces: ['r', 'u', 'b'],
        colors: [0, 2, 5],
        position: [1, 1, -1] 
    },
    'cube20': {
        faces: ['l', 'b'],
        colors: [1, 5],
        position: [-1, 0, -1] 
    },
    'cube21': {
       faces: ['b'],
       colors: [5],
       position: [0, 0, -1] 
   },
    'cube22': {
       faces: ['r', 'b'],
       colors: [0, 5],
       position: [1, 0, -1] 
   },
    'cube23': {
       faces: ['l', 'd', 'b'],
       colors: [1, 3, 5],
       position: [-1, -1, -1] 
   },
    'cube24': {
       faces: ['d', 'b'],
       colors: [3, 5],
       position: [0, -1, -1] 
   },
    'cube25': {
       faces: ['r', 'd', 'b'],
       colors: [0, 3, 5],
       position: [1, -1, -1] 
   }
};

function generateRubiksCube () {
    var rubiksCubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    var rubiksCubeMaterial = new THREE.MeshPhongMaterial({color: 'white', vertexColors: THREE.FaceColors, flatShading: true}); 
    var cubeWireframe = new THREE.MeshBasicMaterial({color: 'black', wireframe: true});
    rubiksCube = new THREE.Group();
    cubeWireframe = new THREE.Mesh(rubiksCubeGeometry, cubeWireframe);

    for (var i = 0; i < 26; i++) {
        var newCube = new THREE.Mesh(rubiksCubeGeometry, rubiksCubeMaterial);
        var newCubeWireframe = cubeWireframe.clone();
        newCube.add(newCubeWireframe);
        var cubeID = 'cube' + i;
     
        newCube.position.set(
            RubiksMap[cubeID].position[0],
            RubiksMap[cubeID].position[1],
            RubiksMap[cubeID].position[2]
        );
        
        setupSubCubeColors(
            newCube, 
            RubiksMap[cubeID].faces,  
            RubiksMap[cubeID].colors        
        );

        rubiksCube.add(newCube);
    }
    perfectRubiksCube = rubiksCube.clone();
    States.rubiksCubeGenerated = true;
}

function setupSubCubeColors (newCube, newCubeFaces, newCubeColors) {
    var newCubeColorsIndex = 0;
    newCubeFaces.forEach( function (face) {
       var primitiveFaceIndex = FaceIndexes[face]; 
       var currentColor = rubiksColors[newCubeColors[newCubeColorsIndex]];
       for (var i = 0; i < 2; i++) {
           newCube.geometry.faces[primitiveFaceIndex + i].color.setHex(currentColor);
       }
       newCubeColorsIndex++;
    });
}  

// TODO: Fix mixed rotations
function rotateRubiks (side, rotationAxis, axisVal) {
    var activeCubes = []; var preRotationPos = []; var preRotationIndex = [];
    var newPosMapping = [2, 4, 7, 1, 6, 0, 3, 5];
    if (side === 'l' || side === 'd' || side === 'f') { newPosMapping.reverse(); } 

    var cubesSelected = 0; var cubeIndex = 0;
    rubiksCube.children.forEach( 
        function (child) {
            if (activeCubes.length < 9) {
                if (child.position[rotationAxis] === axisVal) {
                    // https://github.com/mrdoob/three.js/issues/7375
                    activeCubes.push(child.clone());
                    activeCubes[cubesSelected].rotation.copy(child.rotation);
                    
                    preRotationPos.push(new THREE.Vector3());
                    preRotationPos[cubesSelected].copy(child.position);
                    preRotationIndex.push(cubeIndex);
                    
                    cubesSelected++;
                } 
                cubeIndex++;
            } 
        }
    );
    activeCubes.splice(4, 1);
    preRotationPos.splice(4, 1);
    preRotationIndex.splice(4, 1);
    var pointer = 0;
    
    activeCubes.forEach(
        function (child) {            
            if (pointer < preRotationPos.length) {
                    child.position.set(
                        preRotationPos[newPosMapping[pointer]].x,
                        preRotationPos[newPosMapping[pointer]].y,
                        preRotationPos[newPosMapping[pointer]].z
                    );
            }
            child.rotation[rotationAxis] += Math.PI/2;
            if (child.rotation[rotationAxis] >= 2*Math.PI) { 
                child.rotation[rotationAxis] = 0
            }
            //console.log(child.rotation);
            var newCubeIndex = preRotationIndex[newPosMapping[pointer]];
            rubiksCube.children[newCubeIndex] = child;
            pointer++;
        }
    );
}

/*------------------------------ Event Handlers ------------------------------*/
function onKeyDown (e) {
    switch (e.which) {
        // Pause object rotation on spacebar Keydown
        case 32:
            toggleRotation();
            break;
        // Move camera left on left arrow Keydown
        case 37: translateCamera('left');
            break;
        // Move camera up on up arrow Keydown
        case 38:
            translateCamera('up');
            break;
        // Move camera right on right arrow Keydown
        case 39:                            
            translateCamera('right');
            break; 
        // Move camera down on down arrow Keydown
        case 40:
            translateCamera('down');
            break;                                
        // Move camera forwards on '+' Keydown; can also be invoked by using the mousewheel
        case 107:
            translateCamera('forwards');
            break;                                
        // Move camera backwards '-' Keydown; can also be invoked by using the mousewheel
        case 109:
            translateCamera('backwards');
            break;
        // Reset camera position on 'r' Keydown
        case 82:
            resetCamera();
            break;
        // Toggle cube edge rendering (inc. primitive triangles) on 'e' Keydown
        case 69:
            toggleEdges(activeObject);
            break;
        // Toggle cube faces on 'f' KeyDown
        case 70: 
            toggleFaces(activeObject);
            break;                      
        // Toggle cube vertex rendering on 'v' Keydown
        case 86: 
            toggleVertices(activeObject);
            break;       
        // Apply textures on 't' Keydown
        case 84: 
            toggleTextures();
            break; 
        // Load/switch active object on 's' Keydown
        case 83: 
            if (!States.bunnyLoaded) { loadBunny('bunny-5000.obj'); }
            else { toggleActiveObject(); }
            break;
        // Toggle non-active object on 'x' Keydown
        case 88: 
            toggleNonActiveObjectDisplay();
            break;
        // Toggle Rubik's cube mode on 'z' Keydown
        case 90: 
            toggleRubiksCube();
            break;
        // Rotate 'front' side of rubiks cube anticlockwise on '1' keydown
        case 49:
        case 97:
            if (States.rubiksCubeMode) { rotateRubiks('f', 'z', 1); }
            break;
        // Rotate 'down' side of rubiks cube anticlockwise on '2' keydown
        case 50:
        case 98:
            if (States.rubiksCubeMode) { rotateRubiks('d', 'y', -1); }
            break;
        // Rotate 'left' side of rubiks cube anticlockwise on '4' keydown
        case 52:
        case 100:
            if (States.rubiksCubeMode) { rotateRubiks('l', 'x', -1); }
            break;
        // Rotate 'right' of rubiks cube anticlockwise on '6' keydown
        case 54:
        case 102:
            if (States.rubiksCubeMode) { rotateRubiks('r', 'x', 1); }
            break;
        // Rotate 'up' of rubiks cube anticlockwise on '8' keydown
        case 56:
        case 104:
            if (States.rubiksCubeMode) { rotateRubiks('u', 'y', 1); }
            break;
        // Rotate 'back' side of rubiks cube anticlockwise on '9' keydown
        case 57:
        case 105:
            if (States.rubiksCubeMode) { rotateRubiks('b', 'z', -1); }
            break;
        default:
            break;                            
    }

    renderer.render(scene, camera);
}

// Used to zoom camera in and out via the scroll wheel
function onWheelScroll (e) {                        
   if (e.wheelDelta > 0){
        translateCamera('forwards');
    } else {
        translateCamera('backwards');
    }
    renderer.render(scene, camera);
}

function onMouseDown (e) {
    if (e.which === 1){
        Orbit.xStart = e.x; Orbit.yStart = e.y;
        States.orbiting = true;
    }
}

function onMouseMove (e) {
    if (States.orbiting){
        Orbit.xMove = e.movementX; Orbit.yMove = e.movementY;
        orbitCamera();
        renderer.render(scene, camera);
    }
}

function onMouseUp () {
    Orbit.started = false;  States.orbiting = false;
    Orbit.xStart = 0;   Orbit.yStart = 0;   Orbit.radius = 0;
    Orbit.xMove = 0;    Orbit.yMove = 0;    Orbit. cameraDistance = 0;
    Orbit.xMax = Defaults.axisLength;  Orbit.yMax =  Orbit.xMax;
    Orbit.lookAtPoint = null;
}  

// Handle resizing of the browser window.
function onResize () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
