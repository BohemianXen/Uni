"use strict"; // https://stackoverflow.com/q/1335851/72470

var camera, defaultCamera, scene, renderer;
var cube, cubeMaterial, bunny, bunnyMaterial, pointsMaterial;
var rubiksCube, perfectRubiksCube, rubiksFaces; 
var animationID; 
var activeObject;

var textureLoader = new THREE.TextureLoader();
var objLoader = new THREE.OBJLoader();
textureLoader.setPath("resources/");
objLoader.setPath("resources/");

var sqr = val => val*val;
var sum = (accumulator, val) => accumulator + val;

var Defaults = {
    cameraPos: [2, 1, 5],
    cameraLookAt: new THREE.Vector3(0.0031250000000000444, -0.22544951590594753, 0.9742498396986135),
    cubeColor: new THREE.Color(0x00fB8B),
    bunnyColor: new THREE.Color(0xf44298),
    bunnyScaling: 0.15,
    bunnyPointsSize: 0.01,
    rotationStep: 0.01, 
    cameraMovementDistance: 0.1,
};

// Object States                    
var States = {
    rotating: false,
    vertexRendering: false,
    edgeRendering: false, 
    faceRendering: false,
    textureRendering: false,
    orbiting: false,
    objectLoaded: false, 
    cubeDisplayed: false,
    objectLoadedDisplayed: false, 
    rubiksCubeMode: false, 
    rubiksCubeGenerated: false
};

var RubiksIndexes = {
    rightTop: null,
    rightMid: null,
    rightBot: null,
    leftTop: null,
    leftMid: null,
    leftBot: null,
    upTop: null,
    upMid: null,
    upBot: null,
    downTop: null,
    downMid: null,
    downBot: null,
    frontTop: null,
    frontMid: null,
    frontBot: null,
    backTop: null,
    backMid: null,
    backBot: null
};

init();
rotateX();
States.rotating = true;


// Scene Setup
function init () {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
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

    for (var i = 0; i < lights.length; i++) {
        scene.add(lights[i]);
    }

    // Event Listeners
    document.addEventListener("keydown", onKeyDown); //TODO: Pausing cube blocks other events until resumption
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
    var cubeGeometry = new THREE.BoxGeometry(1, 1, 1);         
    cubeMaterial = new THREE.MeshPhongMaterial({color: Defaults.cubeColor, vertexColors: THREE.VertexColors , flatShading: true});
    cube = new THREE.Mesh(cubeGeometry, cubeMaterial);

    scene.add(cube);
    activeObject = cube;
    States.cubeDisplayed = true;
    States.faceRendering = true;
    
    pointsMaterial = new THREE.PointsMaterial({color: 0xffff00, size: 0.075});
    var cubePoints = new THREE.Points(cubeGeometry, pointsMaterial);
    cube.points = cubePoints;
}

function axesSetup () {
    var xAxisGeometry = new THREE.Geometry();
    var yAxisGeometry = xAxisGeometry.clone();
    var zAxisGeometry = xAxisGeometry.clone();
    var xAxisMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });
    var yAxisMaterial = new THREE.LineBasicMaterial({ color: 0x00ff00 });
    var zAxisMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff });
    var axisLength = 4;

    xAxisGeometry.vertices.push(
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(axisLength, 0, 0)
    );

    yAxisGeometry.vertices.push(
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, axisLength, 0)
    );

    zAxisGeometry.vertices.push(
            new THREE.Vector3(0, 0, 0),
            new THREE.Vector3(0, 0, axisLength)
    );

    var xAxis = new THREE.Line(xAxisGeometry, xAxisMaterial);
    var yAxis = new THREE.Line(yAxisGeometry, yAxisMaterial);
    var zAxis = new THREE.Line(zAxisGeometry, zAxisMaterial);

    scene.add(xAxis, yAxis, zAxis);       
}


// Object Rotation
function rotateX () {
    var obj = activeObject;
    animationID = requestAnimationFrame(rotateX); 
    obj.rotation.x += Defaults.rotationStep;
    if (obj.rotation.x >= 2*Math.PI){
         obj.rotation.x = 0;
        cancelAnimationFrame(animationID); 
        rotateY();
    }
    renderer.render(scene, camera);
}

function rotateY () {
    var obj = activeObject;
    animationID = requestAnimationFrame(rotateY);
    obj.rotation.y += Defaults.rotationStep;
    if (obj.rotation.y >= 2*Math.PI){
        obj.rotation.y = 0;
        cancelAnimationFrame(animationID); 
        rotateZ();
    }
    renderer.render(scene, camera);
} 

function rotateZ () {
    var obj = activeObject;
    animationID = requestAnimationFrame(rotateZ); 
    obj.rotation.z += Defaults.rotationStep;
    if (obj.rotation.z >= 2*Math.PI){
        obj.rotation.z = 0;
        cancelAnimationFrame(animationID); 
        rotateX();
    }
    renderer.render(scene, camera);
}

function toggleRotation () {
    var obj = activeObject;
    if (States.rotating){
        cancelAnimationFrame(animationID); 
    } else {
        if (obj.rotation.y !== 0){
            obj.rotation.x = 0;
            obj.rotation.z = 0;
            rotateY();
        } else if (obj.rotation.z !== 0){
            obj.rotation.x = 0;
            obj.rotation.y = 0;
            rotateZ();
        } else { 
            obj.rotation.y = 0;
            obj.rotation.z = 0;
            rotateX();                                 
        }
    }
    States.rotating = !States.rotating; 
}


// Render modes 
// TODO: - Cannot enter edge mode from texture mode
//       - Cannot enter edge mode from off face mode
//       - Revert back to overlayed edge mode
function toggleEdges (obj) {
    if (!States.edgeRendering){ 
        obj.traverse(
            function (child) {
                if (child.material !== undefined && child.material.isMaterial) { 
                    child.material.wireframe = true; 
                }        
            });
    } else {
        obj.traverse(
            function (child) {
                if (child.material !== undefined && child.material.isMaterial) { 
                    child.material.wireframe = false; 
                }        
            });
    }  

    if (!States.textureRendering) {
        States.edgeRendering = !States.edgeRendering;
    }   
}

// TODO: Fix bugs -> T then F needs second F also a subsquent T does not bring the texture back
//                   F then T means T behaves like F
function toggleFaces (obj) {
    if (!States.faceRendering){
         obj.traverse(
            function (child) {
                if (child.material !== undefined && child.material.isMaterial) { 
                    child.material.opacity = 0.0;
                    child.material.transparent = true;
                }        
            });
    } else { 
        if (States.edgeRendering) { toggleEdges(obj); }
        obj.traverse(
            function (child) {
                if (child.material !== undefined && child.material.isMaterial) { 
                    child.material.opacity = 1.0;
                    child.material.transparent = false;
                }        
            });
    }    
    States.faceRendering = !States.faceRendering;
}    

// TODO  - Cannot enter vertices mode from off face mode
 //      - T -> F -> V -> F -> F now stuck with V=F
function toggleVertices (obj) {
if (!States.vertexRendering){
        obj.traverse(
           function (child) {
               if (child !== undefined && child.isMesh) { 
                  obj.add(obj.points);
               }        
        });
    } else {
        //TODO: Investigate why this throws when toggling bunny vertices off
        try { 
            obj.traverse(
            function (child) {
                if (child !== undefined && !child.isPoints && child.isMesh) { 
                   obj.remove(obj.points);
                }        
            });
        } catch (exception) {
            console.log(exception);
        }

    }     
    States.vertexRendering = !States.vertexRendering;   
}


// Camera Translation    
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


// Camera Orbit   
var Orbit = {
    started: false,
    xFocus: 0, 
    yFocus: 0,
    xMove: 0,
    yMove: 0,
    radius: -1,
    lookAtPoint: null
};

// TODO: - Fix rotation speed 
//       - Zooms out if you drag sideways a bunch
//       - Always looks at origin too much         
function orbitCamera () {
        
    var dotProduct = function (a, b) {
    var result = [a.x*b.x, a.y*b.y, a.z*b.z];
    return result.reduce(sum);
};

    var crossProduct = function (a, b) {
    return new THREE.Vector3(
            (a.y*b.z) - (a.z*b.y),
            (a.z*b.x) - (a.x*b.z), 
            (a.x*b.y) - (a.y*b.x)
        );
};

    var screen2Cartesian = function (xScreen, yScreen) {
    var result = [];
    result.push(-1 + (2*xScreen/window.innerWidth));
    result.push(-(-1 + (2*yScreen/window.innerHeight))); 
    var zSquared = sqr(result[0]) + sqr(result[1]);
    result.push(zSquared);
    if (Orbit.radius === -1){
        Orbit.radius = zSquared;
    }
    if (zSquared <= Orbit.radius){
        result[2] = Math.sqrt(zSquared);//Orbit.radius - zSquared);
    } else {
        result = result.map(x => x / zSquared);        
    }
    return new THREE.Vector3(result[0], result[1], result[2]);  
};  

    if (!Orbit.started){
        var xStart = Orbit.xFocus; 
        var yStart = Orbit.yFocus;
        Orbit.lookAtPoint = screen2Cartesian(xStart, yStart);
        Orbit.prevX = xStart; Orbit.prevY = yStart;
        Orbit.radius = Orbit.lookAtPoint.z;
        Orbit.started = true;                          
    } else {
         if (Orbit.xMove !== 0 || Orbit.yMove !== 0) {
            var op1 = screen2Cartesian(Orbit.xFocus, Orbit.yFocus);
            var op2 = screen2Cartesian(Orbit.xFocus + Orbit.xMove, Orbit.prevY + Orbit.yMove);
            var angle = Math.acos(Math.min(1, dotProduct(op1, op2)));
            var orthogonalVector = crossProduct(op1, op2);

            camera.translateX(op2.x - op1.x); // 4)*());
            camera.translateY(-(op2.y - op1.y));
            //camera.translateZ(op2.z - op1.z);
            //console.log(op1, op2);
            console.log(angle);
            //console.log(orthogonalVector);

            camera.rotateOnAxis(orthogonalVector, angle*2*Math.PI);
        }
    }
    
    camera.lookAt(Orbit.lookAtPoint);

};


// Cube Texture 
var textureNames = ['bronze', 'wire', 'scratched', 'shapes', 'colour', 'water'];
var textures = [];

for (var texture in textureNames){                          
    textures.push(new THREE.MeshBasicMaterial({
        map: textureLoader.load(textureNames[texture] + '.jpg')
    }));
}

function toggleTextures (obj) {
    if (obj === cube){
        if (!States.textureRendering){
            if (States.edgeRendering) { toggleEdges(obj); }
            cube.material = textures;
        } else {
            cube.material = cubeMaterial;
        }
        States.faceRendering = true;
        States.textureRendering = !States.textureRendering; 
        toggleFaces(obj);
    }
 };


// Object Loading/Switch Active Object

function loadObject (filename) {                            

    bunnyMaterial = new THREE.MeshPhongMaterial({color: Defaults.bunnyColor});
    var bunnyPointsMaterial = pointsMaterial.clone();
    bunnyPointsMaterial.size = Defaults.bunnyPointsSize;   

    objLoader.load(filename,

        function(object) {   
            bunny = object;                                                  
            bunny.traverse(function (child) {
                    if (child.isMesh) { 
                        child.material = bunnyMaterial;
                        var bunnyPoints = new THREE.Points(child.geometry, bunnyPointsMaterial);
                        bunny.points = bunnyPoints;
                    }        
            });

            bunny.scale.x = Defaults.bunnyScaling;
            bunny.scale.y = Defaults.bunnyScaling; 
            bunny.scale.z = Defaults.bunnyScaling;

            scene.add(bunny);

            States.objectLoadedDisplayed = true;
            toggleActiveObject();
            States.objectLoaded = true;
        }
    );
}
        
function toggleActiveObject () {

    if (activeObject === cube) {
        if (!States.objectLoaded) {
            if (States.textureRendering) { toggleTextures(cube); }
            if (!States.edgeRendering) { toggleEdges(cube); }                               
            if (States.vertexRendering) { toggleVertices(cube); }
        }

        activeObject = bunny;
        States.faceRendering = true;
        States.edgeRendering = false;

    } else {
        activeObject = cube;
    }     
}

function toggleNonActiveObjectDisplay () {            
    if (activeObject === cube && States.objectLoaded) {
        if (States.objectLoadedDisplayed) {
            scene.remove(bunny);
        } else {
            scene.add(bunny);
        }
        States.objectLoadedDisplayed = !States.objectLoadedDisplayed;
    } else {
        if (States.cubeDisplayed) {
            scene.remove(cube);
        } else {
            scene.add(cube);
        }
        States.cubeDisplayed = !States.cubeDisplayed;
    }
}


// Rubik's Cube Mode 

function toggleRubiksCube () {
    if (!States.rubiksCubeMode){
        //TODO: activeObject? disable other keys? stop rotation and other states
        /*if (States.rotating) { toggleRotation(); }
        if (States.cubeDisplayed) { scene.remove(cube); }
        if (States.objectLoadedDisplayed) { scene.remove(bunny); }
        
        States.cubeDisplayed = false;
        States.objectLoadedDisplayed = false;*/
        
        if (!States.rubiksCubeGenerated) { generateRubiksCube(); }
        scene.add(rubiksCube);
        console.log(rubiksCube);
    } else {
        /*if (!States.cubeDisplayed) { scene.add(cube); }
        if (!States.rotating) { toggleRotation(); }
        States.cubeDisplayed = true;
        //if (States.objectLoaded) { scene.add(bunny); }*/
        scene.remove(rubiksCube);
        //activeObject = cube;
    }
    
    States.rubiksCubeMode = !States.rubiksCubeMode;
    resetCamera();
}

function generateRubiksCube () {
    //              red      orange    white     yellow     green      blue
    var colors = [0xff0000, 0xffa500, 0xffffff, 0xffff00, 0x00ff00, 0x0000ff];
    var rubiksCubeGeometry = new THREE.BoxGeometry(3, 3, 3, 3, 3, 3);
    
    var colorFaces = function () {
        var innerCounter = 0; var outerCounter = 0;
        for (var face in rubiksCubeGeometry.faces) {
           rubiksCubeGeometry.faces[face].color.setHex(colors[outerCounter]);
           innerCounter++;
           if (innerCounter > 17) { 
               innerCounter = 0;
               outerCounter++;
           }
        }
    };
   
    colorFaces(); 
    var rubiksCubeMaterial = new THREE.MeshPhongMaterial({color: 0xffffff, vertexColors: THREE.FaceColors, flatShading: true}); 
    var cubeWireframe = new THREE.MeshBasicMaterial({color: 'black', wireframe: true});
    cubeWireframe = new THREE.Mesh(rubiksCubeGeometry, cubeWireframe);
    
    rubiksCube = new THREE.Mesh(rubiksCubeGeometry, rubiksCubeMaterial);
    rubiksCube.add(cubeWireframe);
    perfectRubiksCube = rubiksCube.clone();
    rubiksFaces = rubiksCube.geometry.faces;
 
    updateRubiksIndexes();
    States.rubiksCubeGenerated = true;
    //activeObject = rubiksCube;
}; 

 function updateRubiksIndexes () {
    var start = 0; var stop = 6;
    for (var row in RubiksIndexes) {
        if (RubiksIndexes.hasOwnProperty(row)) {
            RubiksIndexes[row] = rubiksFaces.slice(start, stop);
            start += 6;
            stop += 6;
        }
    }
}
    
function rotateRubiksBottom () {
    rubiksCube.geometry.colorsNeedUpdate = true;
}

function rotateRubiksLeft () {
    rubiksCube.geometry.colorsNeedUpdate = true; 
}

function rotateRubiksRight () {
    rubiksCube.geometry.colorsNeedUpdate = true;
}

function rotateRubiksTop () {
   var front = RubiksIndexes.frontTop;
   //var up = RubiksIndexes. // TODO: Extend for top side rotations fml 
   var left = RubiksIndexes.leftTop;
   var back = RubiksIndexes.backTop;
   var right = RubiksIndexes.rightTop;
   //var starts = []
   //for ()
   rubiksFaces[72].color.setHex(0x0000ff);
   //rubiksFaces.splice(72, right.length, ...right);
   //rubiksFaces.splice(0, right.length, ...back);
   //rubiksFaces.splice(90, right.length, ...left);
   //rubiksFaces.splice(18, right.length, ...front);
   rubiksCube.geometry.colorsNeedUpdate = true;
}


// Event Handlers

// Key press event handler
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
            toggleTextures(activeObject);
            break; 
        // Load/switch active object on 's' Keydown
        case 83: 
            if (!States.objectLoaded) { loadObject('bunny-5000.obj'); }
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
        // Rotate bottom of rubiks cube anticlockwise on '2' keydown
        case 50:
        case 98:
            if (States.rubiksCubeMode) { rotateRubiksBottom(); }
            break;
        // Rotate left side of rubiks cube anticlockwise on '4' keydown
        case 52:
        case 100:
            if (States.rubiksCubeMode) { rotateRubiksLeft(); }
            break;
        // Rotate bottom of rubiks cube anticlockwise on '6' keydown
        case 54:
        case 102:
            if (States.rubiksCubeMode) { rotateRubiksRight(); }
            break;
        // Rotate top of rubiks cube anticlockwise on '8' keydown
        case 56:
        case 104:
            if (States.rubiksCubeMode) { rotateRubiksTop(); }
            break;
        default:
            break;                            
    }

    renderer.render(scene, camera);
}

// Scroll wheel event handler 
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
        Orbit.xFocus = e.x; Orbit.yFocus = e.y;
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

function onMouseUp (e) {
    Orbit.started = false;
    Orbit.xFocus = 0;   Orbit.yFocus = 0; 
    Orbit.xMove = 0;    Orbit.yMove = 0;
    Orbit.radius = -1;  Orbit.lookAtPoint = null;

    States.orbiting = false;
}  

// Handle resizing of the browser window.
function onResize () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
