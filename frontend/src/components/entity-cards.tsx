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
    bgColor: "from-blue-50 to-blue-100/50 dark:from-blue-950/30 dark:to-blue-900/30",
    borderColor: "border-blue-200 dark:border-blue-800",
    textColor: "text-blue-700 dark:text-blue-300",
    badgeColor: "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-700"
  },
  {
    key: "companies" as keyof EntityExtraction,
    title: "Companies",
    icon: Building,
    bgColor: "from-purple-50 to-purple-100/50 dark:from-purple-950/30 dark:to-purple-900/30",
    borderColor: "border-purple-200 dark:border-purple-800",
    textColor: "text-purple-700 dark:text-purple-300",
    badgeColor: "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-700"
  },
  {
    key: "technologies" as keyof EntityExtraction,
    title: "Technologies",
    icon: Code,
    bgColor: "from-green-50 to-green-100/50 dark:from-green-950/30 dark:to-green-900/30",
    borderColor: "border-green-200 dark:border-green-800",
    textColor: "text-green-700 dark:text-green-300",
    badgeColor: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-700"
  },
  {
    key: "locations" as keyof EntityExtraction,
    title: "Locations",
    icon: MapPin,
    bgColor: "from-orange-50 to-orange-100/50 dark:from-orange-950/30 dark:to-orange-900/30",
    borderColor: "border-orange-200 dark:border-orange-800",
    textColor: "text-orange-700 dark:text-orange-300",
    badgeColor: "bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 border-orange-200 dark:border-orange-700"
  }
];

export function EntityCards({ entities }: EntityCardsProps) {
  const hasEntities = entityTypes.some(type => entities[type.key].length > 0);

  if (!hasEntities) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-2">
          Extracted Entities
        </h3>
        <p className="text-slate-600 dark:text-slate-300">
          Key entities identified in your interview transcript
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {entityTypes.map((type, index) => {
          const entityList = entities[type.key];
          if (entityList.length === 0) return null;

          return (
            <motion.div
              key={type.key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 + index * 0.1 }}
            >
              <Card className={`bg-gradient-to-br ${type.bgColor} ${type.borderColor} h-full`}>
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-3 text-lg">
                    <div className="p-2 rounded-lg bg-white/50 dark:bg-slate-800/50">
                      <type.icon className={`w-5 h-5 ${type.textColor}`} />
                    </div>
                    <span className={type.textColor}>{type.title}</span>
                  </CardTitle>
                </CardHeader>
                
                <CardContent className="space-y-2">
                  {entityList.map((entity, entityIndex) => (
                    <motion.div
                      key={entity}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.8 + index * 0.1 + entityIndex * 0.05 }}
                    >
                      <Badge 
                        variant="secondary" 
                        className={`${type.badgeColor} text-sm`}
                      >
                        {entity}
                      </Badge>
                    </motion.div>
                  ))}
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}