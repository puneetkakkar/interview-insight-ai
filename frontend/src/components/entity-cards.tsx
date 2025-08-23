"use client";

import { motion } from "framer-motion";
import { Users, Building, Code, MapPin } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { EntityExtraction } from "@/types/interview";

interface EntityCardsProps {
  entities: EntityExtraction;
}

const entityTypes = [
  {
    key: "people" as keyof EntityExtraction,
    title: "People",
    icon: Users,
    gradient: "from-blue-500 to-blue-600",
    bgGradient: "from-blue-50 to-blue-100/50",
    darkBgGradient: "from-blue-950/30 to-blue-900/30",
    borderColor: "border-blue-200 dark:border-blue-700",
    textColor: "text-blue-700 dark:text-blue-300",
    badgeColor: "bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-700"
  },
  {
    key: "companies" as keyof EntityExtraction,
    title: "Companies",
    icon: Building,
    gradient: "from-coral-500 to-coral-600",
    bgGradient: "from-coral-50 to-coral-100/50",
    darkBgGradient: "from-coral-950/30 to-coral-900/30",
    borderColor: "border-coral-200 dark:border-coral-700",
    textColor: "text-coral-700 dark:text-coral-300",
    badgeColor: "bg-coral-100 dark:bg-coral-900/40 text-coral-700 dark:text-coral-300 border-coral-200 dark:border-coral-700"
  },
  {
    key: "technologies" as keyof EntityExtraction,
    title: "Technologies",
    icon: Code,
    gradient: "from-purple-500 to-purple-600",
    bgGradient: "from-purple-50 to-purple-100/50",
    darkBgGradient: "from-purple-950/30 to-purple-900/30",
    borderColor: "border-purple-200 dark:border-purple-700",
    textColor: "text-purple-700 dark:text-purple-300",
    badgeColor: "bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-700"
  },
  {
    key: "locations" as keyof EntityExtraction,
    title: "Locations",
    icon: MapPin,
    gradient: "from-emerald-500 to-emerald-600",
    bgGradient: "from-emerald-50 to-emerald-100/50",
    darkBgGradient: "from-emerald-950/30 to-emerald-900/30",
    borderColor: "border-emerald-200 dark:border-emerald-700",
    textColor: "text-emerald-700 dark:text-emerald-300",
    badgeColor: "bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-700"
  }
];

export function EntityCards({ entities }: EntityCardsProps) {
  const hasEntities = entityTypes.some(type => entities[type.key].length > 0);
  const availableEntities = entityTypes.filter(type => entities[type.key].length > 0);

  if (!hasEntities) {
    return null;
  }

  // Determine grid layout based on number of entities
  const getGridCols = (count: number) => {
    if (count === 1) return "grid-cols-1";
    if (count === 2) return "grid-cols-1 md:grid-cols-2";
    if (count === 3) return "grid-cols-1 md:grid-cols-3";
    return "grid-cols-1 md:grid-cols-2 lg:grid-cols-4";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-800 to-coral-700 dark:from-blue-200 dark:to-coral-200 bg-clip-text text-transparent mb-2">
          Extracted Entities
        </h3>
        <p className="text-slate-600 dark:text-slate-300">
          Key entities identified in your interview transcript
        </p>
      </div>

      <div className={`grid ${getGridCols(availableEntities.length)} gap-6`}>
        {availableEntities.map((type, index) => {
          const entityList = entities[type.key];
          if (entityList.length === 0) return null;

          return (
            <motion.div
              key={type.key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 + index * 0.1 }}
              className="h-full"
            >
              <Card className="glass-strong border-0 shadow-xl h-full hover:shadow-2xl transition-all duration-300 group">
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-3 text-lg">
                    <div className={`p-3 rounded-xl bg-gradient-to-br ${type.bgGradient} dark:${type.darkBgGradient} group-hover:scale-110 transition-transform duration-200`}>
                      <type.icon className={`w-6 h-6 ${type.textColor}`} />
                    </div>
                    <span className={`${type.textColor} font-semibold`}>{type.title}</span>
                    <Badge 
                      variant="secondary" 
                      className="ml-auto bg-gradient-to-r from-slate-100 to-slate-200 dark:from-slate-800 dark:to-slate-700 text-slate-700 dark:text-slate-300 border-0"
                    >
                      {entityList.length}
                    </Badge>
                  </CardTitle>
                </CardHeader>
                
                <CardContent className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    {entityList.map((entity, entityIndex) => (
                      <motion.div
                        key={entity}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.8 + index * 0.1 + entityIndex * 0.05 }}
                      >
                        <Badge 
                          variant="secondary" 
                          className={`${type.badgeColor} text-sm border-2 rounded-full px-3 py-1 font-medium hover:scale-105 transition-transform duration-200`}
                        >
                          {entity}
                        </Badge>
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}