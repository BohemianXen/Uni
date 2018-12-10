"use strict"; // https://stackoverflow.com/q/1335851/72470
/*--------------------------------- Globals ----------------------------------*/
var camera, defaultCamera, scene, renderer;
var cube, bunny, xyWall, yzWall, grass;
var rubiksCube, perfectRubiksCube;
var animationID; 
var activeObject;

/*--------------------------------- Loaders ----------------------------------*/
var textureLoader = new THREE.TextureLoader();  
var cubeTextureLoader = new THREE.CubeTextureLoader();
var objLoader = new THREE.OBJLoader();
cubeTextureLoader.setPath("resources/"); textureLoader.setPath("resources/");
objLoader.setPath("resources/");

/*----------------------------------- Math -----------------------------------*/
var PI = Math.PI;
var sqr = val => val*val;

/*-------------------------------- Defaults ----------------------------------*/
var Defaults = {
    backgroundColor: new THREE.Color(0x000000),
    cameraPos: [3, 4, 5],
    cameraZoomPos: [2.5, 1.8, 2.5],
    cameraLookAt: new THREE.Vector3(0, 0, 0),
    cubeColor: new THREE.Color(0x00fB8B),
    wireframeColor: new THREE.Color(0xffff00),
    pointsColor: new THREE.Color(0xffffff),
    pointsSize: 0.075,
    bunnyColor: new THREE.Color(0xf44298),
    bunnyScaling: 0.3,
    bunnyPointsSize: 0.01,
    axisLength: 5,
    rotationStep: 0.01, 
    cameraMovementDistance: 0.1,
    wallDistance: 5
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
    wallsDisplayed: false,
    bunnyDisplayed: false, 
    rubiksCubeMode: false, 
    rubiksCubeGenerated: false
};

/*-------------------------------- Init Call ---------------------------------*/
init();
rotateObj();
States.rotating.on = true; // signals that rotation is occuring

/*------------------------------- Scene Setup --------------------------------*/
function init () {
    scene = new THREE.Scene();
    scene.background = Defaults.backgroundColor;
    camera = new THREE.PerspectiveCamera(
        75, window.innerWidth / window.innerHeight, 0.1, 1000
    );
    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio); // HiDPI/retina rendering
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    document.body.appendChild(renderer.domElement);
    
    // Lights Setup
    var ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    
    var lights = [];
    lights[0] = new THREE.PointLight(0xffffff, 1, 0);
    lights[1] = new THREE.PointLight(0xffffff, 1, 0);
    lights[2] = new THREE.PointLight(0xffffff, 1, 0);

    lights[0].position.set(0, 100, 0);
    lights[1].position.set(10, 10, 5);
    lights[2].position.set(-100, -200, -100);

    for (var i = 0; i < lights.length; i++) { 
        if (i === 1) { lights[i].castShadow = true; }
        scene.add(lights[i]); 
    }

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
    wallSetup();
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

function zoomCamera ()  {
    if (!States.rubiksCubeMode) { 
        camera.position.set(
            Defaults.cameraZoomPos[0],
            Defaults.cameraZoomPos[1],
            Defaults.cameraZoomPos[2]
        );
        camera.lookAt(Defaults.cameraLookAt);
    }
}

function cubeSetup () {
    var geometry = new THREE.BoxGeometry(2, 2, 2);  
    var material = new THREE.MeshPhongMaterial({ 
        color: Defaults.cubeColor, 
        flatShading: true
    });
    var pointsMaterial = new THREE.PointsMaterial({
        color:Defaults.pointsColor,
        size: Defaults.pointsSize
    });
    var points = new THREE.Points(geometry, pointsMaterial);
    var wireframeMaterial = new THREE.MeshBasicMaterial({
        color: Defaults.wireframeColor,
        wireframe: true
    });           
    var wireframe = new THREE.Mesh(geometry, wireframeMaterial);
   
    cube = new THREE.Mesh(geometry, material);
    cube.castShadow = true; // used for scene extension 
    scene.add(cube);
    activeObject = cube; // used for object reliant rotation and render modes 
    States.cubeDisplayed = true; // indicates that the cube is in the scene
    
    // add render mode variants to cube userData
    cube.userData.material = material;
    cube.userData.pointsMaterial = pointsMaterial;
    cube.userData.points = points; 
    cube.userData.wireframeMaterial = wireframeMaterial;  
    cube.userData.wireframe = wireframe;    
    cube.userData.textures = [];
}

function axesSetup () {
    var axesHelper = new THREE.AxesHelper(Defaults.axisLength);
    scene.add(axesHelper);       
}

// extended scenery and shadow for additional credit    
function wallSetup () {
    var dim = Defaults.axisLength + Defaults.wallDistance + 1;
    var geometry = new THREE.BoxGeometry(dim, dim, 1, 10);
    var wallTextures = []; var grassTextures = [];
    // setup texture arrays
    for (var i = 0; i < 6; i++) { 
        wallTextures.push('brick.jpg'); 
        grassTextures.push('grass.jpg');
    }
    
    // map textures to walls/floor
    cubeTextureLoader.minFilter = THREE.NearestFilter; // for non-ideal images
    var wallTexture = cubeTextureLoader.load(wallTextures);
    var grassTexture = cubeTextureLoader.load(grassTextures);
    var wallMaterial = new THREE.MeshPhongMaterial({color: 0xffffff, envMap: wallTexture});
    var grassMaterial = new THREE.MeshPhongMaterial({color: 0xffffff, envMap: grassTexture});
    
    // create wall mesh and adjust wall positions to create scene 
    xyWall = new THREE.Mesh(geometry, wallMaterial);
    yzWall = xyWall.clone();
    xyWall.position.z -= Defaults.wallDistance;
    yzWall.position.x -= Defaults.wallDistance;
    yzWall.rotation.y += PI/2;
    // create grass mesh and adjust positionig to create scene  
    grass = new THREE.Mesh(geometry, grassMaterial);
    grass.rotation.x -= PI/2;
    grass.position.y -= Defaults.wallDistance + 1;
    // accept wall/grass shadows (but do not cast them since false by default)
    xyWall.receiveShadow = true; yzWall.receiveShadow = true;
    grass.receiveShadow = true;
}

// add/remove walls from scene
function toggleWalls () {
    if (!States.wallsDisplayed) { 
        scene.add(xyWall, yzWall, grass); zoomCamera();
    } else { 
        scene.remove(xyWall, yzWall, grass); resetCamera();
    }
    States.wallsDisplayed = !States.wallsDisplayed;
}

/*----------------------------- Object Rotation ------------------------------*/
function rotateObj () {
    var obj = activeObject; // set Obj to the selected on screen object
    animationID = requestAnimationFrame(rotateObj); // get new animation ID 
    obj.rotation[States.rotating.axis] += Defaults.rotationStep;
    zeroOtherAxes(); // used as santity check given effect of switched rotations 
    
    // rotate about different axis after one full rotation
    if (obj.rotation[States.rotating.axis] >= 2*PI) {
        obj.rotation[States.rotating.axis] = 0;
        cancelAnimationFrame(animationID); // reset animation ID 
        // set next rotation axis
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
        rotateObj(); // begin rotating 
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

// pauses rotation
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
/* params:
 * 
 * @param {Mesh} obj - current activeObject (either cube or bunny)
 * @returns {undefined}
 */
function toggleEdges (obj) {
    if (!States.edgeRendering){ obj.add(obj.userData.wireframe); }
    else { obj.remove(obj.userData.wireframe); }
    States.edgeRendering = !States.edgeRendering; // toggle edge state
}

/* params:
 * 
 * @param {Mesh} obj - current activeObject (either cube or bunny)
 * @returns {undefined}
 */
function toggleFaces (obj) {
    if (!States.textureRendering)   { 
        if (!States.faceRendering){
            obj.traverse(
               function (child) {
                    if (child.material !== undefined && child.material.isMaterial 
                        && !child.material.wireframe && !child.isPoints) {
                       child.material.opacity = 0.0; // make faces transparent
                       child.material.transparent = true;
                       child.castShadow = false;
                   }        
               });       
        } else { 
            obj.traverse(
                function (child) {
                    if (child.material !== undefined && child.material.isMaterial 
                        && !child.material.wireframe && !child.isPoints) { 
                        child.material.opacity = 1.0; // make faces opaque
                        child.material.transparent = false;
                        child.castShadow = true;
                    }        
                });
        }    
        States.faceRendering = !States.faceRendering; // toggle face state
    }
}    

/* params:
 * 
 * @param {Mesh} obj - current activeObject (either cube or bunny)
 * @returns {undefined}
 */
function toggleVertices (obj) {
    if (!States.vertexRendering){ obj.add(obj.userData.points); } // add points 
    else { obj.remove(obj.userData.points); } // remove points
    States.vertexRendering = !States.vertexRendering; // toggle vertex state  
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
    xFocus: 0, 
    yFocus: 0,
    xMove: 0,
    yMove: 0,
    xSensitivity: 7.5,
    ySensitivity: 2.5,
    radius: 0,
    lookAtPoint: new THREE.Vector3(), 
    sphere: new THREE.Spherical() // holds the spherical coordinate
};

/* params: 
 * 
 * @param {int} xScreen - mouse x-value on initial click
 * @param {int} yScreen - mouse y-value on initial click
 * @returns {THREE.Vector3}
 */
var screen2Cartesian = function (xScreen, yScreen) {
    // modified from three.js: https://threejs.org/docs/#api/en/core/Raycaster
    var raycaster = new THREE.Raycaster();
    var mouse = new THREE.Vector2();
    var pointFound = false;
    // normalise mouse coords
    mouse.x = -1 + (2*xScreen/window.innerWidth);
    mouse.y = -(-1 + (2*yScreen/window.innerHeight));
    raycaster.setFromCamera( mouse, camera);
    var intersects = raycaster.intersectObjects(scene.children);
    
    var i = 0;
    // search for intersecting object, pointFound is true if so
    for (i; i < intersects.length; i++) {
        if (intersects[i].point !== undefined) { pointFound = true; break; }
    }
    // return the found point or the default look at (origin) otherwise
    return (pointFound) ? intersects[i].point : Orbit.lookAtPoint;
};  

// sets the new lookAt point and calculates the radius (only for debug purposes)
function initOrbit () {
    Orbit.lookAtPoint = screen2Cartesian(Orbit.xFocus, Orbit.yFocus);
    Orbit.radius = camera.position.distanceTo(Orbit.lookAtPoint);
    States.orbiting = true; 
}

function orbitCamera () {
    if (Orbit.xMove !== 0 || Orbit.yMove !== 0) {
        var lookAt2Cam = new THREE.Vector3(); 
        var newPoint = new THREE.Vector3();
        
        // get look at point to camera position vector
        lookAt2Cam.setX (camera.position.x - Orbit.lookAtPoint.x);
        lookAt2Cam.setY (camera.position.y - Orbit.lookAtPoint.y);
        lookAt2Cam.setZ (camera.position.z - Orbit.lookAtPoint.z);
        
        Orbit.sphere.setFromVector3(lookAt2Cam); // turn into spherical coords
        // adjust angles depending on movement distance and sensitivity
        Orbit.sphere.phi -= 
                (Orbit.yMove/window.innerHeight)*2*PI*Orbit.ySensitivity;
        Orbit.sphere.theta -= 
                (Orbit.xMove/window.innerWidth)*2*PI*Orbit.xSensitivity;
        Orbit.sphere.makeSafe(); // restrict phi angle
        newPoint.setFromSpherical(Orbit.sphere); // convert back to cartesian     
        camera.position.addVectors(newPoint, Orbit.lookAtPoint);  // new cam pos
        
        /* DEBUG ONLY 
         * var arrowHelper = new THREE.ArrowHelper(newPoint, Orbit.lookAtPoint,
         *                                       Orbit.radius/2, 0xffffff);
         * renderer.render(scene, camera);
         * scene.add(arrowHelper); 
        */
    }
    camera.lookAt(Orbit.lookAtPoint);  
}

/*------------------------------ Cube Texture --------------------------------*/ 
var textureNames = ['bronze', 'wire', 'scratched', 'shapes', 'colour', 'water'];
for (var texture in textureNames){                          
    cube.userData.textures.push(new THREE.MeshBasicMaterial({
        map: textureLoader.load(textureNames[texture] + '.jpg')
    }));
}

function toggleTextures () {
    if (activeObject === cube){
        if (!States.textureRendering){ cube.material = cube.userData.textures; } 
        else { cube.material = cube.userData.material; } // switch to normal 
        States.faceRendering = false; // reset face render mode
        States.textureRendering = !States.textureRendering; // toggle flag    
    }
 };

/*------------------ Object Loading/Switch Active Object ---------------------*/
function loadBunny (filename) {  
    // set up material
    var material = new THREE.MeshPhongMaterial({color: Defaults.bunnyColor});
    var pointsMaterial = cube.userData.pointsMaterial.clone();
    pointsMaterial.size = Defaults.bunnyPointsSize; 
    var wireframeMaterial = cube.userData.wireframeMaterial.clone();
    var points, wireframe;

    objLoader.load(filename,
        // called on successful loading
        function(object) {   
            bunny = object;                                                  
            bunny.traverse( function (child) {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.material = material; // set phong material
                        points = new THREE.Points(
                            child.geometry, 
                            pointsMaterial
                        );
                        wireframe = new THREE.Mesh(
                            child.geometry, 
                            wireframeMaterial
                        );
                        // update bunny points and wireframe for render modes
                        bunny.userData.points = points;
                        bunny.userData.wireframe = wireframe;
                    }        
            });
            // scale bunny down so it fits within the cube
            bunny.scale.x = Defaults.bunnyScaling;
            bunny.scale.y = Defaults.bunnyScaling; 
            bunny.scale.z = Defaults.bunnyScaling;
            
            States.bunnyDisplayed = true;
            scene.add(bunny);
            toggleActiveObject();
            States.bunnyLoaded = true;
        }
    );
}
        
function toggleActiveObject () {
    if (activeObject === cube) {
        // reset states and turn cube faces off so bunny is visible
        if (!States.bunnyDisplayed) { scene.add(bunny); } 
        if (States.textureRendering) { toggleTextures(); }
        if (!States.edgeRendering) { toggleEdges(cube); }                               
        if (!States.faceRendering) { toggleFaces(cube); }     
        States.faceRendering = false;
        States.edgeRendering = false;  
        activeObject = bunny;
    } else {
        // switch to cube view
        if (!States.cubeDisplayed) { scene.add(cube); } 
        States.faceRendering = !States.faceRendering;
        activeObject = cube;
    }     
}

// removes/adds the non active object from/to the scene
function toggleNonActiveObjectDisplay () {            
    if (activeObject === cube && States.bunnyLoaded) {
        if (States.bunnyDisplayed) { scene.remove(bunny); } 
        else { scene.add(bunny); }
        States.bunnyDisplayed = !States.bunnyDisplayed;
    } else {
        if (States.bunnyLoaded) { 
            if (States.cubeDisplayed) { scene.remove(cube); }
            else { scene.add(cube); }
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
//  2 primitives per cube face; start indexes for each cube face logged here   
var FaceIndexes = {
    'r': 0,
    'l': 2,
    'u': 4,
    'd': 6,
    'f': 8,
    'b': 10
};
// individual cube data; positioning along w/ observable faces and there colours 
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
    // set individual cubes up using rubiks mapping data and add them to group
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

        newCube.castShadow = true;
        rubiksCube.add(newCube);
    }
    perfectRubiksCube = rubiksCube.clone();
    States.rubiksCubeGenerated = true;
}

/* params:
 * @param {Mesh} newCube - cube input
 * @param {Face3} newCubeFaces - faces to be coloured 
 * @param {Hex} newCubeColors - colour for each face 
 * @returns {undefined}
 */
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

/* params:
 * 
 * @param {char} side - cube face to rotate 
 * @param {char} rotationAxis - world axis to rotate each individual cube around
 * @param {int} axisVal - common position of all cubes on rotation side
 * @returns {undefined}
 */
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
            child.rotation[rotationAxis] += PI/2;
            if (child.rotation[rotationAxis] >= 2*PI) { 
                child.rotation[rotationAxis] = 0
            }
            var newCubeIndex = preRotationIndex[newPosMapping[pointer]];
            rubiksCube.children[newCubeIndex] = child;
            pointer++;
        }
    );
}

/*------------------------------ Event Handlers ------------------------------*/
function onKeyDown (e) {
    switch (e.which) {
        // pause object rotation on spacebar Keydown
        case 32:
            toggleRotation();
            break;
        // move camera left on left arrow Keydown
        case 37: translateCamera('left');
            break;
        // move camera up on up arrow Keydown
        case 38:
            translateCamera('up');
            break;
        // move camera right on right arrow Keydown
        case 39:                            
            translateCamera('right');
            break; 
        // move camera down on down arrow Keydown
        case 40:
            translateCamera('down');
            break;                                
        // move camera forwards on '+' Keydown; can also be invoked by using the mousewheel
        case 107:
            translateCamera('forwards');
            break;                                
        // move camera backwards '-' Keydown; can also be invoked by using the mousewheel
        case 109:
            translateCamera('backwards');
            break;
        // reset camera position on 'r' Keydown
        case 82:
            resetCamera();
            break;
        // toggle wall rendering on 'w' Keydown
        case 87: 
            toggleWalls();
            break;
        // toggle cube edge rendering (inc. primitive triangles) on 'e' Keydown
        case 69:
            toggleEdges(activeObject);
            break;
        // toggle cube faces on 'f' KeyDown
        case 70: 
            toggleFaces(activeObject);
            break;                      
        // toggle cube vertex rendering on 'v' Keydown
        case 86: 
            toggleVertices(activeObject);
            break;       
        // apply textures on 't' Keydown
        case 84: 
            toggleTextures();
            break; 
        // move cube for orbit demo purposes 
        case 77: 
            (cube.position.x === 3) ? cube.position.x = 0 : cube.position.x = 3;
            break;
        // load/switch active object on 's' Keydown
        case 83: 
            if (!States.bunnyLoaded) { loadBunny('bunny-5000.obj'); }
            else { toggleActiveObject(); }
            break;
        // toggle non-active object on 'x' Keydown
        case 88: 
            toggleNonActiveObjectDisplay();
            break;
        // toggle Rubik's cube mode on 'z' Keydown
        case 90: 
            toggleRubiksCube();
            break;
        // rotate 'front' side of rubiks cube anticlockwise on '1' keydown
        case 49:
        case 97:
            if (States.rubiksCubeMode) { rotateRubiks('f', 'z', 1); }
            break;
        // rotate 'down' side of rubiks cube anticlockwise on '2' keydown
        case 50:
        case 98:
            if (States.rubiksCubeMode) { rotateRubiks('d', 'y', -1); }
            break;
        // rotate 'left' side of rubiks cube anticlockwise on '4' keydown
        case 52:
        case 100:
            if (States.rubiksCubeMode) { rotateRubiks('l', 'x', -1); }
            break;
        // rotate 'right' of rubiks cube anticlockwise on '6' keydown
        case 54:
        case 102:
            if (States.rubiksCubeMode) { rotateRubiks('r', 'x', 1); }
            break;
        // rotate 'up' of rubiks cube anticlockwise on '8' keydown
        case 56:
        case 104:
            if (States.rubiksCubeMode) { rotateRubiks('u', 'y', 1); }
            break;
        // rotate 'back' side of rubiks cube anticlockwise on '9' keydown
        case 57:
        case 105:
            if (States.rubiksCubeMode) { rotateRubiks('b', 'z', -1); }
            break;
        default:
            break;                            
    }

    renderer.render(scene, camera); // render scene
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
        Orbit.xFocus = e.x; Orbit.yFocus = e.y; // log mouse coords 
        initOrbit();
    }
}

function onMouseMove (e) {
    if (States.orbiting){
        Orbit.xMove = e.movementX; Orbit.yMove = e.movementY;
        orbitCamera();
        renderer.render(scene, camera);
    }
}
// resets Orbit values 
function onMouseUp () {
    Orbit.started = false;  States.orbiting = false;
    Orbit.xStart = 0;   Orbit.yStart = 0;   Orbit.radius = 0;
    Orbit.xMove = 0;    Orbit.yMove = 0;
    Orbit.sphere = new THREE.Spherical();
    Orbit.lookAtPoint = new THREE.Vector3();
}  

// Handle resizing of the browser window.
function onResize () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
