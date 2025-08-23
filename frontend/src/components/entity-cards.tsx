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
    gradient: "",
    bgGradient: "",
    darkBgGradient: "",
    borderColor: "",
    textColor: "",
    badgeColor: ""
  },
  {
    key: "companies" as keyof EntityExtraction,
    title: "Companies",
    icon: Building,
    gradient: "",
    bgGradient: "",
    darkBgGradient: "",
    borderColor: "",
    textColor: "",
    badgeColor: ""
  },
  {
    key: "technologies" as keyof EntityExtraction,
    title: "Technologies",
    icon: Code,
    gradient: "",
    bgGradient: "",
    darkBgGradient: "",
    borderColor: "",
    textColor: "",
    badgeColor: ""
  },
  {
    key: "locations" as keyof EntityExtraction,
    title: "Locations",
    icon: MapPin,
    gradient: "",
    bgGradient: "",
    darkBgGradient: "",
    borderColor: "",
    textColor: "",
    badgeColor: ""
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
        <h3 className="mb-1 text-xl font-semibold text-slate-900 dark:text-slate-100">Entities</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400">Automatically identified people, companies, tech, and locations</p>
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
              <Card className="h-full border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
                <CardHeader className="pb-3">
                  <CardTitle className="flex items-center gap-2 text-base font-semibold text-slate-900 dark:text-slate-100">
                    <div className="p-2 rounded-md border border-slate-200/80 dark:border-slate-800">
                      <type.icon className="w-4 h-4 text-slate-500" />
                    </div>
                    <span>{type.title}</span>
                    <Badge
                      variant="outline"
                      className="ml-auto rounded-full border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs px-2 py-0.5"
                    >
                      {entityList.length}
                    </Badge>
                  </CardTitle>
                </CardHeader>

                <CardContent className="space-y-3">
                  <div className="flex flex-wrap gap-1.5">
                    {entityList.map((entity, entityIndex) => (
                      <motion.div
                        key={entity}
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.75 + index * 0.08 + entityIndex * 0.03 }}
                      >
                        <Badge
                          variant="outline"
                          className="rounded-full border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs px-3 py-1"
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