function mainfig (h,eventdata)
global new_width new_height block_size search_limit search_step...
    check_fframe check_sframe check_newframe check_vectors...
    width_help height_help block_help limit_help step_help file_name 
close(figure(1)) % to ensure only one main window is open at a time
figure('menubar','none','position',[200,200,500,500],'name',...
    'Motion Estimation','color',[0.1,0.4,0.6],'resize','off');
% creates title and push button that is used to load up images and also...
% displays name of current file loaded
uicontrol('style','text','string','Motion Estimation','position',...
    [20,20,455,480],'backgroundcolor',[0.1,0.5,0.6],'fontsize',20);
frame_load=uicontrol('style','pushbutton','string','Load Frames','position',...
    [180,430,120,25],'fontsize',14,'callback',@image_load);
file_name=uicontrol('style','text','string','','position',[205,410,65,15],...
    'fontsize',8,'fontangle','italic','callback',@image_load,'backgroundcolor',[0.1,0.5,0.6]);
% tells user what they need to enter in to the adjacent fields
uicontrol('style','text','string','Enter new width  ','position',...
    [40,320,200,60],'fontsize',12,'backgroundcolor',[0.1,0.5,0.6])
uicontrol('style','text','string','Enter new height ','position',...
    [40,260,200,60],'fontsize',12,'backgroundcolor',[0.1,0.5,0.6])
uicontrol('style','text','string','Enter block size ','position',...
    [40,200,200,60],'fontsize',12,'backgroundcolor',[0.1,0.5,0.6])
uicontrol('style','text','string','Enter search limit ','position',...
    [40,140,200,60],'fontsize',12,'backgroundcolor',[0.1,0.5,0.6])
uicontrol('style','text','string','Enter search step','position',...
    [40,80,200,60],'fontsize',12,'backgroundcolor',[0.1,0.5,0.6])
uicontrol('style','text','string','Created by 09795','position',...
    [375,20,100,20],'backgroundcolor',[0.1,0.5,0.6])
new_width=uicontrol('style','edit','string','0','position',[260,355,200,30]);
new_height=uicontrol('style','edit','string','0','position',[260,295,200,30]);
block_size=uicontrol('style','edit','string','0','position',[260,235,200,30]);
search_limit=uicontrol('style','edit','string','0','position',[260,175,200,30]);
search_step=uicontrol('style','edit','string','0','position',[260,115,200,30]);
% tick boxes that essentially filter displayed images in accorcance with
% the user's preference---Defaults to images requested in assignment brief
uicontrol('style','text','string','What do you wish to display?','position',...
    [20,30,120,40],'fontsize',10,'backgroundcolor',[0.1,0.5,0.6])
check_fframe=uicontrol('style','checkbox','string','First Frame','position',...
    [140,95,100,20],'Callback','','Value',1,'backgroundcolor',[0.1,0.5,0.6]);
check_sframe=uicontrol('style','checkbox','string','Second Frame','position',...
    [140,70,120,20],'Callback','','Value',1,'backgroundcolor',[0.1,0.5,0.6]);
check_newframe=uicontrol('style','checkbox','string','Reconstruction',...
    'position',[140,45,100,20],'Callback','','Value',1,'backgroundcolor',[0.1,0.5,0.6]);
check_vectors=uicontrol('style','checkbox','string','Vectors','position',...
    [140,20,100,20],'Callback','','backgroundcolor',[0.1,0.5,0.6]);
% this button fills in all fields with the recommended values
default=uicontrol('style','pushbutton','string','Use Recommended Settings',...
    'position',[280,400,150,20],'callback',@default_Callback);
% main run button
run=uicontrol('style','pushbutton','string','Run!','position',[315,60,80,30],...
    'CallBack',@run_Callback);
% help togglebuttons that display pop up help descriptions when toggled
width_help=uicontrol('style','togglebutton','string','?','position',...
    [50,370,20,20],'callback',@width_Callback,'backgroundcolor',[0.1,0.4,0.7]);
height_help=uicontrol('style','togglebutton','string','?','position',...
    [50,310,20,20],'callback',@height_Callback,'backgroundcolor',[0.1,0.4,0.7]);
block_help=uicontrol('style','togglebutton','string','?','position',...
    [50,250,20,20],'callback',@block_Callback,'backgroundcolor',[0.1,0.4,0.7]);
limit_help=uicontrol('style','togglebutton','string','?','position',...
    [50,190,20,20],'callback',@limit_Callback,'backgroundcolor',[0.1,0.4,0.7]);
step_help=uicontrol('style','togglebutton','string','?','position',...
    [50,130,20,20],'callback',@step_Callback,'backgroundcolor',[0.1,0.4,0.7]);
return

% default values callback
function default_Callback (h,eventdata)
global new_width new_height block_size search_limit search_step
set(new_width,'string','240')
set(new_height,'string','200')
set(block_size,'string','20')
set(search_limit,'string','20')
set(search_step,'string','2')
return

function run_Callback(h,eventdata)
global new_width new_height block_size search_limit search_step ...
    check_fframe check_sframe check_newframe check_vectors F1 F2

close(figure(2)) % fixes bug where previous instance would be subplotted
% corrects and rounds negative & non-interger values
wdth=sqrt((fix(str2double(get(new_width,'string'))))^2);
hght=sqrt((fix(str2double(get(new_height,'string'))))^2);
block=sqrt((fix(str2double(get(block_size,'string'))))^2);
limit=sqrt((fix(str2double(get(search_limit,'string'))))^2);
step=sqrt((fix(str2double(get(search_step,'string'))))^2);
% ensures no strings are in the edit text boxes and tells user where too
% also prevents empty fields that would stop p. function
if isempty(wdth)==1
    errordlg('Please enter numbers only','Error In Width','on')
elseif isempty(hght)==1
    errordlg('Please enter numbers only','Error In Height','on')
elseif isempty(block)==1
    errordlg('Please enter numbers only','Error In Block','on')
elseif isempty(limit)==1
    errordlg('Please enter numbers only','Error In Limit','on')
elseif isempty(step)==1
    errordlg('Please enter numbers only','Error In Step','on')
else
end
% using the given p. function
[f1,f2,xx,yy,u,v,F2_Reconstructed]=motion_detection_function(F1,F2,wdth,...
    hght,block,limit,step);
% sees which check boxes are filled and decides which images to display...
% as well as whether the vectors are required on principle image
fframe=get(check_fframe,'Value');
sframe=get(check_sframe,'Value');
newframe=get(check_newframe,'Value');
vectors=get(check_vectors,'Value');
figure(2) %creates the 'images' figure
if fframe==1&&sframe==0&&newframe==0&&vectors==0
    imshow(uint8(f1))
    title('First Frame')
elseif fframe==0&&sframe==1&&newframe==0&&vectors==0
    imshow(uint8(f2))
    title('Second Frame')
elseif fframe==0&&sframe==0&&newframe==1&&vectors==0
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif  fframe==1&&sframe==1&&newframe==0&&vectors==0
    subplot(1,2,1)
    imshow(uint8(f1))
    title('First Frame')
    subplot(1,2,2)
    imshow(uint8(f2))
    title('Second Frame')
elseif fframe==1&&sframe==0&&newframe==1&&vectors==0
    subplot(1,2,1)
    imshow(uint8(f1))
    title('First Frame')
    subplot(1,2,2)
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif fframe==1&&sframe==0&&newframe==0&&vectors==1
    imshow(uint8(f1))
    title('First Frame W/ Vectors')
    hold on
    % hold on so quiver is cast on first image --- multiplied vectors by -1 as
    % they seemed to be pointing towards the best matching block as opposed
    % to pointing from it (in the direction of motion)
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
elseif fframe==0&&sframe==1&&newframe==1&&vectors==0
    subplot(1,2,1)
    imshow(uint8(f2))
    title('Second Frame')
    subplot(1,2,2)
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif fframe==1&&sframe==1&&newframe==1&&vectors==0
    subplot(1,3,1)
    imshow(uint8(f1))
    title('First Frame')
    subplot(1,3,2)
    imshow(uint8(f2))
    title('Second Frame')
    subplot(1,3,3)
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif fframe==1&&sframe==1&&newframe==0&&vectors==1
    subplot(1,2,1)
    imshow(uint8(f1))
    title('First Frame W/ Vectors')
    hold on
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
    hold off
    subplot(1,2,2)
    imshow(uint8(f2))
    title('Second Frame')
elseif fframe==1&&sframe==0&&newframe==1&&vectors==1
    subplot(1,2,1)
    imshow(uint8(f1))
    title('First Frame W/ Vectors')
    hold on
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
    hold off
    subplot(1,2,2)
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif fframe==0&&sframe==1&&newframe==1&&vectors==0
    subplot(1,2,1)
    imshow(uint8(f2))
    title('Second Frame')
    subplot(1,2,2)
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif fframe==1&&sframe==1&&newframe==1&&vectors==1
    subplot(1,3,1)
    imshow(uint8(f1))
    title('First Frame W/ Vectors')
    hold on
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
    hold off
    subplot(1,3,2)
    imshow(uint8(f2))
    title('Second Frame')
    subplot(1,3,3)
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif fframe==0&&sframe==1&&newframe==0&&vectors==1
    imshow(uint8(f2))
    title('Second Frame W/ Vectors')
    hold on
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
elseif fframe==0&&sframe==1&&newframe==1&&vectors==1
    subplot(1,2,1)
    imshow(uint8(f2))
    title('Second Frame W/ Vectors')
    hold on
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
    hold off
    subplot(1,2,2)
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
elseif fframe==0&&sframe==0&&newframe==0&&vectors==1
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
    title('Vectors Plot')
elseif fframe==0&&sframe==0&&newframe==1&&vectors==1
    imshow(uint8(F2_Reconstructed))
    title('Reconstruction')
    hold on
    quiver(xx,yy,(-1.*u),(-1.*v),0,'r','linewidth',step)
else
    close(2)
    warndlg('Did you forget to display images?','No Display Warning')
end
return

% loads the user selected file and globalises the two original frames
function image_load(h,eventdata)
global F1 F2 file_name file
[file,frames_path]=uigetfile('*.mat','Select the set of images');
frames=[frames_path,file];
temp=open(frames);
F1=temp.F1;
F2=temp.F2;
set(file_name,'string',file)
return

% displays the appropriate help boxes depending on what togglebutton is
% pressed --- resets toggle button as having to press twice if you need to
% use it again is annoying. Guess I could have just used a button really
function width_Callback(h,eventdata)
global width_help
if get(width_help,'Value')==1
    helpdlg('sets new image width in pixels','Width Help')
    set(width_help,'Value',0);
else
end
return

function height_Callback(h,eventdata)
global height_help
if get(height_help,'Value')==1
    helpdlg('sets new image height in pixels','Height Help')
    set(height_help,'Value',0);
else
end
return

function block_Callback(h,eventdata)
global block_help
if get(block_help,'Value')==1
    helpdlg('sets the block by block search size in squares of pixels',...
        'Block Help')
    set(block_help,'Value',0);
else
end
return

function limit_Callback(h,eventdata)
global limit_help
if get(limit_help,'Value')==1
    helpdlg(...
        'max displacement of search allowed relative to reference block in second frame',...
        'Limit Help')
    set(limit_help,'Value',0);
else
end
return

function step_Callback(h,eventdata)
global step_help
if get(step_help,'Value')==1
    helpdlg('resolution of motion vectors in pixels','Step Help')
    set(step_help,'Value',0)
else
end
return

% 09795






