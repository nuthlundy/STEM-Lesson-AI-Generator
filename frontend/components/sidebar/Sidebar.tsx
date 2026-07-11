import { NavLink } from "react-router-dom";
import { 
  LayoutDashboard, 
  FolderOpen, 
  History, 
  Settings, 
  GraduationCap,
  Beaker,
  Dna,
  Calculator,
  BrainCircuit,
  Upload
} from "lucide-react";
import { cn } from "@/lib/utils";

const subjectModes = [
  { name: "Smart Mode", icon: BrainCircuit, id: "smart" },
  { name: "Mathematics", icon: Calculator, id: "math" },
  { name: "Physics", icon: GraduationCap, id: "physics" },
  { name: "Chemistry", icon: Beaker, id: "chemistry" },
  { name: "Biology", icon: Dna, id: "biology" },
];

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Projects", href: "/projects", icon: FolderOpen },
  { name: "History", href: "/history", icon: History },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  return (
    <div className="flex h-full w-64 flex-col border-r bg-muted/20">
      <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
        <NavLink to="/" className="flex items-center gap-2 font-semibold">
          <Upload className="h-6 w-6" />
          <span className="">STEM Lesson AI</span>
        </NavLink>
      </div>
      <div className="flex-1 overflow-auto py-2">
        <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary",
                  isActive ? "bg-muted text-primary" : ""
                )
              }
            >
              <item.icon className="h-4 w-4" />
              {item.name}
            </NavLink>
          ))}
        </nav>

        <div className="mt-4 px-4 py-2">
          <h4 className="mb-2 text-xs font-semibold uppercase tracking-tight text-muted-foreground">
            Subject Mode
          </h4>
          <nav className="grid items-start gap-1 text-sm">
            {subjectModes.map((mode) => (
              <button
                key={mode.id}
                className={cn(
                  "flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left text-muted-foreground transition-all hover:bg-muted hover:text-primary",
                  mode.id === "smart" && "bg-muted font-medium text-primary"
                )}
              >
                <mode.icon className="h-4 w-4" />
                {mode.name}
              </button>
            ))}
          </nav>
        </div>
      </div>
    </div>
  );
}
