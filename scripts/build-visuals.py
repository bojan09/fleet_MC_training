"""Generate original conceptual SVGs from the manual's teaching points.
Run from the repository root. PDF extracts are retained separately, unchanged.
"""
from pathlib import Path
import json, html
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/content.json').read_text())
# Explicit headings and visual associations keep each graphic tied to its explanation.
specs=[
[
('Cab / sleeper','truck','Driver controls|Rest compartment|Vehicle configuration'),
('Steer axle','axles','Front axle|Steering function|Wheel ends & brakes'),
('Drive axles','drive','Driveshaft|Differential|Powered wheels'),
('Fifth wheel','coupling','Tractor coupling plate|Trailer kingpin|Engagement check'),
('Fuel tanks / DEF tank','def','Diesel fuel|Separate DEF tank|Different fill points'),
('Unit number / VIN','document','Fleet unit ID|Manufacturer VIN|Match the exact vehicle')],
[
('Engine oil','engine','Oil sump|Moving engine parts|Lubrication & cooling'),
('Cooling system','cooling','Radiator & fan|Coolant circulation|Engine & hoses'),
('Turbocharger','turbo','Exhaust turbine|Common shaft|Intake compressor'),
('Belts / tensioners','belt','Accessory pulleys|Drive belt|Belt tensioner'),
('Alternator / batteries','battery','Alternator charges|Battery stores|Electrical consumers'),
('Transmission / driveshaft','drive','Transmission|Driveshaft|Drive axle')],
[
('DPF','exhaust','Exhaust enters|Soot is trapped|Regeneration is OEM-specific'),
('DEF / SCR','scr','DEF dosing|SCR catalyst|NOx reduction'),
('EGR','egr','Exhaust gas|Controlled recirculation|Intake mixture'),
('ECM','ecm','Sensor inputs|Control module|Commands & fault reports'),
('Derate','warning','Fault condition|Possible power limit|Record exact messages'),
('Never guess a repair','workflow','Warning or symptom|Qualified diagnosis|Confirmed repair scope')],
[
('Compressor / governor','compressor','Compressor builds air|Governor regulates|Vehicle-specific limits'),
('Air dryer / reservoirs','air','Air supply|Dryer removes moisture|Reservoir stores air'),
('Foot valve / relay valves','brake','Driver brake demand|Control & relay valves|Air to brake chambers'),
('Brake chambers','brake','Air pressure|Diaphragm & pushrod|Mechanical brake force'),
('Spring parking brakes','springbrake','Spring stores energy|Air releases parking brake|Trained service only'),
('ABS','wheel','Wheel-speed sensors|ABS control|Wheel-lock management'),
('Low-air warning','warning','Low air report|Safe-stop guidance|Qualified brake service')],
[
('Air suspension','suspension','Air springs|Height control|Shocks & linkages'),
('Leaf springs','leaf','Spring pack|Hangers|Axle support'),
('Steer / drive / trailer axle','axles','Steer: steering|Drive: powered|Trailer: supports trailer'),
('Tandem axles','tandem','Two adjacent axles|Weight distribution|Function varies'),
('Lift axle','lift','Auxiliary axle|Raised or lowered|Load & rules determine use'),
('Differential','differential','Input torque|Differential gears|Axle shafts'),
('Wheel end','wheel','Hub & bearings|Seal & lubricant|Heat or leak report')],
[
('Steer tires','steertire','Front steering axle|Often rib-oriented|Application approval'),
('Drive tires','drivetire','Powered axles|Often traction tread|Duty & season'),
('Trailer tires','trailertire','Trailer axles|Load & inflation|Tread & sidewall checks'),
('Pressure','gauge','Measure pressure|Use load guidance|Do not judge by appearance'),
('Load rating','load','Actual axle load|Tire capacity|Wheel capacity'),
('Dual tires','dual','Paired tires|Matched dimensions|Proper inflation')],
[
('Center wear','wearcenter','Center tread wear|Pressure history|Qualified assessment'),
('Both shoulders','wearshoulder','Both tread edges|Inflation & load clues|Not a final diagnosis'),
('One-sided wear','wearside','One tread edge|Alignment or axle clues|Inspect related systems'),
('Cupping / scalloping','wearcup','Repeated low spots|Wheel-end & suspension|Professional assessment'),
('Flat spots','wearflat','Localized tread flattening|Operating history|Qualified inspection'),
('Bulge / exposed cords','bulge','Sidewall deformation|Exposed reinforcement|Qualified tire service'),
('Coordinator action','document','Position & tire size|Photos & measurements|Vendor findings')],
[
('Dry van','van','Enclosed freight body|Doors & structure|Running gear'),
('Reefer','reefer','Insulated body|Refrigeration unit|Mechanical + cooling service'),
('Flatbed / step deck','flatbed','Open deck|Structure|Securement hardware'),
('Tanker','tanker','Specialized vessel|Load compatibility|Specialist service'),
('Container chassis','chassis','Container frame|Twist locks|Running gear'),
('53-foot trailer','dimension','Length measurement|Not a trailer type|Confirm configuration')],
[
('Fifth wheel / kingpin','coupling','Tractor fifth wheel|Trailer kingpin|Qualified engagement check'),
('Glad hands','hoses','Service air line|Emergency / supply line|Correct coupling'),
('Electrical pigtail','connector','Tractor electrical supply|Trailer connector|Lighting & circuits'),
('Landing gear','landing','Trailer support legs|Feet & bracing|Uncoupled support'),
('Trailer tandem slider','slider','Sliding axle assembly|Positioning rails|Secured locking mechanism'),
('Coordinator action','workflow','Report & photos|On-site qualified inspection|Document findings')],
[
('Refrigeration unit','reefer','Refrigeration equipment|Insulated cargo space|Required setpoint'),
('Setpoint vs actual','temperature','Requested setpoint|Displayed actual reading|Record separately'),
('Fuel / electrical','battery','Reefer fuel|Electrical supply|Running mode & alarms'),
('Continuous / start-stop','cycle','Continuous operation|Cycling operation|Cargo / shipper instructions'),
('Alarm code','ecm','Exact alarm code|Reefer make & model|Specialist diagnosis'),
('Cargo risk','workflow','Temperature excursion|Notify operations|Authorized cargo response')],
[
('DOT / FMCSA','document','US DOT|FMCSA|Applicable safety framework'),
('Pre-trip inspection','inspection','Before operation|Safe operating condition|Driver responsibility'),
('DVIR','document','Defect report|Repair follow-up|Operation-specific rules'),
('Periodic inspection','calendar','Qualifying inspection|Applicable periodic interval|Retain required evidence'),
('Roadside inspection','inspection','Driver|Vehicle|Required paperwork'),
('OOS','stop','Out of service|Correct relevant defects|Required documented clearance'),
('Documentation','document','Inspection records|Repair records|Applicable rules & fleet policy')],
[
('Brakes','brake','Hoses & air pressure|Leaks & condition|Qualified brake inspection'),
('Tires / wheels','wheel','Tires & sidewalls|Wheel fasteners|Wheel-end leaks'),
('Steering / suspension','suspension','Steering linkage|Suspension components|Damage or excessive wear'),
('Lighting','lights','Required lamps|Reflectors & markings|Electrical connections'),
('Coupling','coupling','Fifth wheel & kingpin|Mountings|Connection security'),
('Leaks / structural','chassis','Fluid leak report|Frame condition|Qualified assessment'),
('Escalation','stop','Active OOS condition|Repairs & evidence|Documented clearance')],
[
('Check Engine / MIL','warning','Engine / emissions report|Exact active code|Vehicle behavior'),
('Stop Engine / red warning','stop','Red warning report|OEM safe-stop guidance|Qualified assessment'),
('Low oil pressure','engine','Oil-pressure warning|Engine protection risk|Assessment before operation'),
('High coolant temperature','cooling','Temperature warning|Overheating risk|Safe stop & OEM guidance'),
('ABS','wheel','ABS fault indication|Record lamp status|Qualified evaluation'),
('DPF / DEF','scr','Exact dashboard message|Fluid level|Derate status'),
('DTC / SPN / FMI','ecm','Exact fault code|Vehicle identification|OEM diagnostic information')],
[
('Location','location','Highway & mile marker|Travel direction|Safe location / GPS pin'),
('Identification','document','Driver & callback|Tractor / trailer units|VIN if needed'),
('Symptoms','warning','What happened & when|Messages & codes|Sounds or leaks'),
('Safety','stop','Safe location?|Traffic / smoke / injury?|Active OOS status?'),
('Mobility','truck','Can it move safely?|Temperature-sensitive load?|Qualified assessment'),
('Evidence','camera','Relevant photos|Dashboard messages|Position & service history'),
('Avoid','stop','No warning bypass|No unsafe roadside repair|Qualified service')],
[
('1. Triage','stop','Protect driver|Classify urgency|Emergency help if needed'),
('2. Vendor selection','truck','Exact equipment|Appropriate capability|Mobile / tow / shop'),
('3. Confirm ETA','clock','Dispatch ETA|Driver update|Operations update'),
('4. Approve scope','document','Diagnosis|Labor & parts estimate|Fleet authorization'),
('5. Monitor','clock','Arrival & diagnosis|Parts / repair progress|Updated ETR'),
('6. Verify','inspection','Technician findings|Tests & invoice|Required clearance'),
('7. Close','document','Work order|Downtime & cost|Dispatch availability')],
[
('PM A/B/C','calendar','Fleet-defined tiers|OEM schedule|Not universal DOT levels'),
('Trigger','gauge','Miles / engine hours|Calendar time|Duty cycle / condition'),
('WO / RO','document','Unit & complaint|Diagnosis & work|Parts / dates / approval'),
('PM forecast','calendar','Current reading|Expected utilization|Schedule shop time'),
('Backlog','workflow','Safety-critical defects|Prioritized work|Convenience repairs'),
('Return to service','inspection','Work & evidence|Driver notification|Dispatch release'),
('Record quality','document','Who approved?|What & when?|Who performed work?')],
[
('Vendor evaluation','truck','Capability & location|Response & quality|Warranty / certifications'),
('Estimate review','cost','Labor & diagnosis|Parts & supplies|Taxes / towing / total'),
('Warranty','document','OEM coverage|Part coverage|Prior repair warranty'),
('Downtime','clock','Unavailable time|Waiting / parts / repair|Released time'),
('PM compliance','chart','Completed scheduled PMs|PMs due in same window|Completed ÷ due'),
('Road call rate','chart','Roadside events|Defined exposure period|Document denominator'),
('Cost per mile','cost','Maintenance cost|Miles in same period|Cost ÷ miles')],
[
('Scenario A: Low air warning','air','Safe stop & location|Qualified brake service|No continued driving'),
('Scenario B: Reefer high temp','temperature','Setpoint / actual / alarms|Cargo risk & location|Reefer specialist'),
('Scenario C: PM overdue','calendar','Fleet / OEM interval|Last service & planned miles|Schedule approved service'),
('Scenario D: Tire sidewall bulge','bulge','Position / photo / size|Qualified tire service|Assess OOS implications'),
('Scenario E: OOS at roadside','stop','Inspection report|Required repairs|Evidence before release')]
]
# Original schematic drawings; simplified shapes illustrate concepts, not service anatomy.
ink='#23473f';green='#759a65';amber='#d49a45';blue='#668cac';red='#bc6951'
def line(x1,y1,x2,y2,c=ink,w=3):return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
def box(x,y,w,h,fill='#e3eadd',rx=7):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{ink}" stroke-width="2.5"/>'
def circle(x,y,r,fill='#e3eadd'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{ink}" stroke-width="2.5"/>'
def text(x,y,s,size=12,c=ink):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{c}" text-anchor="middle">{html.escape(s)}</text>'
def wheel(x,y,r=18):return circle(x,y,r,'#314b45')+circle(x,y,r*.48,'#cbd7d0')+circle(x,y,3,'#607a70')
def engine():return box(48,45,122,77,'#c8d9bd')+box(65,30,90,19,'#e8edde',3)+''.join(box(59+i*26,57,17,43,'#f1f3ea',3) for i in range(4))+box(57,125,95,19,'#93ae84')+line(70,122,70,141,amber,5)+circle(180,87,22)+circle(180,87,12)+line(170,60,204,60)+line(204,60,204,42)+text(110,163,'Simplified engine system',11)
def truck(axles=False):
 s=box(98,40,137,69,'#e9ede5',2)+f'<path d="M16 113V77L37 58H77L91 91V113Z" fill="#afc5a0" stroke="{ink}" stroke-width="3"/>'+f'<path d="M38 65H68L80 86H29Z" fill="#72968d"/>'+line(13,114,238,114,ink,5)+''.join(wheel(x,123,16) for x in [45,99,131,198,226])+box(61,99,25,11,'#c5d1c5',3)
 if axles:s+=''.join(line(x,147,x,162,amber,2) for x in [45,115,211])+text(45,177,'STEER',9)+text(115,177,'DRIVE',9)+text(211,177,'TRAILER',9)
 return s

def tire(kind='steertire'):
 s=box(68,18,112,150,'#40564f',25)+box(76,22,96,143,'#73877b',19)
 for x in range(87,171,18):s+=line(x,28,x,156,'#d0d9cf',4)
 if kind in ['drivetire','trailertire','wearcup','wearflat']:
  for y in range(41,151,23):s+=line(79,y,169,y+8,'#d0d9cf',3)
 if kind=='wearcenter':s+=box(110,26,25,133,'#d49a45',8)
 if kind=='wearshoulder':s+=box(76,30,14,124,'#d49a45',6)+box(158,30,14,124,'#d49a45',6)
 if kind=='wearside':s+=box(76,30,21,124,'#d49a45',6)
 if kind=='wearcup':s+=''.join(circle(98,y,11,'#d49a45') for y in [49,88,127])
 if kind=='wearflat':s+=box(80,88,88,26,'#d49a45',2)
 return s

def scene(k):
 if k in ['truck','axles','tandem','lift','lights','dimension']: 
  s=truck(k=='axles')
  if k=='lights':s+=''.join(circle(x,y,5,'#e1b35b') for x,y in [(20,99),(83,96),(232,100),(102,45),(233,45)])
  if k=='lift':s+=line(131,153,131,139,amber,4)+line(126,144,131,139,amber)+line(136,144,131,139,amber)+text(130,175,'Auxiliary axle position varies',10)
  if k=='tandem':s+=box(80,145,70,22,'#e5edda',4)+text(115,160,'TANDEM',10)
  if k=='dimension':s+=line(98,153,235,153,amber,2)+line(98,147,98,159,amber,2)+line(235,147,235,159,amber,2)+text(167,173,'Confirm actual length',11)
  return s
 if k=='engine':return engine()
 if k=='cooling':return box(24,32,66,110,'#d4e2e4')+''.join(line(x,40,x,133,blue,2) for x in range(32,84,8))+circle(56,87,23,'#ecf1ec')+''.join(line(56,87,x,y,blue,5) for x,y in [(56,68),(74,95),(38,95)])+box(150,50,75,78,'#c8d9bd')+f'<path d="M90 47H185V50 M151 114H110V126H90" fill="none" stroke="{red}" stroke-width="7"/>'+text(57,161,'Radiator + fan',11)+text(186,161,'Engine',11)
 if k=='turbo':return circle(72,89,45,'#c9d8dd')+circle(177,89,45,'#d4dcbf')+line(72,89,177,89,ink,6)+''.join(line(cx,89,cx+dx,89+dy,ink,3) for cx in [72,177] for dx,dy in [(0,-29),(25,15),(-25,15)])+line(28,45,28,20,red,10)+line(220,132,220,156,blue,10)+text(70,157,'Turbine',12)+text(178,157,'Compressor',12)
 if k=='belt':return ''.join(circle(x,y,r) + circle(x,y,6) for x,y,r in [(50,58,26),(188,55,25),(116,139,29),(123,70,15)])+f'<path d="M31 41Q50 18 72 39L200 33Q228 58 206 76L137 160Q113 183 93 155L30 77Q17 57 31 41Z" fill="none" stroke="{amber}" stroke-width="7"/>'
 if k=='battery':return box(124,58,98,83,'#d0dfc4')+box(137,46,18,12,'#8eaa80',2)+box(191,46,18,12,'#8eaa80',2)+text(147,89,'+',25)+text(200,89,'−',25)+circle(48,100,28)+circle(48,100,17)+line(48,72,48,52,amber,5)+line(48,52,146,52,amber,5)+line(48,128,48,155,blue,4)+line(48,155,201,155,blue,4)+line(201,155,201,141,blue,4)+text(48,170,'Charging',10)+text(173,116,'BATTERY',11)
 if k in ['drive','differential']:return box(12,67,55,57,'#bacfba')+line(67,95,133,95,ink,10)+circle(157,95,27)+line(157,95,210,39,ink,10)+line(157,95,210,151,ink,10)+wheel(216,36,22)+wheel(216,153,22)+text(42,145,'Transmission',10)+text(126,65,'Driveshaft',10)+text(154,134,'Differential',10)
 if k in ['def','exhaust','scr','egr']:
  s=box(17,66,50,65,'#cbd5cb')+box(101,66,54,65,'#c5d7c8')+box(190,66,50,65,'#d3dfc4')+line(0,98,17,98,ink,7)+line(67,98,101,98,ink,7)+line(155,98,190,98,ink,7)+line(240,98,250,98,ink,7)
  if k=='def':return box(25,48,85,102,'#c9d1c6')+box(143,70,77,80,'#d7e4e8')+box(38,34,25,14,'#677e65',3)+box(158,54,25,16,blue,3)+text(67,103,'DIESEL',13)+text(181,118,'DEF',16)+text(124,174,'Separate tanks · separate fluids',11)
  if k=='egr':return engine()+f'<path d="M195 43Q225 5 125 12H58V30" fill="none" stroke="{amber}" stroke-width="6"/>'+text(132,26,'Recirculated exhaust',10)
  s+=text(42,154,'DPF',11)+text(128,154,'Dosing',11)+text(215,154,'SCR',11)+''.join(line(x,72,x,124,green,2) for x in [28,35,42,49,56])+box(110,28,32,23,'#d1e6ed',3)+line(126,51,126,66,blue,4)
  return s
 if k in ['compressor','air']:return circle(40,95,25)+box(25,52,30,29)+line(55,65,99,65,blue,5)+box(99,39,36,65,'#cbdcc5')+line(135,65,177,65,blue,5)+box(158,103,78,43,'#e1e8dc',21)+line(177,65,197,65,blue,5)+line(197,65,197,103,blue,5)+text(40,146,'Compressor',10)+text(117,124,'Dryer',10)+text(197,169,'Reservoir',10)
 if k in ['brake','springbrake']:return box(15,39,62,106,'#c1d5bd',23)+line(0,65,15,65,blue,7)+line(77,92,135,92,ink,9)+line(135,92,154,122,ink,7)+circle(193,99,46,'#d8dfd4')+circle(193,99,30,'#edf0e9')+line(154,122,174,122,amber,6)+text(47,165,'Chamber',11)+text(189,165,'Foundation brake',11)+(f'<path d="M23 100L33 79L43 100L53 79L63 100" fill="none" stroke="{amber}" stroke-width="4"/>' if k=='springbrake' else line(38,56,38,128,ink,3))
 if k in ['suspension','leaf']:return line(20,30,231,30,ink,10)+line(25,136,225,136,ink,10)+wheel(44,143,25)+wheel(210,143,25)+(box(61,49,52,68,'#adc59d',19)+''.join(line(64,y,109,y,ink,2) for y in [64,81,98])+line(167,39,145,122,amber,10)+line(162,65,154,98,ink,16) if k=='suspension' else ''.join(f'<path d="M55 {60+i*8}Q123 {132+i*5} 197 {60+i*8}" fill="none" stroke="{green}" stroke-width="6"/>' for i in range(4)))
 if k in ['steertire','drivetire','trailertire','wearcenter','wearshoulder','wearside','wearcup','wearflat']:return tire(k)
 if k in ['wheel','dual','bulge','load']:return wheel(102,94,62)+circle(102,94,37,'#b0c4ac')+''.join(circle(102+dx,94+dy,4,'#405d50') for dx,dy in [(0,-24),(21,-12),(21,12),(0,24),(-21,12),(-21,-12)])+(wheel(156,94,58) if k=='dual' else '')+(f'<path d="M52 51Q4 51 40 96" fill="#dba87e" stroke="{red}" stroke-width="3"/>'+line(26,51,6,24,red)+text(61,178,'Sidewall damage example',11) if k=='bulge' else '')+(line(102,0,102,30,amber,7)+line(86,19,102,33,amber,4)+line(118,19,102,33,amber,4)+text(105,175,'Load and capacity must match',11) if k=='load' else '')
 if k in ['van','reefer','flatbed','tanker','chassis','landing','slider']:
  s=line(16,129,234,129,ink,6)+wheel(177,143,20)+wheel(221,143,20)+line(45,130,45,158,ink,6)+line(36,159,55,159,ink,5)
  if k in ['van','reefer','landing','slider']:s+=box(16,35,219,87,'#e2e8dd',3)+''.join(line(x,42,x,116,'#bbccbb',1) for x in range(30,230,14))
  if k=='reefer':s+=box(5,45,28,65,'#a5bdac',3)+''.join(line(11,y,27,y,ink,2) for y in range(56,101,9))
  if k=='flatbed':s+=box(16,115,219,13,'#c7b58a',2)+box(65,71,66,44,'#d5dcca',1)+line(75,72,75,114,amber,4)+line(121,72,121,114,amber,4)
  if k=='tanker':s+=box(17,43,214,78,'#cad5d5',39)+''.join(line(x,48,x,115,'#90a6a1',3) for x in [70,120,170])+box(99,28,45,15,'#b8c8bf',3)
  if k=='chassis':s+=line(18,112,233,112,green,8)+''.join(box(x,102,11,12,'#d6a85a',1) for x in [20,220])
  if k=='landing':s+=line(43,119,43,162,amber,10)+text(88,178,'Support legs',11)
  if k=='slider':s+=line(151,162,237,162,amber,5)+text(192,179,'Sliding tandem',10)
  return s
 if k=='coupling':return box(37,45,172,33,'#becbbd',15)+f'<path d="M110 44V63H138V44" fill="#f8faf4" stroke="{ink}" stroke-width="3"/>'+box(43,111,163,18,'#aec3a4',2)+line(71,80,71,109,ink,7)+line(178,80,178,109,ink,7)+box(117,0,14,40,'#c6b384',2)+text(202,18,'Kingpin',11)+line(177,17,135,17,amber,2)+text(124,158,'Fifth wheel on tractor',12)
 if k in ['hoses','connector']:return ''.join(f'<path d="M{x} 27Q{x-42} 64 {x} 87T{x} 148" fill="none" stroke="{c}" stroke-width="9"/>'+box(x-16,12,32,20,c,4)+box(x-16,148,32,20,c,4) for x,c in [(72,red),(178,blue)])+(text(70,187,'Supply',11)+text(180,187,'Service',11) if k=='hoses' else text(125,187,'Electrical connection concept',11))
 if k=='temperature':return box(17,30,215,132,'#c5d6cb')+box(32,45,185,95,'#183d35')+text(125,74,'REQUESTED / SETPOINT',11,'#d5e6ca')+text(125,106,'≠',32,'#f0d799')+text(125,128,'MEASURED / ACTUAL',11,'#d5e6ca')+circle(48,151,5)+circle(68,151,5)
 if k in ['warning','gauge','cycle']:return circle(125,94,71,'#e9eee4')+f'<path d="M65 107A62 62 0 0 1 184 107" fill="none" stroke="{amber}" stroke-width="12"/>'+line(125,105,164,67,ink,5)+circle(125,105,8,'#c1d2b9')+text(125,144,'OEM-specific limits',11)
 if k=='ecm':return box(62,45,126,97,'#a9c29c')+box(80,61,89,64,'#e3eadb')+text(125,101,'ECM / CODE',13)+''.join(line(x,27,x,45,ink,4)+line(x,142,x,160,ink,4) for x in range(78,181,23))+''.join(line(40,y,62,y,blue,4)+line(188,y,213,y,amber,4) for y in [65,89,113])
 if k=='stop':return f'<path d="M90 20H160L204 64V126L160 170H90L46 126V64Z" fill="#eed4c4" stroke="{red}" stroke-width="5"/>'+text(125,110,'STOP',30,red)
 if k=='location':return f'<path d="M125 153Q60 83 73 48Q91 4 135 15Q195 27 178 82Z" fill="#b9d0a7" stroke="{ink}" stroke-width="3"/>'+circle(125,60,23,'#f2f5ea')+f'<path d="M22 143L74 121L127 153L184 126L228 146V181L179 162L125 186L72 154L22 173Z" fill="none" stroke="{blue}" stroke-width="3"/>'
 if k=='camera':return box(28,51,195,107,'#bbcdb4')+box(55,32,63,19,'#95b082',3)+circle(126,103,39,'#e5ece2')+circle(126,103,26,'#63897d')+circle(198,70,6,'#ddb16b')
 if k=='clock':return circle(125,97,72,'#e5ecdf')+''.join(line(x,y,xx,yy,ink,3) for x,y,xx,yy in [(125,33,125,45),(125,149,125,161),(61,97,73,97),(177,97,189,97)])+line(125,97,125,57,ink,5)+line(125,97,163,118,amber,5)+circle(125,97,6)
 if k in ['calendar','document','inspection','cost','chart']:
  s=box(44,20,162,153,'#fdfef9',8)
  if k=='calendar':s+=box(44,20,162,36,'#9ab78b',5)+''.join(box(x,y,22,20,'#e1ead9',3) for x in [66,113,160] for y in [73,107,141])+line(79,7,79,30,ink,5)+line(171,7,171,30,ink,5)
  elif k=='chart':s+=line(65,148,184,148)+box(76,111,22,35,'#b5cb9e',2)+box(112,82,22,64,'#89ac76',2)+box(148,51,22,95,'#587e4b',2)
  elif k=='cost':s+=text(125,78,'$',42)+line(69,99,181,99)+text(125,122,'COST / MILES',12)+line(69,140,181,140,green,3)
  else:
   s+=box(80,9,90,24,'#a8bf97',4)
   for y in [61,93,125]:s+=box(63,y,17,17,'#e7efdf',3)+line(91,y+8,183,y+8,'#809b72',3)+line(66,y+8,70,y+13,green,2)+line(70,y+13,77,y+3,green,2)
  return s
 # General coordination relationship, for non-physical concepts.
 return ''.join(box(x,63,62,61,c)+text(x+31,100,str(i+1),24) for i,(x,c) in enumerate([(12,'#cfddc2'),(96,'#dae5d4'),(180,'#e8e9d6')]))+line(74,94,94,94,green,3)+line(158,94,178,94,green,3)

def svg(title,k,labels):
 labels=labels.split('|')
 right=''
 import textwrap
 for n,s in enumerate(labels):
  y=40+n*66
  right+=box(301,y,244,53,'#ffffff',7)+circle(319,y+26,10,'#e7efdf')+text(319,y+30,str(n+1),10)
  wraps=textwrap.wrap(s,29)
  for j,t in enumerate(wraps):right+=f'<text x="338" y="{y+25+j*15-(6 if len(wraps)>1 else 0)}" font-family="Arial,sans-serif" font-size="12" fill="{ink}">{html.escape(t)}</text>'
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 570 270" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)} — concept illustration</title><desc id="desc">Simplified visual with key concepts: {html.escape("; ".join(labels))}. Not a service diagram.</desc><rect width="570" height="270" rx="10" fill="#f0f4eb"/><text x="22" y="24" font-family="Arial,sans-serif" font-size="9" fill="#6a8161" letter-spacing="1.5">CONCEPT ILLUSTRATION</text><g transform="translate(12 41)">{scene(k)}</g>{right}</svg>'
manifest=json.loads((root/'assets/manifest.json').read_text())
manifest=[x for x in manifest if not x['file'].startswith('assets/lessons/')]
for idx,(l,items) in enumerate(zip(data['lessons'],specs),1):
 assert len(l['notes'])==len(items),(idx,len(l['notes']),len(items))
 l['visualNotes']=[]
 for n,(heading,kind,labels) in enumerate(items,1):
  filename=f'assets/lessons/{l["id"]}-{n}.svg'
  (root/filename).write_text(svg(heading,kind,labels))
  original=l['notes'][n-1]
  body=original[len(heading):].strip() if original.startswith(heading) else original
  alt=f'{heading}: '+labels.replace('|','; ')+'. Simplified concept illustration.'
  l['visualNotes'].append(dict(title=heading,text=body,image=filename,alt=alt,concepts=labels.split('|')))
  manifest.append(dict(file=filename,source=f'Original SVG concept illustration based on Fleet_MC_Training.pdf, page {l["page"]}',type='Original conceptual diagram',rights='Created for this project',review='Simplified relationships; not a mechanical service drawing',alt=alt))
 # Each lesson also contains the exact uncropped illustration embedded on its source PDF page.
 l['referenceImage']=f'assets/lessons/pdf-page-{l["page"]}.png'
 l['referenceAlt']=f'Original illustration embedded on PDF page {l["page"]}: {l["title"]}. Supplied artwork with unverified embedded labels.'
 manifest.append(dict(file=l['referenceImage'],source=f'Fleet_MC_Training.pdf, page {l["page"]}',type='Original supplied PDF illustration',rights='User-provided material; independent redistribution rights not verified',review='Shown unchanged as source artwork; embedded labels and example values are not independently verified',alt=l['referenceAlt']))
(root/'data/content.json').write_text(json.dumps(data,indent=2))
(root/'assets/manifest.json').write_text(json.dumps(manifest,indent=2))
print('Generated',sum(len(l['visualNotes']) for l in data['lessons']),'visual explanations across',len(data['lessons']),'lessons.')

glossary_specs={
'ABS':('wheel','Wheel-speed monitoring|Wheel-lock control|Faults require evaluation'),
'BOL':('document','Shipping document|Freight information|Bill of Lading'),
'Bobtail':('truck','Tractor only|No trailer attached|Equipment configuration'),
'Breakdown':('truck','Interrupted operation|Driver report|Service coordination'),
'CDL':('document','Commercial driving|Driver license|Applicable vehicle class'),
'CSA':('document','Compliance|Safety|Accountability'),
'CVSA':('inspection','Commercial vehicles|Inspection standards|Safety alliance'),
'Deadhead':('truck','Vehicle movement|Without a paying load|Trip context'),
'DEF':('def','Diesel exhaust fluid|Separate from diesel|Supports SCR aftertreatment'),
'DEL':('truck','Delivery|Receiving location|Dispatch abbreviation'),
'Detention':('clock','Shipper / receiver|Excess waiting|Record relevant times'),
'DOT':('document','Department of Transportation|US transportation framework|Confirm applicable rules'),
'DPF':('exhaust','Diesel particulate filter|Traps soot|OEM-specific regeneration'),
'Drop & Hook':('coupling','Drop one trailer|Connect another trailer|No live loading required'),
'DTC':('ecm','Diagnostic Trouble Code|Record exact code|Not a standalone diagnosis'),
'DVIR':('document','Driver Vehicle Inspection Report|Document reported defects|Applicable reporting rules'),
'ECM':('ecm','Electronic Control Module|Receives sensor information|Controls engine functions'),
'ELD':('document','Electronic Logging Device|Driver activity records|Hours-of-service context'),
'ETA':('clock','Estimated Time of Arrival|Communicate the estimate|Update if conditions change'),
'ETR':('clock','Repair / return estimate|Confirm intended meaning|Update during service'),
'FCFS':('clock','First Come|First Served|Queue order'),
'FMCSA':('document','Federal Motor Carrier|Safety Administration|US motor carrier safety'),
'GAWR':('load','Gross Axle Weight Rating|Manufacturer axle rating|Distinguish actual weight'),
'GCWR':('truck','Gross Combination Weight Rating|Combination rating|Tractor and trailer context'),
'Glad hands':('hoses','Air-line connectors|Service circuit|Emergency / supply circuit'),
'GVWR':('load','Gross Vehicle Weight Rating|Manufacturer vehicle rating|Distinguish actual weight'),
'HOS':('clock','Hours of Service|Driving / duty time|Applicable operating rules'),
'Inbound':('truck','Coming into a facility|Arrival direction|Facility perspective'),
'Kingpin':('coupling','Trailer coupling pin|Engages tractor fifth wheel|Qualified engagement check'),
'Layover':('clock','Extended wait|Between assignments|Dispatch context'),
'Live load':('van','Freight being loaded|Driver waits|Loading operation'),
'Live unload':('van','Freight being unloaded|Driver waits|Receiving operation'),
'Loaded miles':('truck','Distance traveled|Freight on board|Trip measurement'),
'OOS':('stop','Out of Service|Correct relevant conditions|Clearance before operation'),
'OEM':('document','Original Equipment Manufacturer|Vehicle / component maker|Model-specific information'),
'Outbound':('truck','Leaving a facility|Departure direction|Facility perspective'),
'PM':('calendar','Preventive Maintenance|Planned service|Fleet / OEM schedules'),
'PM A/B/C':('calendar','Fleet-specific service levels|Not universal DOT categories|Use approved schedules'),
'POD':('document','Proof of Delivery|Delivery confirmation|Dispatch documentation'),
'Pre-trip':('inspection','Before operation|Inspect vehicle condition|Follow applicable rules'),
'PU':('truck','Pickup|Shipping location|Dispatch abbreviation'),
'Reefer':('reefer','Refrigerated trailer|Or refrigeration unit|Temperature-sensitive freight'),
'RO':('document','Repair Order|Unit and complaint|Repair documentation'),
'Road call':('truck','Vehicle away from shop|Service dispatched|Location and equipment'),
'SCR':('scr','Selective Catalytic Reduction|DEF supports the process|NOx emissions control'),
'Steer axle':('axles','Steering axle|Normally front tractor axle|Identify by function'),
'Tandem':('tandem','Two grouped axles|Vehicle weight distribution|Axle function varies'),
'TMS':('workflow','Transportation Management System|Transportation operations|Software system'),
'Unit number':('document','Internal equipment ID|Fleet-assigned identifier|Distinct from VIN'),
'VIN':('document','Vehicle Identification Number|Manufacturer-assigned ID|Identify exact equipment'),
'WO':('document','Work Order|Complaint / diagnosis / work|Dates and authorization')}
for i,g in enumerate(data['glossary'],1):
 kind,labels=glossary_specs[g['term']]
 filename=f'assets/lessons/glossary-{i}.svg'
 # Bobtail must not be shown with an attached trailer.
 artwork=svg(g['term'],kind,labels)
 if g['term']=='Bobtail':artwork=artwork.replace(box(98,40,137,69,'#e9ede5',2),'').replace(wheel(198,123,16),'').replace(wheel(226,123,16),'')
 g['image']=filename;g['alt']=f'{g["term"]}: '+labels.replace('|','; ')+'. Concept illustration.'
 (root/filename).write_text(artwork)
 manifest=[a for a in manifest if a['file']!=filename]
 manifest.append(dict(file=filename,source='Original SVG concept illustration based on PDF glossary, pages 20–22',type='Original conceptual diagram',rights='Created for this project',review='Simplified educational association',alt=g['alt']))
(root/'data/content.json').write_text(json.dumps(data,indent=2))
(root/'assets/manifest.json').write_text(json.dumps(manifest,indent=2))
